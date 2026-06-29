#!/usr/bin/env python3
"""
BBox Format Validation Test
Tests the BlazeFace detector to ensure it returns correct bbox format
"""

import sys
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("=" * 70)
print("BBox Format Validation Test")
print("=" * 70)
print()

# Test 1: Import test
print("Test 1: Importing modules...")
try:
    import cv2
    import numpy as np
    from blazeface_detector import BlazeFaceDetector
    print("✓ All modules imported successfully")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    print("\nInstall missing packages:")
    print("  pip3 install opencv-python numpy --break-system-packages")
    sys.exit(1)

# Test 2: Create detector
print("\nTest 2: Creating BlazeFace detector...")
try:
    detector = BlazeFaceDetector(
        model_path="models/blazeface.tflite",
        confidence_threshold=0.7
    )
    print("✓ Detector created successfully")
except Exception as e:
    print(f"✗ Detector creation failed: {e}")
    print("\nMake sure models/blazeface.tflite exists")
    print("  model will auto-download on first run")
    sys.exit(1)

# Test 3: Create test image
print("\nTest 3: Creating test image...")
try:
    # Create a 640x480 test image (black)
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    print(f"✓ Test image created: {test_image.shape}")
except Exception as e:
    print(f"✗ Test image creation failed: {e}")
    sys.exit(1)

# Test 4: Run detection
print("\nTest 4: Running face detection...")
try:
    detections = detector.detect(test_image)
    print(f"✓ Detection completed")
    print(f"  Detections: {len(detections)}")
    print(f"  Type: {type(detections)}")
except Exception as e:
    print(f"✗ Detection failed: {e}")
    import traceback
    print(f"  Traceback: {traceback.format_exc()}")
    sys.exit(1)

# Test 5: Validate bbox format
print("\nTest 5: Validating bbox format...")
bbox_valid = True

if not isinstance(detections, list):
    print(f"✗ Detections is not a list: {type(detections)}")
    bbox_valid = False
else:
    print(f"✓ Detections is a list")
    
    for idx, bbox in enumerate(detections):
        print(f"\n  Checking bbox {idx}:")
        
        # Check type
        if not isinstance(bbox, (tuple, list)):
            print(f"    ✗ Not a tuple/list: {type(bbox)}")
            bbox_valid = False
            continue
        else:
            print(f"    ✓ Type: {type(bbox)}")
        
        # Check length
        if len(bbox) != 4:
            print(f"    ✗ Wrong length: expected 4, got {len(bbox)}")
            print(f"    ✗ Content: {bbox}")
            bbox_valid = False
            continue
        else:
            print(f"    ✓ Length: 4")
        
        # Check values
        try:
            x1, y1, x2, y2 = bbox
            print(f"    ✓ Unpacking: ({x1}, {y1}, {x2}, {y2})")
            
            # Check coordinate validity
            if x2 <= x1 or y2 <= y1:
                print(f"    ⚠ Invalid coordinates: x2={x2} <= x1={x1} or y2={y2} <= y1={y1}")
            else:
                print(f"    ✓ Coordinates valid")
                
        except Exception as e:
            print(f"    ✗ Unpacking failed: {e}")
            bbox_valid = False
            continue

# Test 6: Test with real image (if webcam available)
print("\nTest 6: Testing with webcam (if available)...")
try:
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("  ⚠ Webcam not available (this is OK)")
    else:
        print("  ✓ Webcam opened")
        
        # Read one frame
        ret, frame = cap.read()
        if ret:
            print(f"  ✓ Frame captured: {frame.shape}")
            
            # Run detection
            detections = detector.detect(frame)
            print(f"  ✓ Detection ran: {len(detections)} faces detected")
            
            # Validate format
            for idx, bbox in enumerate(detections):
                if not isinstance(bbox, (tuple, list)) or len(bbox) != 4:
                    print(f"  ✗ Invalid bbox at {idx}: {bbox}")
                    bbox_valid = False
                else:
                    x1, y1, x2, y2 = bbox
                    print(f"  ✓ Bbox {idx}: ({x1}, {y1}, {x2}, {y2})")
        
        cap.release()
        
except Exception as e:
    print(f"  ⚠ Webcam test skipped: {e}")

# Final result
print("\n" + "=" * 70)
if bbox_valid:
    print("✅ ALL TESTS PASSED!")
    print("   BBox format is correct: (x1, y1, x2, y2)")
else:
    print("❌ TESTS FAILED!")
    print("   BBox format is incorrect")
    print("\n   Please use the fixed blazeface_detector.py")

print("=" * 70)

sys.exit(0 if bbox_valid else 1)
