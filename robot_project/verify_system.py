#!/usr/bin/env python3
"""
System Verification Script
Tests all components before running main application
"""

import sys
import os
from pathlib import Path

print("=" * 70)
print("🔍 HUMANOID ROBOT SYSTEM VERIFICATION")
print("=" * 70)
print()

# Test 1: Python version
print("Test 1: Python Version")
print(f"  Version: {sys.version}")
if sys.version_info >= (3, 8):
    print("  ✅ PASS: Python 3.8+")
else:
    print("  ❌ FAIL: Need Python 3.8 or higher")
print()

# Test 2: Required modules
print("Test 2: Required Modules")
required_modules = {
    'numpy': 'NumPy',
    'cv2': 'OpenCV',
    'PIL': 'Pillow',
    'serial': 'PySerial',
    'tkinter': 'Tkinter',
    'sklearn': 'scikit-learn (for training only)'
}

all_passed = True
for module, name in required_modules.items():
    try:
        __import__(module)
        print(f"  ✅ {name}")
    except ImportError:
        if module == 'sklearn':
            print(f"  ⚠️ {name} (optional for training)")
        else:
            print(f"  ❌ {name}")
            all_passed = False
print()

# Test 3: TensorFlow/TFLite
print("Test 3: TensorFlow/TFLite")
tf_available = False
try:
    import tensorflow as tf
    print(f"  ✅ TensorFlow {tf.__version__}")
    tf_available = True
except ImportError:
    try:
        from tflite_runtime.interpreter import Interpreter
        print(f"  ✅ TFLite Runtime")
        tf_available = True
    except ImportError:
        print(f"  ❌ TensorFlow/TFLite not found")
        all_passed = False
print()

# Test 4: Project files
print("Test 4: Project Files")
required_files = [
    'main.py',
    'blazeface_detector.py',
    'tinycnn_recognizer.py',
    'train_model.py'
]

for file in required_files:
    if Path(file).exists():
        print(f"  ✅ {file}")
    else:
        print(f"  ❌ {file}")
        all_passed = False
print()

# Test 5: Models directory
print("Test 5: Models Directory")
models_dir = Path("models")
if models_dir.exists():
    print(f"  ✅ models/ directory exists")
    
    # Check for models
    blazeface = models_dir / "blazeface.tflite"
    tinycnn = models_dir / "tinycnn_mrdavid.tflite"
    
    if blazeface.exists():
        size = blazeface.stat().st_size / 1024
        print(f"  ✅ blazeface.tflite ({size:.1f} KB)")
    else:
        print(f"  ⚠️ blazeface.tflite (will auto-download)")
    
    if tinycnn.exists():
        size = tinycnn.stat().st_size / 1024
        print(f"  ✅ tinycnn_mrdavid.tflite ({size:.1f} KB)")
    else:
        print(f"  ⚠️ tinycnn_mrdavid.tflite (need to train)")
        print(f"     Run: python3 train_model.py")
else:
    print(f"  ⚠️ models/ directory will be created automatically")
print()

# Test 6: Dataset (for training)
print("Test 6: Dataset (for training)")
dataset_dir = Path("dataset")
if dataset_dir.exists():
    mrdavid_dir = dataset_dir / "mrdavid"
    others_dir = dataset_dir / "others"
    
    if mrdavid_dir.exists():
        count = len(list(mrdavid_dir.glob("*.jpg")) + list(mrdavid_dir.glob("*.png")))
        status = "✅" if count >= 100 else "⚠️"
        print(f"  {status} mrdavid/ ({count} images)")
        if count < 100:
            print(f"     Recommend 100+ images for good accuracy")
    else:
        print(f"  ❌ mrdavid/ directory not found")
    
    if others_dir.exists():
        count = len(list(others_dir.glob("*.jpg")) + list(others_dir.glob("*.png")))
        status = "✅" if count >= 100 else "⚠️"
        print(f"  {status} others/ ({count} images)")
        if count < 100:
            print(f"     Recommend 100+ images for good accuracy")
    else:
        print(f"  ❌ others/ directory not found")
else:
    print(f"  ⚠️ dataset/ directory not found (needed for training)")
    print(f"     Create: mkdir -p dataset/mrdavid dataset/others")
print()

# Test 7: Camera
print("Test 7: Camera Access")
try:
    import cv2
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print(f"  ✅ Camera accessible")
        cap.release()
    else:
        print(f"  ❌ Camera not accessible")
        print(f"     Check camera connection and permissions")
except Exception as e:
    print(f"  ❌ Camera test failed: {e}")
print()

# Test 8: Serial ports (optional)
print("Test 8: Serial Ports (optional)")
try:
    import serial.tools.list_ports
    ports = list(serial.tools.list_ports.comports())
    if ports:
        print(f"  ✅ Available ports:")
        for port in ports:
            print(f"     - {port.device}")
    else:
        print(f"  ⚠️ No serial ports found")
        print(f"     This is OK if not using motor control")
except Exception as e:
    print(f"  ⚠️ Serial port check failed: {e}")
print()

# Test 9: Import face recognition modules
print("Test 9: Face Recognition Modules")
try:
    from blazeface_detector import BlazeFaceDetector
    print(f"  ✅ BlazeFaceDetector")
except ImportError as e:
    print(f"  ❌ BlazeFaceDetector: {e}")
    all_passed = False

try:
    from tinycnn_recognizer import TinyCNNRecognizer
    print(f"  ✅ TinyCNNRecognizer")
except ImportError as e:
    print(f"  ❌ TinyCNNRecognizer: {e}")
    all_passed = False
print()

# Summary
print("=" * 70)
print("SUMMARY")
print("=" * 70)

if all_passed and tf_available:
    print("✅ All critical tests passed!")
    print()
    print("You can now:")
    print("  1. Train model: python3 train_model.py")
    print("  2. Run application: python3 main.py")
else:
    print("❌ Some tests failed")
    print()
    print("Please fix the issues above before running the application.")
    print()
    print("Installation help:")
    print("  Windows: pip install -r requirements.txt")
    print("  Raspberry Pi: See README.md for detailed instructions")

print("=" * 70)
