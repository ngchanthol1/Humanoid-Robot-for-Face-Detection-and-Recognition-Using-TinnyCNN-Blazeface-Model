# 📸 DATASET PREPARATION GUIDE

## ❌ You Got This Error:
```
❌ Directory not found: dataset\mrdavid
❌ Cannot proceed without valid dataset
```

## ✅ Here's How to Fix It (3 Easy Steps!)

---

## Step 1: Create Dataset Folders

**Option A: Automatic (Recommended)**
```bash
python3 setup_dataset.py
```

**Option B: Manual**

**Windows:**
```cmd
mkdir dataset
mkdir dataset\mrdavid
mkdir dataset\others
```

**Linux/Raspberry Pi:**
```bash
mkdir -p dataset/mrdavid
mkdir -p dataset/others
```

**Verify folders exist:**
```
your_project/
├── dataset/
│   ├── mrdavid/     ← Mr. David's photos go here
│   └── others/      ← Other people's photos go here
```

---

## Step 2: Add Images to Folders

You need **100-200 images** in EACH folder.

### 🎯 Image Quality Guidelines:

**Good Images ✅:**
- Clear face visible
- Well-lit (not too dark/bright)
- Different angles: front, left, right
- Different expressions: smile, neutral, serious
- Different distances: close, medium, far
- Various conditions: indoor, outdoor, with/without glasses

**Bad Images ❌:**
- Blurry or out of focus
- Face too small or too far
- Covered face (hands, objects)
- Extreme angles or lighting
- Multiple faces in one image

---

## Step 3: Collect Images (Choose ONE Method)

### **Method 1: Use Webcam (Easiest!) 📸**

**Step-by-step:**

1. Run the capture script:
   ```bash
   python3 capture_faces.py
   ```

2. Choose person:
   ```
   1. Mr. David
   2. Others
   Enter choice: 1
   ```

3. Camera opens, then:
   - Press **SPACE** to capture
   - Change your angle/expression
   - Press **SPACE** again
   - Repeat 100-200 times

4. Press **Q** to finish

5. Repeat for "Others":
   ```bash
   python3 capture_faces.py
   # Choose option 2 this time
   ```

**Tips for webcam capture:**
- Sit in front of camera
- Good lighting (face lamp or window)
- Capture every 2-3 seconds
- Move head: left, right, up, down
- Try different expressions
- Takes about 5-10 minutes per person

---

### **Method 2: Use Existing Photos 📁**

**If you have photos on your computer:**

**Windows:**
```cmd
# Copy Mr. David's photos
copy C:\MyPhotos\david\*.jpg dataset\mrdavid\

# Copy others' photos
copy C:\MyPhotos\family\*.jpg dataset\others\
```

**Linux/Raspberry Pi:**
```bash
# Copy Mr. David's photos
cp ~/Photos/david/*.jpg dataset/mrdavid/

# Copy others' photos
cp ~/Photos/family/*.jpg dataset/others/
```

**Or just drag & drop:**
1. Open file explorer
2. Navigate to your photos
3. Select 100-200 photos
4. Drag to `dataset/mrdavid/` or `dataset/others/`

---

### **Method 3: Extract from Videos 🎥**

If you have videos of Mr. David:

```python
# save as extract_faces.py
import cv2
from pathlib import Path

video_path = "path/to/video.mp4"  # Change this
output_dir = Path("dataset/mrdavid")
output_dir.mkdir(parents=True, exist_ok=True)

cap = cv2.VideoCapture(video_path)
frame_count = 0
saved_count = 0

# Extract every 30th frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    if frame_count % 30 == 0:  # Every 30 frames (~1 per second)
        filename = output_dir / f"frame_{saved_count:04d}.jpg"
        cv2.imwrite(str(filename), frame)
        saved_count += 1
        print(f"Saved: {filename.name}")
    
    frame_count += 1

cap.release()
print(f"Extracted {saved_count} images from video")
```

Run it:
```bash
python3 extract_faces.py
```

---

## Step 4: Verify Dataset

Run verification:
```bash
python3 setup_dataset.py
```

**Expected output:**
```
✅ Created: dataset
✅ Created: dataset/mrdavid
✅ Created: dataset/others

CURRENT STATUS
══════════════════════════════════════════════════════════════════════
Mr. David images: 150
Others images: 120

✅ Dataset ready for training!
   Run: python3 train_model.py
```

