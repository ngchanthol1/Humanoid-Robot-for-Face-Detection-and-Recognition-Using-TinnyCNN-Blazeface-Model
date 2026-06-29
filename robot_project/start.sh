#!/bin/bash
# Face Recognition Robot - Easy Startup Script
# This script checks dependencies and starts the system

echo "================================================================"
echo "    Face Recognition Robot - Startup Script"
echo "================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check Python version
echo "Step 1: Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python found: $PYTHON_VERSION"
else
    print_error "Python3 not found!"
    echo "  Install: sudo apt install python3"
    exit 1
fi

# Check required Python modules
echo ""
echo "Step 2: Checking Python modules..."

MISSING_MODULES=()

# Check PIL
if python3 -c "from PIL import Image, ImageTk" 2>/dev/null; then
    print_success "PIL and ImageTk available"
else
    print_error "PIL ImageTk not found"
    MISSING_MODULES+=("PIL")
fi

# Check OpenCV
if python3 -c "import cv2" 2>/dev/null; then
    print_success "OpenCV available"
else
    print_error "OpenCV not found"
    MISSING_MODULES+=("opencv")
fi

# Check Serial
if python3 -c "import serial" 2>/dev/null; then
    print_success "PySerial available"
else
    print_error "PySerial not found"
    MISSING_MODULES+=("serial")
fi

# Check NumPy
if python3 -c "import numpy" 2>/dev/null; then
    print_success "NumPy available"
else
    print_error "NumPy not found"
    MISSING_MODULES+=("numpy")
fi

# If modules are missing, show install commands
if [ ${#MISSING_MODULES[@]} -gt 0 ]; then
    echo ""
    print_error "Missing modules detected!"
    echo ""
    echo "Install missing dependencies:"
    echo "  sudo apt update"
    echo "  sudo apt install -y python3-pil python3-pil.imagetk python3-opencv python3-serial python3-numpy"
    echo "  pip3 install scipy tensorflow scikit-learn --break-system-packages"
    echo ""
    read -p "Do you want to install now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Installing dependencies..."
        sudo apt update
        sudo apt install -y python3-pil python3-pil.imagetk python3-opencv python3-serial python3-numpy
        pip3 install scipy tensorflow scikit-learn --break-system-packages
        print_success "Installation complete!"
    else
        print_warning "Please install dependencies manually before running."
        exit 1
    fi
fi

# Check required files
echo ""
echo "Step 3: Checking required files..."

REQUIRED_FILES=("main.py" "blazeface_detector.py" "servo_control.py" "tinycnn_recognizer.py")
MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "$file found"
    else
        print_error "$file not found"
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    print_error "Missing required files!"
    echo "  Please download all files to this directory"
    exit 1
fi

# Check directories
echo ""
echo "Step 4: Checking directories..."

REQUIRED_DIRS=("models" "logs")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        print_success "$dir directory exists"
    else
        print_warning "$dir directory not found, creating..."
        mkdir -p "$dir"
        print_success "$dir directory created"
    fi
done

# Check camera
echo ""
echo "Step 5: Checking camera..."

if [ -c "/dev/video0" ]; then
    print_success "Camera found at /dev/video0"
else
    print_warning "Camera not found at /dev/video0"
    echo "  System will still start, but camera may not work"
fi

# Check UART (optional)
echo ""
echo "Step 6: Checking UART (optional for servo control)..."

if [ -c "/dev/ttyAMA0" ]; then
    print_success "UART found at /dev/ttyAMA0"
elif [ -c "/dev/serial0" ]; then
    print_success "UART found at /dev/serial0"
else
    print_warning "UART not found"
    echo "  Servo control may not work without UART"
    echo "  Enable UART in: sudo raspi-config"
fi

# Optional: Run bbox format test
echo ""
read -p "Run bbox format test? (recommended) (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "test_bbox_format.py" ]; then
        print_info "Running bbox format test..."
        python3 test_bbox_format.py
        TEST_RESULT=$?
        if [ $TEST_RESULT -eq 0 ]; then
            print_success "BBox format test passed!"
        else
            print_error "BBox format test failed!"
            echo "  Check test_bbox_format.py output for details"
            read -p "Continue anyway? (y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi
    else
        print_warning "test_bbox_format.py not found, skipping test"
    fi
fi

# All checks passed, start main application
echo ""
echo "================================================================"
print_success "All checks passed! Starting application..."
echo "================================================================"
echo ""

# Start main.py
python3 main.py

# Capture exit code
EXIT_CODE=$?

echo ""
echo "================================================================"
if [ $EXIT_CODE -eq 0 ]; then
    print_success "Application exited normally"
else
    print_error "Application exited with error code: $EXIT_CODE"
    echo ""
    echo "Check logs directory for error details:"
    echo "  ls -lh logs/"
fi
echo "================================================================"

exit $EXIT_CODE
