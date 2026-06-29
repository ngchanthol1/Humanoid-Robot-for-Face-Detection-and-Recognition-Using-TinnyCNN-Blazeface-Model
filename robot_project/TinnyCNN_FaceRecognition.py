#!/usr/bin/env python3
"""
Humanoid Robot Control System - FIXED VERSION
Works on Windows and Raspberry Pi 5
Integrates face recognition with RGB servo motor control
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import serial
import serial.tools.list_ports
import cv2
import threading
import time
import os
from datetime import datetime
import numpy as np
from pathlib import Path

# Try to import PIL/Pillow ImageTk
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    print("=" * 70)
    print("ERROR: PIL ImageTk not available")
    print("=" * 70)
    print("\nPlease install the required package:")
    print("  Windows: pip install pillow")
    print("  Raspberry Pi: sudo apt install python3-pil python3-pil.imagetk")
    print("\nOr using pip:")
    print("  pip3 install pillow --break-system-packages")
    print("\nThen restart the application.")
    print("=" * 70)
    exit(1)

# Import face recognition components
FACE_RECOGNITION_AVAILABLE = False
try:
    from blazeface_detector import BlazeFaceDetector
    from tinycnn_recognizer import TinyCNNRecognizer
    FACE_RECOGNITION_AVAILABLE = True
    print("✓ Face recognition modules loaded successfully")
except ImportError as e:
    print(f"⚠ Warning: Face recognition modules not found ({e})")
    print("Face detection will use OpenCV fallback.")
    print("\nMake sure these files exist:")
    print("  - blazeface_detector.py")
    print("  - tinycnn_recognizer.py")
    print("  - models/blazeface.tflite (auto-downloads)")
    print("  - models/tinycnn_mrdavid.tflite (from training)")

class HumanoidRobotGUI:
    def __init__(self, root):
        # Add new by me
        self.face_padding_percent = 0.2  # Face crop padding (0.0-0.5)
        self.camera_fps = 30              # Camera capture FPS
        self.processing_delay = 0.05      # Processing delay (lower = faster)
        # End add new by me
        self.root = root
        self.root.title("🤖 Humanoid Robot Control System - Raspberry Pi 5")
        self.root.geometry("1600x900")
        
        # Serial connection
        self.serial_port = None
        self.is_connected = False
        
        # Camera and face recognition
        self.camera = None
        self.camera_running = False
        self.face_detection_active = False
        self.recognition_active = False
        
        # Face recognition components
        self.detector = None
        self.recognizer = None
        
        # Motor states (16 motors)
        self.current_angles = {i: 0 for i in range(1, 17)}
        self.current_colors = {i: "RGBMIX" for i in range(1, 17)}
        
        # RGB Color protocols
        self.rgb_protocols = self.load_rgb_protocols()
        self.angle_protocols = self.generate_angle_protocols()
        
        # Threading locks
        self.serial_lock = threading.Lock()
        self.camera_lock = threading.Lock()
        
        # Greeting control
        self._greeting_in_progress = False
        self._last_greeting_time = 0
        self._last_recognized_person = None
        
        # Create GUI
        self.create_widgets()
        
        # Auto-refresh COM ports
        self.refresh_ports()
    
    def load_rgb_protocols(self):
        """Load RGB color protocols for 16 motors"""
        return {
            1: {"RGBMIX": "FFFF01070DE00D", "REDGREEN": "FFFF01070DC02D", "GREENBLUE": "FFFF01070D608D"},
            2: {"RGBMIX": "FFFF02070DE00C", "REDGREEN": "FFFF02070DC02C", "GREENBLUE": "FFFF02070D608C"},
            3: {"RGBMIX": "FFFF03070DE00B", "REDGREEN": "FFFF03070DC02B", "GREENBLUE": "FFFF03070D608B"},
            4: {"RGBMIX": "FFFF04070DE00A", "REDGREEN": "FFFF04070DC02A", "GREENBLUE": "FFFF04070D608A"},
            5: {"RGBMIX": "FFFF05070DE009", "REDGREEN": "FFFF05070DC029", "GREENBLUE": "FFFF05070D6089"},
            6: {"RGBMIX": "FFFF06070DE008", "REDGREEN": "FFFF06070DC028", "GREENBLUE": "FFFF06070D6088"},
            7: {"RGBMIX": "FFFF07070DE007", "REDGREEN": "FFFF07070DC027", "GREENBLUE": "FFFF07070D6087"},
            8: {"RGBMIX": "FFFF08070DE006", "REDGREEN": "FFFF08070DC026", "GREENBLUE": "FFFF08070D6086"},
            9: {"RGBMIX": "FFFF09070DE005", "REDGREEN": "FFFF09070DC025", "GREENBLUE": "FFFF09070D6085"},
            10: {"RGBMIX": "FFFF0A070DE004", "REDGREEN": "FFFF0A070DC024", "GREENBLUE": "FFFF0A070D6084"},
            11: {"RGBMIX": "FFFF0B070DE003", "REDGREEN": "FFFF0B070DC023", "GREENBLUE": "FFFF0B070D6083"},
            12: {"RGBMIX": "FFFF0C070DE002", "REDGREEN": "FFFF0C070DC022", "GREENBLUE": "FFFF0C070D6082"},
            13: {"RGBMIX": "FFFF0D070DE001", "REDGREEN": "FFFF0D070DC021", "GREENBLUE": "FFFF0D070D6081"},
            14: {"RGBMIX": "FFFF0E070DE000", "REDGREEN": "FFFF0E070DC020", "GREENBLUE": "FFFF0E070D6080"},
            15: {"RGBMIX": "FFFF0F070DE0FF", "REDGREEN": "FFFF0F070DC01F", "GREENBLUE": "FFFF0F070D607F"},
            16: {"RGBMIX": "FFFF10070DE0FE", "REDGREEN": "FFFF10070DC01E", "GREENBLUE": "FFFF10070D607E"}
        }
    
    def generate_angle_protocols(self):
        """Generate angle protocols for common angles (-160 to 160)"""
        protocols = {}
        
        # Common angles for quick reference
        common_angles = [-160, -90, -45, -20, 0, 20, 45, 90, 160]
        
        for motor in range(1, 17):
            protocols[motor] = {}
            motor_hex = format(motor, '02X')
            
            for angle in common_angles:
                # Calculate angle value for protocol
                angle_value = (angle + 160) * 13
                angle_hex = format(int(angle_value), '04X')
                
                # Build protocol
                protocol = f"FFFF{motor_hex}0A0E{angle_hex}03E8"
                checksum = self.calculate_checksum(protocol)
                protocols[motor][str(angle)] = protocol + checksum
        
        return protocols
    
    def calculate_checksum(self, hex_string):
        """Calculate checksum for protocol"""
        total = sum(int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2))
        checksum = (256 - (total % 256)) % 256
        return format(checksum, '02X')
    
    def create_widgets(self):
        """Create main GUI layout"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Left panel - Camera and Face Recognition
        self.create_camera_panel(main_frame)
        
        # Right panel - Motor Controls
        self.create_control_panel(main_frame)
        
        # Bottom panel - Serial Connection and Logs
        self.create_bottom_panel(main_frame)
    
    def create_camera_panel(self, parent):
        """Create camera and face recognition panel"""
        camera_frame = ttk.LabelFrame(parent, text="📷 Camera & Face Recognition", padding="10")
        camera_frame.grid(row=0, column=0, rowspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Camera display container
        self.camera_container = tk.Frame(camera_frame, bg="black", width=640, height=480)
        self.camera_container.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        self.camera_container.grid_remove()  # Hide initially
        
        self.camera_label = tk.Label(self.camera_container, bg="black")
        self.camera_label.pack()
        
        # Placeholder message
        self.placeholder_frame = tk.Frame(camera_frame, bg="#2C3E50", width=640, height=480, 
                                         relief="solid", borderwidth=2)
        self.placeholder_frame.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        self.placeholder_frame.grid_propagate(False)
        
        placeholder_content = tk.Frame(self.placeholder_frame, bg="#2C3E50")
        placeholder_content.place(relx=0.5, rely=0.5, anchor="center")
        
        icon_label = tk.Label(placeholder_content, text="📷", font=("Arial", 80), 
                             bg="#2C3E50", fg="white")
        icon_label.pack(pady=10)
        
        msg_label = tk.Label(placeholder_content, 
                            text="Camera Not Active\n\nClick 'Start Detection & Scanning' below\nto begin face recognition", 
                            font=("Arial", 16, "bold"), bg="#2C3E50", fg="white",
                            justify="center")
        msg_label.pack(pady=10)
        
        # Face detection controls
        detection_frame = ttk.LabelFrame(camera_frame, text="🎯 Face Detection & Recognition", padding="15")
        detection_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Main detection button
        self.detect_face_btn = ttk.Button(detection_frame, text="🔍 Start Detection & Scanning", 
                                         command=self.start_detection_scanning, width=35,
                                         style="Accent.TButton")
        self.detect_face_btn.grid(row=0, column=0, pady=10, padx=5)
        
        # Stop button
        self.stop_detection_btn = ttk.Button(detection_frame, text="⏹️ Stop Detection", 
                                            command=self.stop_detection_scanning, 
                                            state="disabled", width=35)
        self.stop_detection_btn.grid(row=1, column=0, pady=5, padx=5)
        
        # Status display
        status_container = ttk.Frame(detection_frame)
        status_container.grid(row=2, column=0, pady=10)
        
        self.face_status = ttk.Label(status_container, text="Status: Ready to Start", 
                                    font=("Arial", 11, "bold"), foreground="#3498DB")
        self.face_status.pack(pady=5)
        
        # Recognition result
        self.recognition_result = ttk.Label(status_container, text="", 
                                           font=("Arial", 14, "bold"),
                                           foreground="#2ECC71")
        self.recognition_result.pack(pady=5)
        
        # Model info
        model_status = "✓ Ready" if FACE_RECOGNITION_AVAILABLE else "⚠ Using OpenCV fallback"
        model_info = ttk.Label(detection_frame, 
                              text=f"📁 Models: blazeface.tflite + tinycnn_mrdavid.tflite - {model_status}",
                              font=("Arial", 9, "italic"), foreground="#7F8C8D")
        model_info.grid(row=3, column=0, pady=5)
        
        # Info label
        info_label = ttk.Label(detection_frame, 
                              text="ℹ️ Recognition activates automatically when scanning starts",
                              font=("Arial", 9, "italic"), foreground="gray")
        info_label.grid(row=4, column=0, pady=5)
    
    def create_control_panel(self, parent):
        """Create motor control panel"""
        control_main = ttk.Frame(parent)
        control_main.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Global controls
        global_frame = ttk.LabelFrame(control_main, text="🎮 Global Controls", padding="10")
        global_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Angle controls
        angle_frame = ttk.Frame(global_frame)
        angle_frame.grid(row=0, column=0, pady=5)
        
        ttk.Label(angle_frame, text="Set All Angles:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        ttk.Button(angle_frame, text="-90°", width=8, 
                  command=lambda: self.set_all_angles(-90)).grid(row=0, column=1, padx=2)
        ttk.Button(angle_frame, text="0°", width=8, 
                  command=lambda: self.set_all_angles(0)).grid(row=0, column=2, padx=2)
        ttk.Button(angle_frame, text="90°", width=8, 
                  command=lambda: self.set_all_angles(90)).grid(row=0, column=3, padx=2)
        
        # Color controls
        color_frame = ttk.Frame(global_frame)
        color_frame.grid(row=1, column=0, pady=5)
        
        ttk.Label(color_frame, text="Set All Colors:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        tk.Button(color_frame, text="🔴 Red", width=8, bg="#FF6B6B", fg="white",
                 command=lambda: self.set_all_colors("RGBMIX")).grid(row=0, column=1, padx=2)
        tk.Button(color_frame, text="🟢 Green", width=8, bg="#51CF66", fg="white",
                 command=lambda: self.set_all_colors("REDGREEN")).grid(row=0, column=2, padx=2)
        tk.Button(color_frame, text="🔵 Blue", width=8, bg="#339AF0", fg="white",
                 command=lambda: self.set_all_colors("GREENBLUE")).grid(row=0, column=3, padx=2)
        
        # Patterns
        pattern_frame = ttk.Frame(global_frame)
        pattern_frame.grid(row=2, column=0, pady=5)
        
        ttk.Button(pattern_frame, text="🌈 Rainbow Wave", width=15,
                  command=self.rainbow_wave).grid(row=0, column=0, padx=2)
        ttk.Button(pattern_frame, text="↕️ Wave Motion", width=15,
                  command=self.wave_motion).grid(row=0, column=1, padx=2)
        ttk.Button(pattern_frame, text="⏹️ Stop All", width=15,
                  command=self.stop_all, style="Accent.TButton").grid(row=0, column=2, padx=2)
        
        # Individual motor controls
        motors_frame = ttk.LabelFrame(control_main, text="🔧 Individual Motor Controls (1-16)", 
                                     padding="10")
        motors_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create scrollable motor controls
        canvas = tk.Canvas(motors_frame, height=400)
        scrollbar = ttk.Scrollbar(motors_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Create 16 motor widgets in 4x4 grid
        self.motor_widgets = {}
        for i in range(16):
            motor_num = i + 1
            row = i // 4
            col = i % 4
            self.create_motor_widget(scrollable_frame, motor_num, row, col)
    
    def create_bottom_panel(self, parent):
        """Create serial connection and log panel"""
        bottom_frame = ttk.Frame(parent)
        bottom_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Serial connection
        conn_frame = ttk.LabelFrame(bottom_frame, text="🔌 Serial Connection (UART)", padding="10")
        conn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Port selection
        port_frame = ttk.Frame(conn_frame)
        port_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(port_frame, text="Port:").grid(row=0, column=0, padx=5)
        self.port_var = tk.StringVar(value="/dev/ttyAMA0" if os.name != 'nt' else "COM3")
        self.port_combo = ttk.Combobox(port_frame, textvariable=self.port_var, width=15)
        self.port_combo.grid(row=0, column=1, padx=5)
        
        ttk.Label(port_frame, text="Baud:").grid(row=0, column=2, padx=5)
        self.baud_var = tk.StringVar(value="115200")
        baud_combo = ttk.Combobox(port_frame, textvariable=self.baud_var, width=10)
        baud_combo['values'] = ('9600', '19200', '38400', '57600', '115200')
        baud_combo.grid(row=0, column=3, padx=5)
        
        self.connect_btn = ttk.Button(port_frame, text="Connect", 
                                      command=self.connect_serial, width=12)
        self.connect_btn.grid(row=0, column=4, padx=5)
        
        self.disconnect_btn = ttk.Button(port_frame, text="Disconnect", 
                                        command=self.disconnect_serial, 
                                        state="disabled", width=12)
        self.disconnect_btn.grid(row=0, column=5, padx=5)
        
        self.status_label = ttk.Label(port_frame, text="● Disconnected", 
                                     foreground="red", font=("Arial", 10, "bold"))
        self.status_label.grid(row=0, column=6, padx=10)
        
        # Log
        log_frame = ttk.LabelFrame(bottom_frame, text="📋 Activity Log", padding="5")
        log_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=80, height=10, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Button(log_frame, text="Clear Log", command=self.clear_log).grid(row=1, column=0, pady=5)
        
        bottom_frame.rowconfigure(1, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
    
    def create_motor_widget(self, parent, motor_num, row, col):
        """Create individual motor control widget"""
        motor_frame = ttk.LabelFrame(parent, text=f"Motor {motor_num}", padding="5")
        motor_frame.grid(row=row, column=col, padx=3, pady=3, sticky=(tk.W, tk.E))
        
        # Status display with color indicator
        status_canvas = tk.Canvas(motor_frame, width=120, height=30, bg="#FF6B6B", 
                                 highlightthickness=1, highlightbackground="gray")
        status_canvas.grid(row=0, column=0, columnspan=3, pady=3)
        
        angle_text = status_canvas.create_text(60, 15, text="0°", 
                                              font=("Arial", 12, "bold"), fill="white")
        
        # Angle control
        angle_frame = ttk.Frame(motor_frame)
        angle_frame.grid(row=1, column=0, columnspan=3, pady=3)
        
        ttk.Label(angle_frame, text="Angle:").grid(row=0, column=0)
        angle_entry = ttk.Entry(angle_frame, width=6)
        angle_entry.grid(row=0, column=1, padx=2)
        angle_entry.insert(0, "0")
        
        ttk.Button(angle_frame, text="Set", width=4,
                  command=lambda: self.set_motor_angle(motor_num)).grid(row=0, column=2)
        
        # Quick angles
        quick_frame = ttk.Frame(motor_frame)
        quick_frame.grid(row=2, column=0, columnspan=3, pady=2)
        
        for i, angle in enumerate([-90, 0, 90]):
            ttk.Button(quick_frame, text=f"{angle}°", width=5,
                      command=lambda m=motor_num, a=angle: self.quick_angle(m, a)).grid(
                          row=0, column=i, padx=1)
        
        # Color buttons
        color_frame = ttk.Frame(motor_frame)
        color_frame.grid(row=3, column=0, columnspan=3, pady=3)
        
        colors = [("🔴", "#FF6B6B", "RGBMIX"), 
                  ("🟢", "#51CF66", "REDGREEN"), 
                  ("🔵", "#339AF0", "GREENBLUE")]
        
        for i, (emoji, bg, color_name) in enumerate(colors):
            tk.Button(color_frame, text=emoji, width=4, bg=bg, fg="white",
                     command=lambda m=motor_num, c=color_name: self.set_motor_color(m, c)).grid(
                         row=0, column=i, padx=1)
        
        # Store widgets
        self.motor_widgets[motor_num] = {
            'frame': motor_frame,
            'status_canvas': status_canvas,
            'angle_text': angle_text,
            'angle_entry': angle_entry
        }
    
    # ===== SERIAL COMMUNICATION =====
    
    def refresh_ports(self):
        """Refresh available serial ports"""
        if os.name == 'nt':  # Windows
            ports = [f"COM{i}" for i in range(1, 20)]
        else:  # Linux/Raspberry Pi
            ports = ["/dev/ttyAMA0", "/dev/ttyUSB0", "/dev/ttyACM0"]
        
        ports.extend([port.device for port in serial.tools.list_ports.comports()])
        self.port_combo['values'] = list(set(ports))
    
    def connect_serial(self):
        """Connect to STM32 via UART"""
        try:
            if self.is_connected:
                return
            
            port = self.port_var.get()
            baud = int(self.baud_var.get())
            
            self.serial_port = serial.Serial(port=port, baudrate=baud, timeout=1)
            time.sleep(0.5)
            
            self.is_connected = True
            self.status_label.config(text="● Connected", foreground="green")
            self.connect_btn.config(state="disabled")
            self.disconnect_btn.config(state="normal")
            
            self.log_message(f"✓ Connected to {port} at {baud} baud")
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
            self.log_message(f"✗ Connection error: {str(e)}")
    
    def disconnect_serial(self):
        """Disconnect from serial port"""
        try:
            if self.serial_port and self.is_connected:
                self.serial_port.close()
                self.is_connected = False
                self.status_label.config(text="● Disconnected", foreground="red")
                self.connect_btn.config(state="normal")
                self.disconnect_btn.config(state="disabled")
                self.log_message("Disconnected from serial port")
        except Exception as e:
            self.log_message(f"Disconnect error: {str(e)}")
    
    def send_hex_command(self, hex_string, description=""):
        """Send hex command to STM32"""
        if not self.is_connected or not self.serial_port:
            self.log_message("⚠ Not connected to serial port")
            return False
        
        try:
            with self.serial_lock:
                hex_bytes = bytes.fromhex(hex_string)
                self.serial_port.write(hex_bytes)
                self.log_message(f"→ {description}: {hex_string}")
                time.sleep(0.02)
                return True
        except Exception as e:
            self.log_message(f"✗ Send error: {str(e)}")
            return False
    
    # ===== MOTOR CONTROL =====
    
    def set_motor_angle(self, motor_num):
        """Set motor angle"""
        try:
            entry = self.motor_widgets[motor_num]['angle_entry']
            angle = int(entry.get().strip())
            
            if angle < -160 or angle > 160:
                messagebox.showerror("Invalid Range", "Angle must be between -160° and 160°")
                return
            
            angle_str = str(angle)
            if angle_str in self.angle_protocols[motor_num]:
                cmd = self.angle_protocols[motor_num][angle_str]
            else:
                available = [int(a) for a in self.angle_protocols[motor_num].keys()]
                nearest = min(available, key=lambda x: abs(x - angle))
                cmd = self.angle_protocols[motor_num][str(nearest)]
                self.log_message(f"⚠ Using nearest angle: {nearest}°")
            
            if self.send_hex_command(cmd, f"Motor {motor_num} → {angle}°"):
                self.current_angles[motor_num] = angle
                self.update_motor_display(motor_num)
                
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer")
    
    def quick_angle(self, motor_num, angle):
        """Set motor to preset angle"""
        entry = self.motor_widgets[motor_num]['angle_entry']
        entry.delete(0, tk.END)
        entry.insert(0, str(angle))
        self.set_motor_angle(motor_num)
    
    def set_motor_color(self, motor_num, color):
        """Set motor RGB color"""
        if motor_num in self.rgb_protocols and color in self.rgb_protocols[motor_num]:
            cmd = self.rgb_protocols[motor_num][color]
            
            if self.send_hex_command(cmd, f"Motor {motor_num} → {color}"):
                self.current_colors[motor_num] = color
                self.update_motor_display(motor_num)
    
    def update_motor_display(self, motor_num):
        """Update motor status display"""
        color_map = {
            "RGBMIX": "#FF6B6B",
            "REDGREEN": "#51CF66",
            "GREENBLUE": "#339AF0"
        }
        
        widgets = self.motor_widgets[motor_num]
        angle = self.current_angles[motor_num]
        color = self.current_colors[motor_num]
        
        canvas = widgets['status_canvas']
        canvas.config(bg=color_map.get(color, "#FFFFFF"))
        canvas.itemconfig(widgets['angle_text'], text=f"{angle}°")
    
    def set_all_angles(self, angle):
        """Set all motors to same angle"""
        for motor_num in range(1, 17):
            entry = self.motor_widgets[motor_num]['angle_entry']
            entry.delete(0, tk.END)
            entry.insert(0, str(angle))
            self.set_motor_angle(motor_num)
            time.sleep(0.03)
    
    def set_all_colors(self, color):
        """Set all motors to same color"""
        for motor_num in range(1, 17):
            self.set_motor_color(motor_num, color)
            time.sleep(0.03)
    
    def stop_all(self):
        """Stop all motors"""
        self.set_all_angles(0)
        self.log_message("⏹️ All motors stopped")
    
    def rainbow_wave(self):
        """Execute rainbow wave pattern"""
        def wave():
            self.log_message("🌈 Starting rainbow wave...")
            colors = ["RGBMIX", "REDGREEN", "GREENBLUE"]
            
            for cycle in range(2):
                for offset in range(3):
                    for i in range(16):
                        motor = i + 1
                        color = colors[(i + offset) % 3]
                        self.set_motor_color(motor, color)
                    time.sleep(0.5)
            
            self.log_message("✓ Rainbow wave completed")
        
        threading.Thread(target=wave, daemon=True).start()
    
    def wave_motion(self):
        """Execute wave motion pattern"""
        def motion():
            self.log_message("↕️ Starting wave motion...")
            angles = [-45, 0, 45, 0]
            
            for angle in angles * 2:
                self.set_all_angles(angle)
                time.sleep(0.4)
            
            self.set_all_angles(0)
            self.log_message("✓ Wave motion completed")
        
        threading.Thread(target=motion, daemon=True).start()
    
    # ===== CAMERA AND FACE RECOGNITION =====
    
    def start_detection_scanning(self):
        """Start camera and face detection with automatic recognition"""
        try:
            if self.camera_running:
                return
            
            # Open camera
            self.camera = cv2.VideoCapture(0)
            
            if not self.camera.isOpened():
                messagebox.showerror("Camera Error", "Could not open camera")
                return
            
            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            # self.camera.set(cv2.CAP_PROP_FPS, 30)
            self.camera.set(cv2.CAP_PROP_FPS, 1)
            
            # Load face recognition models
            if FACE_RECOGNITION_AVAILABLE:
                try:
                    self.log_message("📁 Loading face recognition models...")
                    
                    # Load BlazeFace detector (will auto-download if needed)
                    if self.detector is None:
                        self.log_message("Loading BlazeFace detector...")
                        self.detector = BlazeFaceDetector(
                            model_path="models/blazeface.tflite",
                            confidence_threshold=0.70
                        )
                        self.log_message("✓ BlazeFace detector loaded")
                    
                    # Load TinyCNN recognizer
                    if self.recognizer is None:
                        # Try multiple model paths
                        model_paths = [
                            "models/tinycnn_mrdavid.tflite",
                            "models/ultra_robust_int8.tflite",
                            "models/ultra_robust_float32.tflite"
                        ]
                        
                        for model_path in model_paths:
                            if Path(model_path).exists():
                                self.log_message(f"Loading recognizer: {model_path}")
                                self.recognizer = TinyCNNRecognizer(
                                    model_path=model_path,
                                    david_threshold=0.80,
                                    min_confidence=0.70,
                                    enable_quality_check=True
                                    # confidence_threshold=0.80,
                                    
                                )
                                if self.recognizer.model_available:
                                    self.log_message("✓ TinyCNN recognizer loaded")
                                    break
                        
                        if self.recognizer is None or not self.recognizer.model_available:
                            self.log_message("⚠ No trained model found")
                            self.log_message("Train model first: python3 train_model.py")
                    
                except Exception as model_err:
                    self.log_message(f"⚠ Model loading error: {str(model_err)}")
                    self.log_message("Using OpenCV fallback detection")
            
            # Show camera display
            self.placeholder_frame.grid_remove()
            self.camera_container.grid()
            
            self.camera_running = True
            self.face_detection_active = True
            self.recognition_active = True
            
            # Update button states
            self.detect_face_btn.config(state="disabled")
            self.stop_detection_btn.config(state="normal")
            
            # Start camera thread
            threading.Thread(target=self.camera_loop, daemon=True).start()
            
            self.face_status.config(text="Status: Scanning for faces...", foreground="orange")
            self.log_message("📷 Camera started - Recognition ACTIVE")
            
        except Exception as e:
            messagebox.showerror("Camera Error", f"Failed to start camera: {str(e)}")
            self.log_message(f"✗ Camera error: {str(e)}")
    
    def stop_detection_scanning(self):
        """Stop camera and face detection"""
        self.camera_running = False
        self.face_detection_active = False
        self.recognition_active = False
        
        if self.camera:
            self.camera.release()
            self.camera = None
        
        # Hide camera display, show placeholder
        self.camera_container.grid_remove()
        self.placeholder_frame.grid()
        
        # Update button states
        self.detect_face_btn.config(state="normal")
        self.stop_detection_btn.config(state="disabled")
        
        self.face_status.config(text="Status: Stopped", foreground="red")
        self.recognition_result.config(text="")
        
        self.log_message("📷 Camera stopped")
    
    def camera_loop(self):
        """Main camera processing loop"""
        while self.camera_running:
            try:
                ret, frame = self.camera.read()
                
                if not ret:
                    self.log_message("⚠ Failed to read frame")
                    break
                
                # Process frame for face detection
                if self.face_detection_active:
                    frame = self.process_frame_for_faces(frame)
                
                # Convert and display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img = img.resize((640, 480), Image.Resampling.LANCZOS)
                imgtk = ImageTk.PhotoImage(image=img)
                
                self.camera_label.imgtk = imgtk
                self.camera_label.configure(image=imgtk)
                
            except Exception as e:
                self.log_message(f"✗ Camera loop error: {str(e)}")
                break
            
            time.sleep(0.03)
    
    def process_frame_for_faces(self, frame):
        """
        Process frame for face detection and recognition
        
        FIXED: 
        - Display boxes: TIGHT around face (x1, y1, x2, y2)
        - Crop for recognizer: PADDED for better recognition (x1_padded, etc.)
        
        This gives you small, clean boxes while sending good crops to the model!
        """
        if not FACE_RECOGNITION_AVAILABLE or self.detector is None:
            # OpenCV fallback
            return self._opencv_fallback_detection(frame)
        
        try:
            # Use BlazeFace detector - returns clean [(x1, y1, x2, y2), ...] format
            detections = self.detector.detect(frame)
            
            if detections and len(detections) > 0:
                for bbox in detections:
                    # Clean unpack - TIGHT coordinates from detector
                    x1, y1, x2, y2 = bbox
                    
                    # ============================================================
                    # Calculate PADDED coordinates for crop (better recognition)
                    # ============================================================
                    width = x2 - x1
                    height = y2 - y1
                    pad_x = int(width * self.face_padding_percent)
                    pad_y = int(height * self.face_padding_percent)
                    
                    # Apply padding with boundary checks
                    frame_h, frame_w = frame.shape[:2]
                    x1_padded = max(0, x1 - pad_x)
                    y1_padded = max(0, y1 - pad_y)
                    x2_padded = min(frame_w, x2 + pad_x)
                    y2_padded = min(frame_h, y2 + pad_y)
                    
                    # ============================================================
                    # Extract face with PADDING (for recognizer)
                    # ============================================================
                    if y2 > y1 and x2 > x1 and y2_padded > y1_padded and x2_padded > x1_padded:
                        # Crop with padding - gives recognizer more context
                        face_img = frame[y1_padded:y2_padded, x1_padded:x2_padded]
                        
                        # ============================================================
                        # Draw boxes using TIGHT coordinates (x1, y1, x2, y2)
                        # This makes boxes small and close to the face!
                        # ============================================================
                        
                        # Draw initial detection box (yellow) - TIGHT around face
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
                        
                        # Try recognition if available
                        if self.recognition_active and self.recognizer and self.recognizer.model_available:
                            try:
                                result = self.recognizer.recognize_with_details(face_img)
                                
                                is_mrdavid = result['is_mrdavid']
                                confidence = result['confidence']
                                label = result['label']
                                
                                if is_mrdavid:
                                    # ============================================================
                                    # Mr. David recognized - GREEN box TIGHT around face
                                    # ============================================================
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                                    cv2.putText(frame, "Welcome Mr. David!", (x1, y1-15),
                                              cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
                                    cv2.putText(frame, f"{confidence:.0%}", (x1, y2+25),
                                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                                    
                                    self.root.after(0, lambda: self.face_status.config(
                                        text="Status: Mr. David Recognized! ✓", foreground="green"))
                                    self.root.after(0, lambda c=confidence: self.recognition_result.config(
                                        text=f"✓ Welcome Mr. David ({c:.0%})", foreground="green"))
                                    
                                    # Trigger greeting
                                    if self._last_recognized_person != "Mr. David":
                                        self._last_recognized_person = "Mr. David"
                                        self.root.after(0, self.execute_greeting_action)
                                else:
                                    # ============================================================
                                    # Unrecognized person - RED box TIGHT around face
                                    # ============================================================
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                                    cv2.putText(frame, "Unrecognized Person", (x1, y1-15),
                                              cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                                    cv2.putText(frame, f"{confidence:.0%}", (x1, y2+25),
                                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                                    
                                    self.root.after(0, lambda: self.face_status.config(
                                        text="Status: Unrecognized Person", foreground="red"))
                                    self.root.after(0, lambda c=confidence: self.recognition_result.config(
                                        text=f"❌ Unrecognized Person ({c:.0%})", foreground="red"))
                                    
                                    # Trigger message for unrecognized person (NO robot action)
                                    if self._last_recognized_person != "Unknown":
                                        self._last_recognized_person = "Unknown"
                                        self.root.after(0, self.execute_unknown_person_action)
                                    
                            except Exception as rec_err:
                                self.log_message(f"✗ Recognition error: {str(rec_err)}")
                        else:
                            # No recognition - just show detection with TIGHT coords
                            cv2.putText(frame, "Face Detected", (x1, y1-10),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                self.root.after(0, lambda: self.face_status.config(
                    text="Status: Face Detected - Analyzing...", foreground="orange"))
            else:
                self.root.after(0, lambda: self.face_status.config(
                    text="Status: Scanning...", foreground="blue"))
                self._last_recognized_person = None
                    
        except Exception as e:
            self.log_message(f"✗ Detection error: {str(e)}")
            import traceback
            self.log_message(traceback.format_exc())
        
        return frame
        
    def _opencv_fallback_detection(self, frame):
        """OpenCV Haar Cascade fallback detection"""
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                if self.recognition_active:
                    cv2.putText(frame, "Welcome Mr. David", (x, y-15),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                    
                    self.root.after(0, lambda: self.face_status.config(
                        text="Status: Face Detected ✓", foreground="green"))
                    self.root.after(0, lambda: self.recognition_result.config(
                        text="✓ Welcome!"))
                    
                    if self._last_recognized_person != "Mr. David":
                        self._last_recognized_person = "Mr. David"
                        self.root.after(0, self.execute_greeting_action)
                else:
                    cv2.putText(frame, "Face Detected", (x, y-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            if len(faces) == 0:
                self.root.after(0, lambda: self.face_status.config(
                    text="Status: Scanning...", foreground="orange"))
                self._last_recognized_person = None
                    
        except Exception as e:
            self.log_message(f"✗ OpenCV detection error: {str(e)}")
        
        return frame
    
    def execute_greeting_action(self):
        """Execute robot greeting when Mr. David is recognized"""
        # Cooldown check (5 seconds)
        current_time = time.time()
        if current_time - self._last_greeting_time < 5:
            return
        
        if self._greeting_in_progress:
            return
        
        if not self.is_connected:
            self.log_message("⚠ Cannot greet - not connected to STM32")
            return
        
        self._greeting_in_progress = True
        self._last_greeting_time = current_time
        
        def greeting():
            try:
                self.log_message("🎉 GREETING MR. DAVID!")
                
                # Step 1: Color flash (Green acknowledgment)
                self.log_message("Step 1: Green acknowledgment...")
                for motor in range(1, 17):
                    self.set_motor_color(motor, "REDGREEN")
                time.sleep(0.5)
                
                # Step 2: Wave motion
                self.log_message("Step 2: Welcoming wave...")
                wave_motors = [5, 6, 7, 8, 9, 10, 11, 12]
                wave_sequence = [20, 20, 0, 0, 0, -20, 0, 0]
                
                for angle in wave_sequence:
                    for motor in wave_motors:
                        angle_str = str(angle)
                        if motor in self.angle_protocols and angle_str in self.angle_protocols[motor]:
                            cmd = self.angle_protocols[motor][angle_str]
                            self.send_hex_command(cmd, f"Wave M{motor}→{angle}°")
                        self.current_angles[motor] = angle
                        self.root.after(0, lambda m=motor: self.update_motor_display(m))
                    time.sleep(0.3)
                
                # Step 3: Return to neutral
                self.log_message("Step 3: Returning to neutral...")
                for motor in range(1, 17):
                    if motor in self.angle_protocols and "0" in self.angle_protocols[motor]:
                        cmd = self.angle_protocols[motor]["0"]
                        self.send_hex_command(cmd, f"Reset M{motor}→0°")
                    self.current_angles[motor] = 0
                    self.root.after(0, lambda m=motor: self.update_motor_display(m))
                    time.sleep(0.02)
                
                self.log_message("✅ GREETING COMPLETED!")
                
            except Exception as e:
                self.log_message(f"✗ Greeting error: {str(e)}")
            finally:
                self._greeting_in_progress = False
        
        threading.Thread(target=greeting, daemon=True).start()
    
    def execute_unknown_person_action(self):
        """Execute action when unrecognized person is detected"""
        # Cooldown check (3 seconds - shorter than greeting)
        current_time = time.time()
        if current_time - self._last_greeting_time < 3:
            return
        
        self._last_greeting_time = current_time
        
        # Log the event
        self.log_message("⚠️ UNRECOGNIZED PERSON DETECTED!")
        self.log_message("   Message: Please register to our application")
        
        # Display message in recognition result
        self.root.after(0, lambda: self.recognition_result.config(
            text="❌ Sorry, we have not seen your face before.\nPlease register to our application.",
            foreground="red"))
        
        # NO ROBOT ACTION - Just stay still
        # Robot does not move for unrecognized people
        
        # Optional: Set all motors to neutral position (commented out by default)
        # Uncomment below if you want robot to go to neutral when unknown person detected
        '''
        if self.is_connected:
            def stay_neutral():
                try:
                    self.log_message("Robot staying in neutral position...")
                    for motor in range(1, 17):
                        if motor in self.angle_protocols and "0" in self.angle_protocols[motor]:
                            cmd = self.angle_protocols[motor]["0"]
                            self.send_hex_command(cmd, f"Neutral M{motor}")
                        self.current_angles[motor] = 0
                        time.sleep(0.02)
                except Exception as e:
                    self.log_message(f"✗ Error: {str(e)}")
            
            threading.Thread(target=stay_neutral, daemon=True).start()
        '''
    
    # ===== UTILITY FUNCTIONS =====
    
    def log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def clear_log(self):
        """Clear the activity log"""
        self.log_text.delete(1.0, tk.END)
    
    def on_closing(self):
        """Handle window closing"""
        if self.camera_running:
            self.stop_detection_scanning()
        
        if self.is_connected:
            self.disconnect_serial()
        
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    
    # Configure styles
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure("Accent.TButton", 
                   foreground="white", 
                   background="#339AF0",
                   font=("Arial", 10, "bold"))
    
    # Create application
    app = HumanoidRobotGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