**If you see this:**
```
⚠️  No Mr. David images found
⚠️  Need more images:
   - Mr. David: 100 more images
   - Others: 50 more images
```
Then go back to Step 3 and add more images!

---

## Step 5: Train Model

Once you have 100+ images in BOTH folders:

```bash
python3 train_model.py --epochs 150 --batch-size 8
```

**Training takes:**
- Raspberry Pi 5: 30-60 minutes
- Windows (with GPU): 10-20 minutes
- Windows (CPU only): 20-40 minutes

**Expected output:**
```
══════════════════════════════════════════════════════════════════════
DATASET LOADED
══════════════════════════════════════════════════════════════════════
Total: 270 images
  Mr. David (label=1): 150 images
  Others (label=0): 120 images
  Ratio: 55.6% David
══════════════════════════════════════════════════════════════════════

[Training progress...]

══════════════════════════════════════════════════════════════════════
✅ TRAINING COMPLETE
══════════════════════════════════════════════════════════════════════

VALIDATION SET:
  Overall: 0.9074 (90.74%)
  Mr. David: 0.9200 (92.00%)
  Others: 0.8833 (88.33%)
```

---

## 🎯 Quick Checklist

- [ ] Folders created (`dataset/mrdavid` and `dataset/others`)
- [ ] 100+ images in `dataset/mrdavid/`
- [ ] 100+ images in `dataset/others/`
- [ ] Images are .jpg or .png format
- [ ] Images show clear faces
- [ ] Verified with `python3 setup_dataset.py`
- [ ] Ready to train!

---

## 💡 Pro Tips

### For Best Accuracy:

1. **Quality over Quantity**
   - 200 good images > 500 bad images
   - Clear, well-lit faces are essential

2. **Variety is Key**
   - Multiple angles (front, 45°, profile)
   - Multiple expressions (neutral, smile, serious)
   - Multiple conditions (indoor, outdoor, different lighting)
   - With/without glasses or hats

3. **Balance Classes**
   - Similar number in both folders
   - If 150 Mr. David → aim for 150 Others too

4. **Realistic Scenarios**
   - Capture images in conditions similar to where robot will work
   - If indoor robot → mostly indoor training images

5. **Quick Test Set**
   - Save 10-20 images separately for testing
   - Don't include in training folders
   - Use to verify model after training

---

## 🆘 Troubleshooting

### "No such file or directory: dataset"
**Fix:** Run `python3 setup_dataset.py` first

### "Only X images found, need 100+"
**Fix:** Add more images using webcam capture or copy more files

### "Image file corrupted"
**Fix:** Remove corrupted images, they usually have 0 KB size

### "Camera not working in capture_faces.py"
**Fix:** 
```bash
# Test camera
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'FAIL')"

# On Raspberry Pi, enable camera
sudo raspi-config
# Interface Options > Camera > Enable
```

### "Training takes too long"
**Fix:** 
- Use fewer images (100 per class is OK)
- Reduce epochs: `--epochs 100`
- Use smaller batch size: `--batch-size 4`

---

## 📊 Example Dataset Structure

```
robot_project/
├── dataset/
│   ├── mrdavid/
│   │   ├── face_001.jpg  (David front view)
│   │   ├── face_002.jpg  (David left view)
│   │   ├── face_003.jpg  (David right view)
│   │   ├── face_004.jpg  (David smiling)
│   │   ├── ... (146 more images)
│   │   └── face_150.jpg
│   │
│   └── others/
│       ├── person1_01.jpg  (John front view)
│       ├── person1_02.jpg  (John left view)
│       ├── person2_01.jpg  (Mary front view)
│       ├── person2_02.jpg  (Mary smiling)
│       ├── ... (116 more images)
│       └── person15_10.jpg
│
├── main.py
├── train_model.py
├── setup_dataset.py
├── capture_faces.py
└── ... (other files)
```

---

## ✅ Ready to Train!

Once you see this status:
```
✅ Dataset ready for training!
   Run: python3 train_model.py
```

You're ready! Run:
```bash
python3 train_model.py --epochs 150
```

Then after training completes:
```bash
python3 main.py
```

**Good luck! 🚀**
