# 🤖 Humanoid Robot Face Recognition System
## Complete Setup Guide for Raspberry Pi 5

This is a complete face recognition system for a humanoid robot with RGB servo motors, optimized for Raspberry Pi 5.

---

## 📋 System Components

1. **blazeface_detector.py** - Fast face detection using BlazeFace TFLite
2. **tinycnn_recognizer.py** - Lightweight CNN for recognizing Mr. David
3. **train_model.py** - Training script for the TinyCNN model
4. **main.py** - Complete GUI application for robot control
5. **Models/** - Directory for model files

---

## 🔧 Hardware Requirements

- Raspberry Pi 5 (4GB+ RAM recommended)
- C270 HD Webcam (or compatible USB camera)
- STM32-based humanoid robot with 16 RGB servo motors
- UART connection between Raspberry Pi and STM32

---

## 📦 Software Installation

### 1. Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
pip3 install scipy tensorflow pyserial opencv-python pillow scikit-learn --break-system-packages
```

### 2. Create Project Structure

```bash
mkdir -p ~/robot_project
cd ~/robot_project

# Create directories
mkdir -p Models dataset/mrdavid dataset/others face_crops logs
```

### 3. Download Project Files

Place all project files in `~/robot_project/`:
- `main.py`
- `blazeface_detector.py`
- `tinycnn_recognizer.py`
- `train_model.py`

---

## 🎓 Training the Recognition Model

### Step 1: Collect Training Data

You need face images in two categories:

```
dataset/
├── mrdavid/          # Mr. David's face images (50-100+ images)
│   ├── david_01.jpg
│   ├── david_02.jpg
│   └── ...
└── others/           # Other people's faces (50-100+ images)
    ├── person1_01.jpg
    ├── person2_01.jpg
    └── ...
```

**Tips for collecting good training data:**
- Use varied lighting conditions
- Include different angles (front, side, slight tilt)
- Include different expressions (neutral, smiling, etc.)
- Use the face detection system to crop faces from photos
- More images = better accuracy (aim for 50-100 per category)

### Step 2: Use BlazeFace to Extract Faces

You can use the face detection system to automatically crop faces:

```bash
# Run this helper script to extract faces from images
python3 blazeface_detector.py
```

Then press 's' when faces are detected to save crops to `face_crops/`.

### Step 3: Train the Model

```bash
# Train with default settings (50 epochs)
python3 train_model.py

# Or with custom settings
python3 train_model.py --epochs 100 --batch-size 16 --img-size 96
```

**Training Parameters:**
- `--dataset`: Dataset directory (default: `dataset/`)
- `--epochs`: Number of training epochs (default: 50)
- `--batch-size`: Batch size (default: 32)
- `--img-size`: Input image size (default: 96)
- `--output`: Output model path (default: `models/tinycnn_mrdavid.tflite`)

### Step 4: Copy Model to Models Directory

```bash
# Copy trained model to Models directory
cp models/tinycnn_mrdavid.tflite Models/
```

---

## 🚀 Running the System

### 1. Automatic Model Download (BlazeFace)

The BlazeFace model will download automatically on first run. Or manually:

```bash
# Run once to download BlazeFace model
python3 blazeface_detector.py
```

This downloads `models/blazeface.tflite` automatically.

### 2. Copy BlazeFace Model

```bash
# Copy to Models directory
cp models/blazeface.tflite Models/
```

### 3. Launch Main Application

```bash
python3 main.py
```

---

## 🎮 Using the GUI Application

### Serial Connection
1. Select UART port (usually `/dev/ttyAMA0` on Raspberry Pi)
2. Set baud rate (default: 115200)
3. Click "Connect"

### Face Recognition
1. Click "🔍 Start Detection & Scanning"
2. System will:
   - Detect faces using BlazeFace
   - Recognize Mr. David using TinyCNN
   - Display "Welcome Mr. David" in BLUE when recognized
   - Execute greeting action automatically

### Motor Control
- **Global Controls**: Set all motors at once
- **Individual Controls**: Control each of 16 motors separately
- **Patterns**: Rainbow wave, wave motion
- **Colors**: Red (RGBMIX), Green (REDGREEN), Blue (GREENBLUE)
- **Angles**: -160° to +160°

---

## 🔍 System Architecture

### Face Detection Pipeline

```
Camera Frame → BlazeFace Detector → Face Bounding Boxes → TinyCNN Recognizer → Recognition Result
```

### Recognition Flow

1. **BlazeFace Detection**
   - Input: 640x480 BGR frame from camera
   - Output: List of face bounding boxes `[(x1, y1, x2, y2), ...]`
   - Speed: ~30 FPS on Raspberry Pi 5

2. **TinyCNN Recognition**
   - Input: Cropped face image (BGR)
   - Output: `(is_mrdavid, confidence)`
   - Confidence threshold: 0.75 (adjustable)

3. **Robot Action**
   - When Mr. David is recognized:
     1. Flash colors (acknowledgment)
     2. Set all motors to GREEN
     3. Execute wave motion
     4. Return to neutral position
   - Cooldown: 5 seconds between greetings

---

## ⚙️ Configuration

### Confidence Threshold

Edit `tinycnn_recognizer.py`:

```python
recognizer = TinyCNNRecognizer(
    model_path="Models/tinycnn_mrdavid.tflite",
    confidence_threshold=0.75  # Adjust this (0.0 to 1.0)
)
```

- **Lower** (e.g., 0.6): More sensitive, may get false positives
- **Higher** (e.g., 0.85): More strict, may miss some recognitions

### BlazeFace Detection Threshold

Edit `blazeface_detector.py`:

```python
detector = BlazeFaceDetector(
    model_path="Models/blazeface.tflite",
    confidence_threshold=0.7  # Adjust this (0.0 to 1.0)
)
```

---

## 🐛 Troubleshooting

### Issue: "Model not found"
**Solution:**
```bash
# Check if models exist
ls -lh Models/

# Should show:
# blazeface.tflite
# tinycnn_mrdavid.tflite

# If missing, download/train them
python3 blazeface_detector.py  # Downloads BlazeFace
python3 train_model.py         # Trains TinyCNN
```

### Issue: "Camera not opening"
**Solution:**
```bash
# Check camera connection
ls /dev/video*

# Test camera
sudo apt install v4l-utils
v4l2-ctl --list-devices

# Try different camera index in main.py
# Change: cv2.VideoCapture(0) to cv2.VideoCapture(1)
```

### Issue: "Serial port error"
**Solution:**
```bash
# Enable UART on Raspberry Pi
sudo raspi-config
# Interface Options → Serial Port → Enable

# Check available ports
ls /dev/ttyAMA* /dev/ttyUSB* /dev/ttyACM*

# Add user to dialout group
sudo usermod -a -G dialout $USER
# Then logout and login again
```

### Issue: "Low recognition accuracy"
**Solution:**
1. Collect more training data (50-100 images per category minimum)
2. Use varied lighting and angles
3. Increase training epochs: `python3 train_model.py --epochs 100`
4. Adjust confidence threshold (lower for more sensitive)
5. Check if dataset is balanced (similar number of images in both categories)

### Issue: "Too slow on Raspberry Pi"
**Solution:**
1. BlazeFace is already optimized for RPi 5
2. Reduce camera resolution in main.py:
   ```python
   self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
   self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
   ```
3. Enable speed optimization:
   ```python
   detections = detector.detect(frame, optimize_speed=True)
   ```

---

## 📊 Model Performance

### BlazeFace Detector
- **Speed**: ~30 FPS on Raspberry Pi 5
- **Model Size**: ~200 KB
- **Input**: 640x480 BGR
- **Accuracy**: High for frontal faces

### TinyCNN Recognizer
- **Speed**: ~10-20 FPS on Raspberry Pi 5
- **Model Size**: ~500-1000 KB (depends on quantization)
- **Input**: 96x96 RGB (adjustable)
- **Accuracy**: 90%+ with good training data

---

## 📁 File Descriptions

### Core Files

| File | Description |
|------|-------------|
| `main.py` | Complete GUI application with camera, face recognition, and motor control |
| `blazeface_detector.py` | BlazeFace face detection implementation (TFLite) |
| `tinycnn_recognizer.py` | TinyCNN face recognition implementation (TFLite) |
| `train_model.py` | Training script for TinyCNN model |

### Models

| Model | Size | Purpose |
|-------|------|---------|
| `blazeface.tflite` | ~200 KB | Face detection |
| `tinycnn_mrdavid.tflite` | ~500 KB | Mr. David recognition |

---

## 🎯 Best Practices

### Training Data Collection
1. **Quantity**: 50-100 images per category minimum
2. **Quality**: Clear, well-lit face images
3. **Variety**: Different angles, expressions, lighting
4. **Balance**: Equal number of images in both categories

### Model Training
1. **Start small**: Train with fewer epochs first (20-30)
2. **Monitor validation**: Check validation accuracy during training
3. **Avoid overfitting**: If validation accuracy stops improving, stop training
4. **Save checkpoints**: Best model is automatically saved

### Recognition Tuning
1. **Test threshold**: Start with 0.75, adjust based on results
2. **False positives**: Increase threshold (e.g., 0.85)
3. **False negatives**: Decrease threshold (e.g., 0.65)
4. **Monitor logs**: Check activity log for confidence scores

---

## 🔄 System Workflow

```
[1] Collect Training Data
    ↓
[2] Train TinyCNN Model (train_model.py)
    ↓
[3] Copy Models to Models/
    ↓
[4] Launch main.py
    ↓
[5] Connect to Serial Port
    ↓
[6] Start Face Detection
    ↓
[7] System Recognizes Mr. David
    ↓
[8] Robot Executes Greeting Action
```

---

## 📝 Command Reference

```bash
# Install dependencies
pip3 install scipy tensorflow pyserial opencv-python pillow scikit-learn --break-system-packages

# Download BlazeFace model
python3 blazeface_detector.py

# Train TinyCNN model
python3 train_model.py --epochs 50

# Test trained model on image
python3 train_model.py --test-image path/to/test.jpg

# Run main application
python3 main.py
```

---

## 🆘 Support

### Getting Help
1. Check activity log in GUI for error messages
2. Enable debug logging in Python files
3. Test components individually:
   - Camera: `python3 -c "import cv2; print(cv2.VideoCapture(0).isOpened())"`
   - Serial: `ls /dev/ttyAMA* /dev/ttyUSB*`
   - Models: `ls -lh Models/`

### Common Issues
- **Import errors**: Reinstall dependencies with `--break-system-packages`
- **Model errors**: Retrain model or check file paths
- **Camera errors**: Check USB connection and permissions
- **Serial errors**: Check UART enable and port permissions

---

## 📜 License

This project is for educational and research purposes.

---

## ✨ Features

- ✅ Real-time face detection (BlazeFace)
- ✅ Person recognition (TinyCNN)
- ✅ Automatic robot greeting
- ✅ RGB LED control (16 motors)
- ✅ Servo angle control (-160° to +160°)
- ✅ Pattern animations (rainbow wave, wave motion)
- ✅ Activity logging
- ✅ UART communication
- ✅ Raspberry Pi 5 optimized

---

## 🚀 Future Enhancements

- [ ] Multi-person recognition
- [ ] Voice interaction
- [ ] Emotion detection
- [ ] Hand gesture recognition
- [ ] Remote control via web interface
- [ ] Data augmentation during training
- [ ] Model compression for faster inference

---

## 👨‍💻 Development

**Version**: 1.0  
**Platform**: Raspberry Pi 5 (Bookworm)  
**Python**: 3.11+  
**TensorFlow**: 2.x (TFLite)

---

**Happy Robot Building! 🤖🎉**
