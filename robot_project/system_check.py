#!/usr/bin/env python3
"""
Complete System Check for Face Recognition Robot
Tests all components and validates bbox format
"""

import sys
import os

print("=" * 70)
print("FACE RECOGNITION ROBOT - SYSTEM CHECK")
print("=" * 70)
print()

errors = []
warnings = []

# Test 1: Python version
print("Test 1: Python Version")
import sys
version = sys.version_info
print(f"  Python {version.major}.{version.minor}.{version.micro}")
if version.major < 3 or (version.major == 3 and version.minor < 9):
    errors.append("Python 3.9+ required")
else:
    print("  ✓ Python version OK")
print()

# Test 2: Required modules
print("Test 2: Required Python Modules")
required_modules = {
    'cv2': 'OpenCV',
    'numpy': 'NumPy',
    'PIL': 'PIL/Pillow',
    'serial': 'PySerial',
    'tkinter': 'Tkinter'
}

for module, name in required_modules.items():
    try:
        __import__(module)
        print(f"  ✓ {name}")
    except ImportError:
        print(f"  ✗ {name} NOT FOUND")
        errors.append(f"{name} not installed")

# Special check for ImageTk
try:
    from PIL import ImageTk
    print(f"  ✓ PIL ImageTk")
except ImportError:
    print(f"  ✗ PIL ImageTk NOT FOUND")
    errors.append("PIL ImageTk not installed (install: sudo apt install python3-pil.imagetk)")

print()

# Test 3: Face recognition modules
print("Test 3: Face Recognition Modules")
try:
    from blazeface_detector import BlazeFaceDetector
    print("  ✓ blazeface_detector.py")
except ImportError as e:
    print(f"  ✗ blazeface_detector.py: {e}")
    errors.append("blazeface_detector.py missing or has errors")

try:
    from tinycnn_recognizer import TinyCNNRecognizer
    print("  ✓ tinycnn_recognizer.py")
except ImportError as e:
    print(f"  ✗ tinycnn_recognizer.py: {e}")
    warnings.append("tinycnn_recognizer.py missing (recognition won't work)")

try:
    from servo_control import ServoController
    print("  ✓ servo_control.py")
except ImportError as e:
    print(f"  ✗ servo_control.py: {e}")
    warnings.append("servo_control.py missing (servo control won't work)")

print()

# Test 4: Required files
print("Test 4: Required Files")
required_files = ['main.py', 'blazeface_detector.py', 'tinycnn_recognizer.py', 'servo_control.py']
for file in required_files:
    if os.path.exists(file):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} NOT FOUND")
        errors.append(f"{file} missing")

print()

# Test 5: Directories
print("Test 5: Required Directories")
required_dirs = ['models', 'logs']
for dir_name in required_dirs:
    if os.path.exists(dir_name):
        print(f"  ✓ {dir_name}/")
    else:
        print(f"  ⚠ {dir_name}/ NOT FOUND (will be created)")
        try:
            os.makedirs(dir_name, exist_ok=True)
            print(f"    Created {dir_name}/")
        except Exception as e:
            warnings.append(f"Could not create {dir_name}: {e}")

print()

# Test 6: Models
print("Test 6: model Files")
if os.path.exists('models/blazeface.tflite'):
    print("  ✓ models/blazeface.tflite")
else:
    print("  ⚠ models/blazeface.tflite NOT FOUND (will auto-download)")
    warnings.append("BlazeFace model will be downloaded on first run")

if os.path.exists('models/tinycnn_mrdavid.tflite'):
    print("  ✓ models/tinycnn_mrdavid.tflite")
else:
    print("  ⚠ models/tinycnn_mrdavid.tflite NOT FOUND")
    warnings.append("TinyCNN model missing - recognition won't work. Train model first.")

print()

# Test 7: BBox format validation
print("Test 7: BBox Format Validation")
try:
    import cv2
    import numpy as np
    from blazeface_detector import BlazeFaceDetector
    
    # Create test image
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Create detector
    detector = BlazeFaceDetector(
        model_path="models/blazeface.tflite",
        confidence_threshold=0.7
    )
    
    # Run detection
    detections = detector.detect(test_image)
    
    # Validate format
    if not isinstance(detections, list):
        print(f"  ✗ Detections is not a list: {type(detections)}")
        errors.append("BBox format invalid")
    else:
        print(f"  ✓ Detections is a list")
        
        bbox_ok = True
        for idx, bbox in enumerate(detections):
            if not isinstance(bbox, (tuple, list)):
                print(f"  ✗ Bbox {idx} is not tuple/list: {type(bbox)}")
                bbox_ok = False
            elif len(bbox) != 4:
                print(f"  ✗ Bbox {idx} length != 4: {len(bbox)}")
                bbox_ok = False
            else:
                try:
                    x1, y1, x2, y2 = bbox
                    print(f"  ✓ Bbox {idx} format OK: ({x1}, {y1}, {x2}, {y2})")
                except:
                    print(f"  ✗ Bbox {idx} cannot unpack")
                    bbox_ok = False
        
        if bbox_ok:
            print("  ✓ BBox format validation PASSED")
        else:
            errors.append("BBox format validation failed")
            
except Exception as e:
    print(f"  ✗ BBox validation error: {str(e)}")
    errors.append(f"BBox validation failed: {e}")

print()

# Test 8: Camera
print("Test 8: Camera Availability")
try:
    import cv2
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("  ✓ Camera found at /dev/video0")
        cap.release()
    else:
        print("  ⚠ Camera not available")
        warnings.append("Camera not found - face detection won't work")
except Exception as e:
    print(f"  ⚠ Camera test failed: {e}")
    warnings.append("Could not test camera")

print()

# Test 9: UART
print("Test 9: UART Ports")
uart_found = False
for port in ['/dev/ttyAMA0', '/dev/serial0', '/dev/ttyUSB0', '/dev/ttyACM0']:
    if os.path.exists(port):
        print(f"  ✓ {port} found")
        uart_found = True

if not uart_found:
    print("  ⚠ No UART ports found")
    warnings.append("UART not found - servo control won't work. Enable UART in raspi-config")

print()

# Summary
print("=" * 70)
print("SUMMARY")
print("=" * 70)

if len(errors) == 0:
    print("✅ SYSTEM CHECK PASSED!")
    print()
    print("Your system is ready to run the face recognition robot!")
    print()
    print("Next steps:")
    print("  1. Run: python3 main.py")
    print("  2. Click 'Connect' to connect to STM32")
    print("  3. Click 'Start Detection' to begin face recognition")
    print()
else:
    print("❌ SYSTEM CHECK FAILED")
    print()
    print("ERRORS (must fix):")
    for i, error in enumerate(errors, 1):
        print(f"  {i}. {error}")
    print()

if len(warnings) > 0:
    print("WARNINGS (optional features may not work):")
    for i, warning in enumerate(warnings, 1):
        print(f"  {i}. {warning}")
    print()

if len(errors) == 0:
    print("=" * 70)
    print("✅ ALL CRITICAL TESTS PASSED - SYSTEM READY!")
    print("=" * 70)
    sys.exit(0)
else:
    print("=" * 70)
    print("❌ PLEASE FIX ERRORS BEFORE RUNNING")
    print("=" * 70)
    sys.exit(1)
