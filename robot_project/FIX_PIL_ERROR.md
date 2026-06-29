# 🔧 PIL ImageTk Import Error - Quick Fix

## Error Message:
```
ImportError: cannot import name 'ImageTk' from 'PIL'
```

## ✅ Solution (Choose One):

### Option 1: Install via apt (Recommended for Raspberry Pi)
```bash
sudo apt update
sudo apt install python3-pil python3-pil.imagetk
```

### Option 2: Install via pip
```bash
pip3 install pillow --break-system-packages
```

### Option 3: Install all dependencies at once
```bash
# Recommended: Install everything needed
sudo apt update
sudo apt install python3-pil python3-pil.imagetk python3-opencv python3-serial python3-numpy

# Then install remaining via pip
pip3 install scipy tensorflow scikit-learn --break-system-packages
```

## ⚡ After Installation:

```bash
# Run main.py
python3 main.py
```

---

## 🔍 Verify Installation:

```bash
# Test if ImageTk is available
python3 -c "from PIL import Image, ImageTk; print('✓ PIL and ImageTk working!')"
```

Expected output:
```
✓ PIL and ImageTk working!
```

---

## 📦 Complete Installation Command:

```bash
# One-line install for everything
sudo apt update && sudo apt install -y python3-pil python3-pil.imagetk python3-opencv python3-serial python3-numpy python3-scipy && pip3 install tensorflow scikit-learn --break-system-packages
```

---

## 🆘 If Still Not Working:

### Check Python version:
```bash
python3 --version
# Should be 3.11+
```

### Check PIL installation:
```bash
python3 -c "import PIL; print(PIL.__version__)"
```

### Reinstall Pillow:
```bash
pip3 uninstall pillow
pip3 install pillow --break-system-packages
```

---

## ✅ Verification Checklist:

Run these commands to verify all dependencies:

```bash
# Check Python packages
python3 -c "import tkinter; print('✓ tkinter')"
python3 -c "from PIL import Image, ImageTk; print('✓ PIL/ImageTk')"
python3 -c "import cv2; print('✓ OpenCV')"
python3 -c "import serial; print('✓ pyserial')"
python3 -c "import numpy; print('✓ NumPy')"
python3 -c "import scipy; print('✓ SciPy')"
python3 -c "import tensorflow; print('✓ TensorFlow')"
```

All should print "✓" without errors.

---

## 🚀 Once Fixed, Run:

```bash
python3 main.py
```

System should start without errors! 🎉
