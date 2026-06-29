#!/usr/bin/env python3
"""
BlazeFace Face Detector - CLEAN + STABLE VERSION
Guaranteed output format:
    [(x1, y1, x2, y2), (x1, y1, x2, y2), ...]
"""
import os
import cv2
import numpy as np
import logging
import urllib.request
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BlazeFace")
try:
    import tensorflow as tf
    TFLITE_AVAILABLE = True
    logger.info("✓ TensorFlow Lite loaded")
except:
    TFLITE_AVAILABLE = False
    logger.error("❌ TensorFlow Lite not installed")

class BlazeFaceDetector:
    def __init__(self, model_path="models/blazeface.tflite", confidence_threshold=0.7):
        self.confidence_threshold = confidence_threshold
        
        # Create models directory if it doesn't exist
        os.makedirs("models", exist_ok=True)
        
        # Download model if it doesn't exist
        if not os.path.exists(model_path):
            logger.info(f"Model not found at {model_path}, downloading...")
            self.download_model(model_path)
        
        if not TFLITE_AVAILABLE:
            raise ImportError("TensorFlow Lite is required")
        
        logger.info(f"Loading BlazeFace model: {model_path}")
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        shape = self.input_details[0]['shape']
        self.in_h, self.in_w = shape[1], shape[2]
        logger.info(f"✓ BlazeFace ready: input={self.in_w}x{self.in_h}")
    
    # -----------------------------------------------------
    # Download model from MediaPipe repository
    # -----------------------------------------------------
    def download_model(self, model_path):
        """Download BlazeFace model from MediaPipe's official repository"""
        # MediaPipe BlazeFace short range model (optimized for close-range face detection)
        model_url = "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite"
        
        temp_path = model_path + ".tmp"
        try:
            logger.info(f"Downloading BlazeFace model from {model_url}")
            logger.info("This may take a moment...")
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            
            # Download with progress indication
            def report_progress(block_num, block_size, total_size):
                downloaded = block_num * block_size
                if total_size > 0:
                    percent = min(downloaded * 100 / total_size, 100)
                    if block_num % 10 == 0:  # Update every 10 blocks
                        logger.info(f"Download progress: {percent:.1f}%")
            
            # Download the file
            urllib.request.urlretrieve(model_url, temp_path, reporthook=report_progress)
            
            # Verify download
            if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
                # Move temp file to final location
                if os.path.exists(model_path):
                    os.remove(model_path)
                os.rename(temp_path, model_path)
                
                file_size = os.path.getsize(model_path)
                logger.info(f"✓ Model downloaded successfully!")
                logger.info(f"✓ Saved to: {os.path.abspath(model_path)}")
                logger.info(f"✓ File size: {file_size / 1024:.2f} KB")
            else:
                raise RuntimeError("Downloaded file is empty or invalid")
            
        except Exception as e:
            # Clean up temp file if it exists
            if os.path.exists(temp_path):
                os.remove(temp_path)
            logger.error(f"❌ Failed to download model: {e}")
            raise RuntimeError(f"Could not download BlazeFace model: {e}")

    
    # -----------------------------------------------------
    # Draw bounding boxes ONLY around detected faces
    # -----------------------------------------------------
    def draw_detections(self, frame, detections, color=(0, 255, 0), thickness=2, 
                       show_label=False, show_confidence=False):
        """
        Draw bounding boxes ONLY around detected faces (not the whole frame)
        Faces are sorted by size (largest to smallest) and numbered with IDs
        
        Args:
            frame: Input image/frame
            detections: List of detected face boxes [(x1, y1, x2, y2), ...]
            color: Box color in BGR format (default: green)
            thickness: Box line thickness
            show_label: Whether to show face ID labels
            show_confidence: Whether to show confidence scores
        
        Returns:
            Frame with bounding boxes drawn ONLY around detected faces
        """
        output = frame.copy()
        
        # Sort detections by size (area) - largest to smallest
        # Calculate area for each detection and sort
        detections_with_area = []
        for detection in detections:
            if isinstance(detection, tuple) and len(detection) >= 4:
                x1, y1, x2, y2 = detection[:4]
                area = (x2 - x1) * (y2 - y1)
                detections_with_area.append((area, detection))
        
        # Sort by area (largest first)
        detections_with_area.sort(key=lambda x: x[0], reverse=True)
        
        # Draw boxes ONLY around detected faces with ID numbers
        for face_id, (area, detection) in enumerate(detections_with_area, start=1):
            x1, y1, x2, y2 = detection[:4]
            
            # Draw rectangle ONLY around this face
            cv2.rectangle(output, (x1, y1), (x2, y2), color, thickness)
            
            # Add ID label if requested
            if show_label:
                label = f"ID:{face_id}"
                
                # Get text size for background
                (label_width, label_height), baseline = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
                )
                
                # Draw label background
                cv2.rectangle(output, 
                            (x1, y1 - label_height - 10), 
                            (x1 + label_width + 5, y1), 
                            color, -1)
                
                # Draw label text
                cv2.putText(output, label, (x1 + 2, y1 - 5), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        # Add face count at top
        count_text = f"Faces: {len(detections)}"
        cv2.putText(output, count_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        return output
    
    # -----------------------------------------------------
    # Detect and draw in one step
    # -----------------------------------------------------
    def detect_and_draw(self, frame, color=(0, 255, 0), thickness=2, 
                       show_label=False, confidence_threshold=None):
        """
        Detect faces and draw bounding boxes in one step
        Faces are automatically sorted by size (largest to smallest) and numbered
        
        Args:
            frame: Input image/frame
            color: Box color in BGR format
            thickness: Box line thickness
            show_label: Whether to show face ID labels
            confidence_threshold: Override default confidence threshold
        
        Returns:
            Tuple of (output_frame, detections)
            - output_frame: Frame with boxes drawn ONLY around detected faces
            - detections: List of detected face boxes [(x1, y1, x2, y2), ...]
                         sorted by size (largest to smallest)
        """
        # Temporarily override confidence threshold if provided
        original_threshold = self.confidence_threshold
        if confidence_threshold is not None:
            self.confidence_threshold = confidence_threshold
        
        # Detect faces
        detections = self.detect(frame)
        
        # Restore original threshold
        self.confidence_threshold = original_threshold
        
        # Draw boxes ONLY around detected faces (with sorting and IDs)
        output = self.draw_detections(frame, detections, color, thickness, show_label)
        
        return output, detections
    
    # -----------------------------------------------------
    # Get sorted detections with IDs
    # -----------------------------------------------------
    def get_sorted_detections_with_ids(self, frame):
        """
        Detect faces and return them sorted by size with ID numbers
        
        Args:
            frame: Input image/frame
        
        Returns:
            List of tuples: [(face_id, x1, y1, x2, y2, area), ...]
            Sorted from largest to smallest face
        """
        detections = self.detect(frame)
        
        # Calculate area and add IDs
        detections_with_info = []
        for detection in detections:
            if isinstance(detection, tuple) and len(detection) >= 4:
                x1, y1, x2, y2 = detection[:4]
                area = (x2 - x1) * (y2 - y1)
                detections_with_info.append((area, x1, y1, x2, y2))
        
        # Sort by area (largest first)
        detections_with_info.sort(key=lambda x: x[0], reverse=True)
        
        # Add IDs (1, 2, 3, ...)
        result = []
        for face_id, (area, x1, y1, x2, y2) in enumerate(detections_with_info, start=1):
            result.append((face_id, x1, y1, x2, y2, area))
        
        return result
    
    # -----------------------------------------------------
    # Preprocess input
    # -----------------------------------------------------
    def preprocess(self, img):
        img_resized = cv2.resize(img, (self.in_w, self.in_h))
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        img_norm = (img_rgb.astype(np.float32) / 127.5) - 1.0
        return np.expand_dims(img_norm, axis=0)
    
    # -----------------------------------------------------
    # Main face detection function
    # -----------------------------------------------------
    def detect(self, frame):
        if frame is None or frame.size == 0:
            return []
        
        H, W = frame.shape[:2]
        input_tensor = self.preprocess(frame)
        
        # Run inference
        self.interpreter.set_tensor(self.input_details[0]['index'], input_tensor)
        self.interpreter.invoke()
        
        raw_boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        raw_scores = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
        
        detections = []
        for i, score in enumerate(raw_scores):
            if score < self.confidence_threshold:
                continue
            
            box = raw_boxes[i]
            if len(box) < 4:
                continue
            
            ymin, xmin, ymax, xmax = box[:4]
            
            # Convert to pixel coordinates
            x1 = int(xmin * W)
            y1 = int(ymin * H)
            x2 = int(xmax * W)
            y2 = int(ymax * H)
            
            # Clip
            x1 = max(0, min(x1, W - 1))
            y1 = max(0, min(y1, H - 1))
            x2 = max(0, min(x2, W - 1))
            y2 = max(0, min(y2, H - 1))
            
            # Skip invalid boxes
            if x2 <= x1 or y2 <= y1:
                continue
            
            # Skip tiny boxes (prevents UNKNOWN red issue)
            if (x2 - x1) < 20 or (y2 - y1) < 20:
                continue
            
            detections.append((x1, y1, x2, y2))
        
        return detections


# -----------------------------------------------------
# Test/Main function
# -----------------------------------------------------
if __name__ == "__main__":
    logger.info("="*60)
    logger.info("BlazeFace Detector - Auto-Resizing Face Detection")
    logger.info("="*60)
    
    try:
        # Initialize detector (this will download model if needed)
        detector = BlazeFaceDetector()
        
        # Verify model file exists
        model_path = "models/blazeface.tflite"
        if os.path.exists(model_path):
            file_size = os.path.getsize(model_path)
            logger.info(f"✓ Model saved successfully!")
            logger.info(f"✓ Location: {os.path.abspath(model_path)}")
            logger.info(f"✓ Size: {file_size / 1024:.2f} KB")
        else:
            logger.error(f"❌ Model file not found at {model_path}")
        
        # Test with a dummy image
        logger.info("\nTesting face detection with dummy image...")
        test_img = np.zeros((480, 640, 3), dtype=np.uint8)
        detections = detector.detect(test_img)
        logger.info(f"✓ Detection test completed (found {len(detections)} faces)")
        
        logger.info("\n" + "="*60)
        logger.info("Webcam Demo - Auto-Resizing Face Detection")
        logger.info("="*60)
        logger.info("\nFeatures:")
        logger.info("  ✓ Detects ONLY human faces")
        logger.info("  ✓ Boxes automatically resize with distance")
        logger.info("  ✓ Move closer → Box gets BIGGER")
        logger.info("  ✓ Move farther → Box gets SMALLER")
        logger.info("  ✓ No labels, just clean boxes")
        logger.info("\nStarting webcam demo in 2 seconds...")
        logger.info("Press 'q' to quit | Press 'c' to change color")
        
        import time
        time.sleep(2)
        
        # Try to open webcam
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            logger.info("\n✓ Webcam opened successfully")
            logger.info("Try moving closer and farther from the camera!\n")
            
            frame_count = 0
            colors = [
                (0, 255, 0),    # Green
                (0, 0, 255),    # Red
                (255, 0, 0),    # Blue
                (0, 255, 255),  # Yellow
            ]
            color_names = ["Green", "Red", "Blue", "Yellow"]
            current_color = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Detect and draw - boxes automatically resize with distance
                output, detections = detector.detect_and_draw(
                    frame, 
                    color=colors[current_color], 
                    thickness=3,
                    show_label=False  # No ID labels
                )
                
                # Add instructions
                instructions = "Q:Quit | C:Change Color"
                cv2.putText(output, instructions, 
                           (10, frame.shape[0] - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Show current color
                color_text = f"Color: {color_names[current_color]}"
                cv2.putText(output, color_text, 
                           (frame.shape[1] - 150, frame.shape[0] - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[current_color], 2)
                
                # Add movement hint
                hint = "Move closer/farther to see boxes resize!"
                cv2.putText(output, hint, 
                           (10, frame.shape[0] - 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
                
                cv2.imshow('Auto-Resizing Face Detection (Press Q to quit)', output)
                
                # Log face detections
                frame_count += 1
                if frame_count % 60 == 0 and len(detections) > 0:
                    logger.info(f"Frame {frame_count}: {len(detections)} face(s) detected")
                    for i, (x1, y1, x2, y2) in enumerate(detections, 1):
                        width = x2 - x1
                        height = y2 - y1
                        area = width * height
                        logger.info(f"  Face {i}: {width}x{height}px (Area: {area})")
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('c'):
                    current_color = (current_color + 1) % len(colors)
                    logger.info(f"Color changed to: {color_names[current_color]}")
            
            cap.release()
            cv2.destroyAllWindows()
            logger.info("\n✓ Webcam demo completed")
            logger.info("Boxes automatically resized as you moved!")
        else:
            logger.info("ℹ Webcam not available - skipping demo")
        
    except KeyboardInterrupt:
        logger.info("\n\nDemo interrupted by user")
        if 'cap' in locals():
            cap.release()
            cv2.destroyAllWindows()
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
