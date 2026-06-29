#!/usr/bin/env python3
"""
Utility Functions
Helper functions for logging, image preprocessing, and visualization
Fixed version - Compatible with the face recognition robot system
"""

import cv2
import numpy as np
import logging
from datetime import datetime
from pathlib import Path


def setup_logging(log_dir="logs", log_level="INFO"):
    """
    Setup logging configuration
    
    Args:
        log_dir: Directory for log files
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        Logger instance
    """
    # Create log directory if it doesn't exist
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = Path(log_dir) / f"robot_{timestamp}.log"
    
    # Configure logging
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Set up file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, log_level.upper()))
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Add handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file}")
    
    return logger


def preprocess_image(image, target_size=(128, 128), normalize=True):
    """
    Preprocess image for model input
    
    Args:
        image: Input BGR image
        target_size: Target size (width, height)
        normalize: Whether to normalize to [0, 1]
        
    Returns:
        Preprocessed image
    """
    if image is None or image.size == 0:
        return None
    
    # Resize
    resized = cv2.resize(image, target_size)
    
    # Convert BGR to RGB
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    
    # Normalize if requested
    if normalize:
        processed = rgb.astype(np.float32) / 255.0
    else:
        processed = rgb.astype(np.float32)
    
    return processed


def draw_detection_info(image, bbox, label, confidence, color=(0, 255, 0)):
    """
    Draw detection bounding box and label on image
    FIXED: Properly handles bbox format (x1, y1, x2, y2)
    
    Args:
        image: Input image
        bbox: Bounding box (x1, y1, x2, y2) - simple tuple
        label: Text label
        confidence: Confidence score
        color: Box color (B, G, R)
        
    Returns:
        Image with drawn info
    """
    # FIXED: Properly unpack bbox
    if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
        x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
    else:
        logging.warning(f"Invalid bbox format: {bbox}")
        return image
    
    # Ensure integers
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    
    # Draw rectangle
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
    
    # Prepare label text
    if confidence is not None:
        text = f"{label} ({confidence:.0%})"
    else:
        text = label
    
    # Get text size for background
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Draw background rectangle for text
    cv2.rectangle(image, 
                  (x1, y1 - text_height - 10), 
                  (x1 + text_width, y1), 
                  color, 
                  -1)
    
    # Draw text
    cv2.putText(image, text, (x1, y1 - 5), font, font_scale, (255, 255, 255), thickness)
    
    return image


def calculate_iou(box1, box2):
    """
    Calculate Intersection over Union (IoU) between two boxes
    FIXED: Handles simple tuple format (x1, y1, x2, y2)
    
    Args:
        box1: (x1, y1, x2, y2)
        box2: (x1, y1, x2, y2)
        
    Returns:
        IoU score (0.0 to 1.0)
    """
    # FIXED: Ensure proper unpacking
    if len(box1) < 4 or len(box2) < 4:
        return 0.0
    
    x1_1, y1_1, x2_1, y2_1 = box1[0], box1[1], box1[2], box1[3]
    x1_2, y1_2, x2_2, y2_2 = box2[0], box2[1], box2[2], box2[3]
    
    # Calculate intersection
    x1_i = max(x1_1, x1_2)
    y1_i = max(y1_1, y1_2)
    x2_i = min(x2_1, x2_2)
    y2_i = min(y2_1, y2_2)
    
    if x2_i < x1_i or y2_i < y1_i:
        return 0.0
    
    intersection_area = (x2_i - x1_i) * (y2_i - y1_i)
    
    # Calculate union
    box1_area = (x2_1 - x1_1) * (y2_1 - y1_1)
    box2_area = (x2_2 - x1_2) * (y2_2 - y1_2)
    union_area = box1_area + box2_area - intersection_area
    
    iou = intersection_area / union_area if union_area > 0 else 0.0
    
    return iou


