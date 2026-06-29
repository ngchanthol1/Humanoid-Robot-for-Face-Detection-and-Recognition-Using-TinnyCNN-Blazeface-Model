# ⚡ Quick Start Guide

## 🚀 Get Up and Running in 5 Minutes

### Step 1: Install Everything (2 minutes)

```bash
# Install dependencies
pip3 install scipy tensorflow pyserial opencv-python pillow scikit-learn --break-system-packages
```

### Step 2: Download Models (1 minute)

```bash
# Create Models directory
mkdir -p Models

# Download BlazeFace (happens automatically on first run)
python3 blazeface_detector.py

# Copy model
cp models/blazeface.tflite Models/
```

### Step 3: Launch Application (30 seconds)

```bash
python3 main.py
```

---

## 🎯 Without Training (Demo Mode)

If you don't have training data yet, the system will use OpenCV fallback detection:

1. Run `python3 main.py`
2. Click "Start Detection & Scanning"
3. System will detect faces (but recognize everyone as "Mr. David" for demo)

---

## 🎓 With Training (Full System)

### Quick Training Process

```bash
# 1. Create dataset structure
mkdir -p dataset/mrdavid dataset/others

# 2. Add images to folders
#    dataset/mrdavid/    <- Add 50+ photos of Mr. David
#    dataset/others/     <- Add 50+ photos of other people

# 3. Train model (takes 10-30 minutes)
python3 train_model.py --epochs 50

# 4. Copy model
cp models/tinycnn_mrdavid.tflite Models/

# 5. Run system
python3 main.py
```

---

## 📝 Minimal Working Example

```python
# test_detection.py - Minimal face detection test
import cv2
from blazeface_detector import BlazeFaceDetector

detector = BlazeFaceDetector()
camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    if not ret:
        break
    
    faces = detector.detect(frame)
    
    for (x1, y1, x2, y2) in faces:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    cv2.imshow('Face Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
```

---

## 🎮 GUI Controls Quick Reference

### Connect Robot
1. Select Port: `/dev/ttyAMA0` (Raspberry Pi UART)
2. Baud: `115200`
3. Click "Connect"

### Start Face Recognition
1. Click "🔍 Start Detection & Scanning"
2. When Mr. David detected:
   - Green box around face
   - "Welcome Mr. David" in BLUE
   - Robot performs greeting

### Manual Motor Control
- **Angles**: -160° to +160°
- **Colors**: 
  - 🔴 Red (RGBMIX)
  - 🟢 Green (REDGREEN)
  - 🔵 Blue (GREENBLUE)
- **Patterns**: Rainbow Wave, Wave Motion

---

## ⚙️ Important File Paths

```
Project Root/
├── main.py                          # Main application
├── blazeface_detector.py            # Face detection
├── tinycnn_recognizer.py            # Face recognition
├── train_model.py                   # Model training
├── Models/                          # Model files
│   ├── blazeface.tflite            # Face detection model
│   └── tinycnn_mrdavid.tflite      # Recognition model
└── dataset/                         # Training data
    ├── mrdavid/                    # Mr. David's photos
    └── others/                     # Other people's photos
```

---

## 🐛 Quick Troubleshooting

### Problem: "Model not found"
```bash
ls Models/  # Check if models exist
python3 blazeface_detector.py  # Download BlazeFace
python3 train_model.py         # Train TinyCNN
```

### Problem: "Camera not working"
```bash
ls /dev/video*  # Check camera device
# If no video devices, check USB connection
```

### Problem: "Serial port error"
```bash
ls /dev/ttyAMA*  # Check UART ports
sudo usermod -a -G dialout $USER  # Add permissions
# Logout and login again
```

### Problem: "Low accuracy"
- Collect more training images (50-100 per category)
- Use better lighting
- Include varied angles
- Retrain with more epochs

---

## 📊 Expected Performance

| Component | Performance |
|-----------|-------------|
| Face Detection | ~30 FPS |
| Recognition | ~10-20 FPS |
| Total System | ~10-15 FPS |
| Startup Time | ~5 seconds |

---

## 🎯 Testing Checklist

- [ ] Dependencies installed
- [ ] Camera working (`ls /dev/video*`)
- [ ] Serial port accessible (`ls /dev/ttyAMA*`)
- [ ] BlazeFace model downloaded
- [ ] TinyCNN model trained (optional)
- [ ] Models copied to Models/ directory
- [ ] GUI launches without errors
- [ ] Camera displays video
- [ ] Face detection works
- [ ] Serial connection succeeds
- [ ] Motors respond to commands

---

## 💡 Pro Tips

1. **Better Recognition**: Train with 100+ images per category
2. **Faster Detection**: Reduce camera resolution to 320x240
3. **Debug Mode**: Check activity log for detailed info
4. **Test Components**: Test face detection separately before full system
5. **Save Crops**: Press 's' during detection to save face images

---

## 📞 Need Help?

1. Check `README.md` for detailed documentation
2. Review activity log in GUI
3. Test components individually
4. Check file paths and permissions

---

**Ready to start? Run:**
```bash
python3 main.py
```

**🎉 Enjoy your Face Recognition Robot!**
