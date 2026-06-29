#!/usr/bin/env python3
"""
Servo Control Module
Manages RGB servo motor control via UART communication with STM32F103
FIXED VERSION - Fully compatible with main.py and face recognition system
"""

import serial
import time
import logging
import threading


class ServoController:
    """Controls 16 RGB servo motors via UART to STM32F103"""
    
    def __init__(self, port="/dev/ttyAMA0", baudrate=115200):
        """
        Initialize servo controller
        
        Args:
            port: UART device path (default: /dev/ttyAMA0 for Raspberry Pi)
            baudrate: Communication baud rate (default: 115200)
        """
        self.logger = logging.getLogger(__name__)
        self.port = port
        self.baudrate = baudrate
        self.serial_port = None
        self.is_connected = False
        
        # Threading lock for serial communication (required by main.py)
        self.serial_lock = threading.Lock()
        
        # Current states for motors (1-16)
        self.current_angles = {i: 0 for i in range(1, 17)}
        self.current_colors = {i: "RGBMIX" for i in range(1, 17)}
        
        # RGB Color protocols - COMPATIBLE WITH MAIN.PY
        # Colors: RGBMIX (Red), REDGREEN (Green), GREENBLUE (Blue)
        self.rgb_protocols = {
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
        
        # KEEP ORIGINAL RGB PROTOCOLS FOR BACKWARD COMPATIBILITY
        # Alias: RED → RGBMIX, GREEN → REDGREEN, BLUE → GREENBLUE
        for motor in range(1, 17):
            self.rgb_protocols[motor]["RED"] = self.rgb_protocols[motor]["RGBMIX"]
            self.rgb_protocols[motor]["GREEN"] = self.rgb_protocols[motor]["REDGREEN"]
            self.rgb_protocols[motor]["BLUE"] = self.rgb_protocols[motor]["GREENBLUE"]
        
        # Angle protocols - EXPANDED WITH MORE ANGLES
        self.angle_protocols = self._load_angle_protocols()
        
        self.logger.info("ServoController initialized (compatible with main.py)")
    
    def _load_angle_protocols(self):
        """Load comprehensive angle protocols for motors 1-16"""
        protocols = {}
        
        # MOTOR 1 - Complete set (from original + new angles)
        protocols[1] = {
            "-160": "FFFF010A0E000003E8FE",
            "-90": "FFFF010A0E040003E8FA",
            "-45": "FFFF010A0E060003E8F8",
            "0": "FFFF010A0E080003E8F6",
            "5": "FFFF010A0E084003E8B6",
            "10": "FFFF010A0E088003E876",
            "15": "FFFF010A0E08C003E836",
            "20": "FFFF010A0E090003E8F5",
            "45": "FFFF010A0E0A0003E8F4",
            "90": "FFFF010A0E0C0003E8F2",
            "160": "FFFF010A0E100003E8EE"
        }
        
        # MOTOR 2 - Extended angles
        protocols[2] = {
            "-160": "FFFF020A0E000003E8FD",
            "-90": "FFFF020A0E040003E8F9",
            "-45": "FFFF020A0E060003E8F7",
            "0": "FFFF020A0E080003E8F5",
            "20": "FFFF020A0E090003E8F4",
            "45": "FFFF020A0E0A0003E8F3",
            "90": "FFFF020A0E0C0003E8F1",
            "160": "FFFF020A0E100003E8ED"
        }
        
        # MOTOR 3 - Extended angles
        protocols[3] = {
            "-160": "FFFF030A0E000003E8FC",
            "-90": "FFFF030A0E040003E8F8",
            "-45": "FFFF030A0E060003E8F6",
            "0": "FFFF030A0E080003E8F4",
            "20": "FFFF030A0E090003E8F3",
            "45": "FFFF030A0E0A0003E8F2",
            "90": "FFFF030A0E0C0003E8F0",
            "160": "FFFF030A0E100003E8EC"
        }
        
        # MOTOR 4 - Extended angles
        protocols[4] = {
            "-160": "FFFF040A0E000003E8FB",
            "-90": "FFFF040A0E040003E8F7",
            "-45": "FFFF040A0E060003E8F5",
            "0": "FFFF040A0E080003E8F3",
            "20": "FFFF040A0E090003E8F2",
            "45": "FFFF040A0E0A0003E8F1",
            "90": "FFFF040A0E0C0003E8EF",
            "160": "FFFF040A0E100003E8EB"
        }
        
        # MOTOR 5 - Extended angles
        protocols[5] = {
            "-160": "FFFF050A0E000003E8FA",
            "-90": "FFFF050A0E040003E8F6",
            "-45": "FFFF050A0E060003E8F4",
            "0": "FFFF050A0E080003E8F2",
            "20": "FFFF050A0E090003E8F1",
            "45": "FFFF050A0E0A0003E8F0",
            "90": "FFFF050A0E0C0003E8EE",
            "160": "FFFF050A0E100003E8EA"
        }
        
        # MOTOR 6 - Extended angles
        protocols[6] = {
            "-160": "FFFF060A0E000003E8F9",
            "-90": "FFFF060A0E040003E8F5",
            "-45": "FFFF060A0E060003E8F3",
            "0": "FFFF060A0E080003E8F1",
            "20": "FFFF060A0E090003E8F0",
            "45": "FFFF060A0E0A0003E8EF",
            "90": "FFFF060A0E0C0003E8ED",
            "160": "FFFF060A0E100003E8E9"
        }
        
        # MOTOR 7 - Extended angles
        protocols[7] = {
            "-160": "FFFF070A0E000003E8F8",
            "-90": "FFFF070A0E040003E8F4",
            "-45": "FFFF070A0E060003E8F2",
            "0": "FFFF070A0E080003E8F0",
            "20": "FFFF070A0E090003E8EF",
            "45": "FFFF070A0E0A0003E8EE",
            "90": "FFFF070A0E0C0003E8EC",
            "160": "FFFF070A0E100003E8E8"
        }
        
        # MOTOR 8 - Extended angles
        protocols[8] = {
            "-160": "FFFF080A0E000003E8F7",
            "-90": "FFFF080A0E040003E8F3",
            "-45": "FFFF080A0E060003E8F1",
            "0": "FFFF080A0E080003E8EF",
            "20": "FFFF080A0E090003E8EE",
            "45": "FFFF080A0E0A0003E8ED",
            "90": "FFFF080A0E0C0003E8EB",
            "160": "FFFF080A0E100003E8E7"
        }
        
        # MOTOR 9 - Extended angles
        protocols[9] = {
            "-160": "FFFF090A0E000003E8F6",
            "-90": "FFFF090A0E040003E8F2",
            "-45": "FFFF090A0E060003E8F0",
            "0": "FFFF090A0E080003E8EE",
            "20": "FFFF090A0E090003E8ED",
            "45": "FFFF090A0E0A0003E8EC",
            "90": "FFFF090A0E0C0003E8EA",
            "160": "FFFF090A0E100003E8E6"
        }
        
        # MOTOR 10 - Extended angles
        protocols[10] = {
            "-160": "FFFF0A0A0E000003E8F5",
            "-90": "FFFF0A0A0E040003E8F1",
            "-45": "FFFF0A0A0E060003E8EF",
            "0": "FFFF0A0A0E080003E8ED",
            "20": "FFFF0A0A0E090003E8EC",
            "45": "FFFF0A0A0E0A0003E8EB",
            "90": "FFFF0A0A0E0C0003E8E9",
            "160": "FFFF0A0A0E100003E8E5"
        }
        
        # MOTOR 11 - Extended angles
        protocols[11] = {
            "-160": "FFFF0B0A0E000003E8F4",
            "-90": "FFFF0B0A0E040003E8F0",
            "-45": "FFFF0B0A0E060003E8EE",
            "0": "FFFF0B0A0E080003E8EC",
            "20": "FFFF0B0A0E090003E8EB",
            "45": "FFFF0B0A0E0A0003E8EA",
            "90": "FFFF0B0A0E0C0003E8E8",
            "160": "FFFF0B0A0E100003E8E4"
        }
        
        # MOTOR 12 - Extended angles
        protocols[12] = {
            "-160": "FFFF0C0A0E000003E8F3",
            "-90": "FFFF0C0A0E040003E8EF",
            "-45": "FFFF0C0A0E060003E8ED",
            "0": "FFFF0C0A0E080003E8EB",
            "20": "FFFF0C0A0E090003E8EA",
            "45": "FFFF0C0A0E0A0003E8E9",
            "90": "FFFF0C0A0E0C0003E8E7",
            "160": "FFFF0C0A0E100003E8E3"
        }
        
        # MOTOR 13 - Extended angles
        protocols[13] = {
            "-160": "FFFF0D0A0E000003E8F2",
            "-90": "FFFF0D0A0E040003E8EE",
            "-45": "FFFF0D0A0E060003E8EC",
            "0": "FFFF0D0A0E080003E8EA",
            "20": "FFFF0D0A0E090003E8E9",
            "45": "FFFF0D0A0E0A0003E8E8",
            "90": "FFFF0D0A0E0C0003E8E6",
            "160": "FFFF0D0A0E100003E8E2"
        }
        
        # MOTOR 14 - Extended angles
        protocols[14] = {
            "-160": "FFFF0E0A0E000003E8F1",
            "-90": "FFFF0E0A0E040003E8ED",
            "-45": "FFFF0E0A0E060003E8EB",
            "0": "FFFF0E0A0E080003E8E9",
            "20": "FFFF0E0A0E090003E8E8",
            "45": "FFFF0E0A0E0A0003E8E7",
            "90": "FFFF0E0A0E0C0003E8E5",
            "160": "FFFF0E0A0E100003E8E1"
        }
        
        # MOTOR 15 - Extended angles
        protocols[15] = {
            "-160": "FFFF0F0A0E000003E8F0",
            "-90": "FFFF0F0A0E040003E8EC",
            "-45": "FFFF0F0A0E060003E8EA",
            "0": "FFFF0F0A0E080003E8E8",
            "20": "FFFF0F0A0E090003E8E7",
            "45": "FFFF0F0A0E0A0003E8E6",
            "90": "FFFF0F0A0E0C0003E8E4",
            "160": "FFFF0F0A0E100003E8E0"
        }
        
        # MOTOR 16 - Extended angles
        protocols[16] = {
            "-160": "FFFF100A0E000003E8EF",
            "-90": "FFFF100A0E040003E8EB",
            "-45": "FFFF100A0E060003E8E9",
            "0": "FFFF100A0E080003E8E7",
            "20": "FFFF100A0E090003E8E6",
            "45": "FFFF100A0E0A0003E8E5",
            "90": "FFFF100A0E0C0003E8E3",
            "160": "FFFF100A0E100003E8DF"
        }
        
        return protocols
    
    def connect(self):
        """Connect to UART serial port"""
        try:
            self.logger.info(f"Connecting to {self.port} at {self.baudrate} baud...")
            
            self.serial_port = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            
            time.sleep(0.5)  # Wait for connection to stabilize
            
            self.is_connected = True
            self.logger.info(f"✓ Connected to {self.port}")
            return True
            
        except serial.SerialException as e:
            self.logger.error(f"✗ Connection failed: {str(e)}")
            self.logger.error(f"  Make sure UART is enabled: sudo raspi-config")
            self.logger.error(f"  Check port exists: ls {self.port}")
            self.logger.error(f"  Alternative ports: /dev/serial0, /dev/ttyUSB0, /dev/ttyACM0")
            return False
        except Exception as e:
            self.logger.error(f"✗ Unexpected error: {str(e)}")
            return False
    
    def disconnect(self):
        """Disconnect from serial port"""
        try:
            if self.serial_port and self.is_connected:
                with self.serial_lock:
                    self.serial_port.close()
                self.is_connected = False
                self.logger.info("Disconnected from UART")
        except Exception as e:
            self.logger.error(f"Disconnect error: {str(e)}")
    
    def send_hex_command(self, hex_string, description=""):
        """
        Send hex command to serial port
        
        Args:
            hex_string: Hex command string
            description: Optional description for logging
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected or not self.serial_port:
            self.logger.warning("Not connected to UART")
            return False
        
        try:
            with self.serial_lock:
                hex_bytes = bytes.fromhex(hex_string)
                self.serial_port.write(hex_bytes)
                self.serial_port.flush()
                
                if description:
                    self.logger.debug(f"→ {description}: {hex_string}")
                
                time.sleep(0.02)  # Small delay between commands
            return True
            
        except ValueError as e:
            self.logger.error(f"✗ Invalid hex string: {hex_string}")
            return False
        except Exception as e:
            self.logger.error(f"✗ Send error: {str(e)}")
            return False
    
    def send_batch_commands(self, commands, delay=0.001):
        """
        Send multiple commands with delays
        
        Args:
            commands: List of hex command strings
            delay: Delay between commands in seconds
            
        Returns:
            True if all successful, False if any failed
        """
        if not self.is_connected or not self.serial_port:
            self.logger.warning("Not connected to UART")
            return False
        
        try:
            with self.serial_lock:
                for hex_string in commands:
                    hex_bytes = bytes.fromhex(hex_string)
                    self.serial_port.write(hex_bytes)
                    time.sleep(delay)
                self.serial_port.flush()
            return True
            
        except Exception as e:
            self.logger.error(f"✗ Batch send error: {str(e)}")
            return False
    
    def set_motor_color(self, motor_num, color):
        """
        Set motor RGB color
        
        Args:
            motor_num: Motor number (1-16)
            color: Color name (RGBMIX/RED, REDGREEN/GREEN, GREENBLUE/BLUE)
            
        Returns:
            True if successful, False otherwise
        """
        if motor_num not in self.rgb_protocols:
            self.logger.warning(f"Motor {motor_num} not found (valid: 1-16)")
            return False
        
        if color not in self.rgb_protocols[motor_num]:
            self.logger.warning(f"Color {color} not available")
            self.logger.info(f"Available colors: RGBMIX, REDGREEN, GREENBLUE (or RED, GREEN, BLUE)")
            return False
        
        hex_cmd = self.rgb_protocols[motor_num][color]
        
        if self.send_hex_command(hex_cmd, f"Motor {motor_num} → {color}"):
            self.current_colors[motor_num] = color
            return True
        
        return False
    
    def set_motor_angle(self, motor_num, angle):
        """
        Set motor angle
        
        Args:
            motor_num: Motor number (1-16)
            angle: Angle in degrees (-160 to 160)
            
        Returns:
            True if successful, False otherwise
        """
        angle_str = str(angle)
        
        if motor_num not in self.angle_protocols:
            self.logger.warning(f"Motor {motor_num} angle protocols not loaded")
            return False
        
        if angle_str not in self.angle_protocols[motor_num]:
            # Find nearest available angle
            available_angles = [int(a) for a in self.angle_protocols[motor_num].keys()]
            nearest_angle = min(available_angles, key=lambda x: abs(x - angle))
            
            self.logger.warning(f"Angle {angle}° not available for Motor {motor_num}")
            self.logger.info(f"Using nearest angle: {nearest_angle}°")
            self.logger.info(f"Available angles: {sorted(available_angles)}")
            
            angle = nearest_angle
            angle_str = str(angle)
        
        hex_cmd = self.angle_protocols[motor_num][angle_str]
        
        if self.send_hex_command(hex_cmd, f"Motor {motor_num} → {angle}°"):
            self.current_angles[motor_num] = angle
            return True
        
        return False
    
    def set_all_colors(self, color):
        """
        Set all motors to same color
        
        Args:
            color: Color name (RGBMIX, REDGREEN, GREENBLUE)
            
        Returns:
            True if successful, False otherwise
        """
        commands = []
        
        for motor_num in range(1, 17):
            if motor_num in self.rgb_protocols and color in self.rgb_protocols[motor_num]:
                hex_cmd = self.rgb_protocols[motor_num][color]
                commands.append(hex_cmd)
                self.current_colors[motor_num] = color
        
        result = self.send_batch_commands(commands)
        
        if result:
            self.logger.info(f"All motors → {color}")
        
        return result
    
    def set_all_angles(self, angle):
        """
        Set all motors to same angle
        
        Args:
            angle: Angle in degrees
            
        Returns:
            True if successful, False otherwise
        """
        angle_str = str(angle)
        commands = []
        
        for motor_num in range(1, 17):
            if motor_num in self.angle_protocols and angle_str in self.angle_protocols[motor_num]:
                hex_cmd = self.angle_protocols[motor_num][angle_str]
                commands.append(hex_cmd)
                self.current_angles[motor_num] = angle
        
        result = self.send_batch_commands(commands)
        
        if result:
            self.logger.info(f"All motors → {angle}°")
        
        return result
    
    def reset_all_servos(self):
        """Reset all servos to 0° and RGBMIX color"""
        self.logger.info("Resetting all servos...")
        self.set_all_colors("RGBMIX")
        time.sleep(0.5)
        self.set_all_angles(0)
        self.logger.info("✓ All servos reset complete")
    
    def execute_greeting(self):
        """
        Execute greeting sequence when Mr. David is detected
        COMPATIBLE WITH MAIN.PY
        
        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected:
            self.logger.error("Cannot execute greeting - not connected")
            return False
        
        try:
            self.logger.info("🎉 Executing greeting sequence for Mr. David...")
            
            # Step 1: Color flash acknowledgment (0.2s each)
            self.logger.info("Step 1: Color flash acknowledgment...")
            colors = ["RGBMIX", "GREENBLUE", "REDGREEN"]
            for color in colors:
                self.set_all_colors(color)
                time.sleep(0.2)
            
            # Step 2: All GREEN
            self.logger.info("Step 2: Setting all motors to GREEN...")
            self.set_all_colors("REDGREEN")
            time.sleep(0.5)
            
            # Step 3: Wave motion (motors 5-12, upper body)
            self.logger.info("Step 3: Wave motion (motors 5-12)...")
            wave_motors = [5, 6, 7, 8, 9, 10, 11, 12]
            wave_sequence = [0, 45, 90, 45, 0, -45, 0]
            
            for angle in wave_sequence:
                for motor in wave_motors:
                    self.set_motor_angle(motor, angle)
                time.sleep(0.4)
            
            # Step 4: Color celebration (2 cycles)
            self.logger.info("Step 4: Color celebration...")
            for _ in range(2):
                for color in colors:
                    self.set_all_colors(color)
                    time.sleep(0.3)
            
            # Step 5: Return to neutral
            self.logger.info("Step 5: Returning to neutral position...")
            self.set_all_angles(0)
            time.sleep(0.3)
            self.set_all_colors("REDGREEN")
            
            self.logger.info("✅ Greeting sequence complete!")
            return True
            
        except Exception as e:
            self.logger.error(f"✗ Greeting sequence error: {str(e)}")
            return False
    
    def rainbow_wave(self, cycles=2):
        """
        Execute rainbow wave pattern (from main.py)
        
        Args:
            cycles: Number of cycles to repeat
        """
        self.logger.info("🌈 Starting rainbow wave...")
        colors = ["RGBMIX", "REDGREEN", "GREENBLUE"]
        
        for cycle in range(cycles):
            for offset in range(3):
                for i in range(16):
                    motor = i + 1
                    color = colors[(i + offset) % 3]
                    self.set_motor_color(motor, color)
                time.sleep(0.5)
        
        self.logger.info("✓ Rainbow wave complete")
    
    def wave_motion(self, repetitions=2):
        """
        Execute wave motion pattern (from main.py)
        
        Args:
            repetitions: Number of times to repeat
        """
        self.logger.info("↕️ Starting wave motion...")
        angles = [-45, 0, 45, 0]
        
        for _ in range(repetitions):
            for angle in angles:
                self.set_all_angles(angle)
                time.sleep(0.4)
        
        self.set_all_angles(0)
        self.logger.info("✓ Wave motion complete")
    
    def get_motor_state(self, motor_num):
        """
        Get current state of a motor
        
        Args:
            motor_num: Motor number (1-16)
            
        Returns:
            Dictionary with angle and color
        """
        if motor_num not in range(1, 17):
            return None
        
        return {
            'motor': motor_num,
            'angle': self.current_angles.get(motor_num, 0),
            'color': self.current_colors.get(motor_num, 'RGBMIX')
        }
    
    def get_all_states(self):
        """
        Get current state of all motors
        
        Returns:
            Dictionary with all motor states
        """
        return {
            'angles': self.current_angles.copy(),
            'colors': self.current_colors.copy(),
            'connected': self.is_connected
        }
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
    
    def __del__(self):
        """Destructor - ensure cleanup"""
        try:
            self.disconnect()
        except:
            pass


# Test code
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 70)
    print("Servo Controller - Test Mode")
    print("=" * 70)
    print("\n🤖 RGB Servo Motor Control Module")
    print("\n📌 Features:")
    print("  ✓ Controls 16 RGB servo motors")
    print("  ✓ UART communication (115200 baud)")
    print("  ✓ Thread-safe operation")
    print("  ✓ Compatible with main.py")
    print("  ✓ Face recognition integration")
    print("\n🎨 Available Colors:")
    print("  • RGBMIX (Red) / RED")
    print("  • REDGREEN (Green) / GREEN")
    print("  • GREENBLUE (Blue) / BLUE")
    print("\n📐 Available Angles:")
    print("  -160°, -90°, -45°, 0°, 20°, 45°, 90°, 160°")
    print("\n🎭 Actions:")
    print("  • execute_greeting() - Welcome Mr. David")
    print("  • rainbow_wave() - Rainbow color pattern")
    print("  • wave_motion() - Wave motion pattern")
    print("  • reset_all_servos() - Reset to default")
    print("\n📡 UART Configuration:")
    print(f"  Port: /dev/ttyAMA0 (configurable)")
    print(f"  Baudrate: 115200")
    print(f"  Alternative ports: /dev/serial0, /dev/ttyUSB0")
    print("\n🔧 Setup Requirements:")
    print("  1. Enable UART: sudo raspi-config")
    print("  2. Connect STM32F103 to Raspberry Pi UART")
    print("  3. Add user to dialout: sudo usermod -a -G dialout $USER")
    print("  4. Check port: ls /dev/ttyAMA* /dev/serial*")
    print("\n💡 Usage Example:")
    print("  from servo_control import ServoController")
    print("  controller = ServoController()")
    print("  controller.connect()")
    print("  controller.set_motor_color(1, 'REDGREEN')")
    print("  controller.set_motor_angle(1, 45)")
    print("  controller.execute_greeting()")
    print("  controller.disconnect()")
    print("\n" + "=" * 70)
    print("✅ Servo controller module ready!")
    print("=" * 70)