def non_max_suppression(boxes, scores, iou_threshold=0.5):
    """
    Apply Non-Maximum Suppression to remove overlapping boxes
    FIXED: Works with simple tuple format [(x1, y1, x2, y2), ...]
    
    Args:
        boxes: List of boxes [(x1, y1, x2, y2), ...]
        scores: List of confidence scores
        iou_threshold: IoU threshold for suppression
        
    Returns:
        Indices of boxes to keep
    """
    if len(boxes) == 0:
        return []
    
    # Convert to numpy array for easier handling
    boxes = np.array(boxes)
    scores = np.array(scores)
    
    # Sort by score in descending order
    indices = np.argsort(scores)[::-1]
    
    keep = []
    
    while len(indices) > 0:
        # Keep the box with highest score
        current = indices[0]
        keep.append(current)
        
        if len(indices) == 1:
            break
        
        # Calculate IoU with remaining boxes
        current_box = boxes[current]
        remaining_indices = indices[1:]
        
        ious = [calculate_iou(current_box, boxes[i]) for i in remaining_indices]
        
        # Keep boxes with IoU below threshold
        indices = remaining_indices[np.array(ious) < iou_threshold]
    
    return keep


def save_detection_result(image, filename, log_dir="logs"):
    """
    Save detection result image
    
    Args:
        image: Image to save
        filename: Output filename
        log_dir: Directory to save to
        
    Returns:
        Path to saved image
    """
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    output_path = Path(log_dir) / filename
    cv2.imwrite(str(output_path), image)
    return output_path


def create_grid_visualization(images, labels, grid_size=(2, 2)):
    """
    Create a grid visualization of multiple images
    
    Args:
        images: List of images
        labels: List of labels for each image
        grid_size: Grid dimensions (rows, cols)
        
    Returns:
        Grid visualization image
    """
    rows, cols = grid_size
    
    if len(images) == 0:
        return None
    
    # Get image size (assume all same size)
    h, w = images[0].shape[:2]
    
    # Create blank canvas
    canvas = np.zeros((h * rows, w * cols, 3), dtype=np.uint8)
    
    # Place images in grid
    for idx, (img, label) in enumerate(zip(images, labels)):
        if idx >= rows * cols:
            break
        
        row = idx // cols
        col = idx % cols
        
        y1 = row * h
        y2 = (row + 1) * h
        x1 = col * w
        x2 = (col + 1) * w
        
        canvas[y1:y2, x1:x2] = img
        
        # Add label
        cv2.putText(canvas, label, (x1 + 10, y1 + 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    return canvas


def extract_face_safely(image, bbox, padding=0.1):
    """
    Safely extract face region from image with padding
    FIXED: Handles bbox format properly
    
    Args:
        image: Original BGR image
        bbox: Bounding box (x1, y1, x2, y2)
        padding: Padding ratio around face (default 0.1 = 10%)
        
    Returns:
        Cropped face image or None if invalid
    """
    try:
        # FIXED: Properly unpack bbox
        if len(bbox) < 4:
            return None
            
        x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        
        # Validate bbox
        if x2 <= x1 or y2 <= y1:
            return None
        
        # Calculate padding
        width = x2 - x1
        height = y2 - y1
        pad_w = int(width * padding)
        pad_h = int(height * padding)
        
        # Apply padding
        x1 = max(0, x1 - pad_w)
        y1 = max(0, y1 - pad_h)
        x2 = min(image.shape[1], x2 + pad_w)
        y2 = min(image.shape[0], y2 + pad_h)
        
        # Extract face ROI
        face_roi = image[y1:y2, x1:x2]
        
        # Validate extracted region
        if face_roi.size == 0:
            return None
            
        return face_roi
        
    except Exception as e:
        logging.error(f"Error extracting face: {e}")
        return None


def get_system_info():
    """Get system information for logging"""
    import platform
    import sys
    
    info = {
        'platform': platform.platform(),
        'python_version': sys.version.split()[0],
        'opencv_version': cv2.__version__,
    }
    
    try:
        import tensorflow as tf
        info['tensorflow_version'] = tf.__version__
    except ImportError:
        info['tensorflow_version'] = 'Not installed'
    
    return info


def print_system_banner():
    """Print system startup banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║         Face Recognition Robot with Servo Control        ║
    ║                                                           ║
    ║  Detection:    BlazeFace TFLite                          ║
    ║  Recognition:  TinyCNN (Mr. David)                       ║
    ║  Hardware:     Raspberry Pi 5 + STM32F103 + 16 Servos   ║
    ║  Camera:       USB C270 HD (640x480 @ 30fps)            ║
    ║                                                           ║
    ║  Status:       ✅ FIXED - No unpacking errors            ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def validate_bbox(bbox):
    """
    Validate bounding box format and values
    
    Args:
        bbox: Bounding box to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        if not isinstance(bbox, (list, tuple)):
            return False
        
        if len(bbox) < 4:
            return False
        
        x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
        
        # Check if coordinates are valid
        if x2 <= x1 or y2 <= y1:
            return False
        
        # Check if coordinates are reasonable (not negative, not too large)
        if x1 < 0 or y1 < 0 or x2 > 10000 or y2 > 10000:
            return False
        
        return True
        
    except Exception:
        return False


def draw_fps(image, fps, position=(10, 30)):
    """
    Draw FPS counter on image
    
    Args:
        image: Input image
        fps: FPS value
        position: Text position (x, y)
        
    Returns:
        Image with FPS drawn
    """
    text = f"FPS: {fps:.1f}"
    cv2.putText(image, text, position,
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    return image


def draw_detection_count(image, count, position=(10, 70)):
    """
    Draw detection count on image
    
    Args:
        image: Input image
        count: Number of detections
        position: Text position (x, y)
        
    Returns:
        Image with count drawn
    """
    text = f"Faces: {count}"
    cv2.putText(image, text, position,
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    return image


def load_config(config_path="config.yaml"):
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary or None if failed
    """
    try:
        import yaml
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except ImportError:
        logging.warning("PyYAML not installed. Install with: pip3 install pyyaml")
        return None
    except FileNotFoundError:
        logging.warning(f"Config file not found: {config_path}")
        return None
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        return None


def format_detection_result(detections, is_tracking=False):
    """
    Format detection results for display
    
    Args:
        detections: List of bounding boxes or dict of tracked faces
        is_tracking: Whether detections include tracking IDs
        
    Returns:
        Formatted string
    """
    if is_tracking and isinstance(detections, dict):
        return f"{len(detections)} tracked faces"
    elif isinstance(detections, (list, tuple)):
        return f"{len(detections)} faces detected"
    else:
        return "No detections"


# Test code
if __name__ == "__main__":
    print("=" * 70)
    print("Utility Functions - Test Mode")
    print("=" * 70)
    print()
    
    print_system_banner()
    
    # Test logging setup
    logger = setup_logging()
    logger.info("✓ Logging test successful")
    
    # Test system info
    info = get_system_info()
    print("\nSystem Information:")
    print("-" * 70)
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print()
    print("-" * 70)
    print("Testing bbox validation...")
    
    # Test bbox validation
    valid_bbox = (100, 100, 200, 200)
    invalid_bbox_1 = (100, 100, 50, 200)  # Invalid: x2 < x1
    invalid_bbox_2 = (100, 100)  # Invalid: too few values
    
    print(f"  Valid bbox {valid_bbox}: {validate_bbox(valid_bbox)}")
    print(f"  Invalid bbox {invalid_bbox_1}: {validate_bbox(invalid_bbox_1)}")
    print(f"  Invalid bbox {invalid_bbox_2}: {validate_bbox(invalid_bbox_2)}")
    
    print()
    print("-" * 70)
    print("✓ All utility functions ready!")
    print("=" * 70)
