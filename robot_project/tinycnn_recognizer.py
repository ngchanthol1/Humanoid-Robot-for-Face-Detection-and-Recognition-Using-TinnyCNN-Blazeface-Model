#!/usr/bin/env python3
"""
TinyCNN Face Recognizer - FIXED VERSION with Real-Time Camera Support
Properly handles binary classification with strict validation:
- Class 1 = Mr. David (should greet)
- Class 0 = Unknown person (should reject)
- Enhanced preprocessing for camera frames
- Stricter thresholds to prevent false positives on real faces
"""

import cv2
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TinyCNNRecognizer")

try:
    import tensorflow as tf
    TFLITE_AVAILABLE = True
    logger.info("✓ TensorFlow Lite loaded")
except ImportError:
    TFLITE_AVAILABLE = False
    logger.error("❌ TensorFlow Lite not installed")


class TinyCNNRecognizer:
    """
    Face recognizer using TinyCNN model
    Handles binary classification with camera-specific enhancements
    """
    
    def __init__(self, model_path="models/tinycnn_mrdavid.tflite", 
                 david_threshold=0.88,
                 min_confidence=0.80,
                 enable_quality_check=True):
        """
        Initialize recognizer
        
        Args:
            model_path: Path to .tflite model file
            david_threshold: Threshold to recognize as David (0.0-1.0)
                           CRITICAL: Higher value = stricter recognition
                           0.93 = Good balance for live camera
                           0.95 = Very strict (fewer false positives)
                           0.88 = Too permissive (causes false positives on real faces!)
            min_confidence: Minimum confidence for any prediction (reject if too uncertain)
            enable_quality_check: Enable image quality validation
        """
        self.model_path = model_path
        self.david_threshold = david_threshold
        self.min_confidence = min_confidence
        self.enable_quality_check = enable_quality_check
        self.model_available = False
        self.interpreter = None
        
        if not TFLITE_AVAILABLE:
            logger.error("TensorFlow Lite not available")
            return
        
        try:
            logger.info(f"Loading model: {model_path}")
            
            # Load TFLite model
            self.interpreter = tf.lite.Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()
            
            # Get input/output details
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            # Get expected input shape
            self.input_shape = self.input_details[0]['shape']
            self.input_height = self.input_shape[1]
            self.input_width = self.input_shape[2]
            
            logger.info(f"✓ Model loaded - Input size: {self.input_width}x{self.input_height}")
            logger.info(f"✓ David threshold: {self.david_threshold:.2f} (STRICT for camera)")
            logger.info(f"✓ Min confidence: {self.min_confidence:.2f}")
            logger.info(f"✓ Quality check: {'ENABLED' if self.enable_quality_check else 'DISABLED'}")
            
            self.model_available = True
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            self.model_available = False
    
    def check_image_quality(self, face_img):
        """
        Check if image quality is good enough for recognition
        
        Args:
            face_img: BGR face image from OpenCV
            
        Returns:
            Tuple (is_good_quality, quality_score, issues)
        """
        if not self.enable_quality_check:
            return True, 1.0, []
        
        issues = []
        quality_score = 1.0
        
        # Check 1: Image size
        h, w = face_img.shape[:2]
        if h < 40 or w < 40:
            issues.append("too_small")
            quality_score *= 0.5
        
        # Check 2: Brightness (avoid too dark or too bright)
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        
        if brightness < 40:
            issues.append("too_dark")
            quality_score *= 0.6
        elif brightness > 220:
            issues.append("too_bright")
            quality_score *= 0.7
        
        # Check 3: Blur detection (Laplacian variance)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        if laplacian_var < 50:
            issues.append("too_blurry")
            quality_score *= 0.5
        
        # Check 4: Contrast
        contrast = gray.std()
        if contrast < 20:
            issues.append("low_contrast")
            quality_score *= 0.7
        
        is_good = quality_score >= 0.3 and len(issues) < 3
        
        return is_good, quality_score, issues
    
    def preprocess(self, face_img):
        """
        Preprocess face image for model input
        Enhanced for camera frames with normalization
        
        Args:
            face_img: BGR face image from OpenCV
            
        Returns:
            Preprocessed numpy array ready for model
        """
        # Resize to model input size
        img = cv2.resize(face_img, (self.input_width, self.input_height), 
                        interpolation=cv2.INTER_AREA)  # Better for downscaling
        
        # Convert BGR to RGB (CRITICAL!)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Enhanced preprocessing for camera frames
        # Apply slight histogram equalization for better generalization
        img_yuv = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
        
        # Normalize to [0, 1] range
        img = img.astype(np.float32) / 255.0
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        return img
    
    def recognize(self, face_img):
        """
        Recognize face and return if it's Mr. David
        Enhanced with quality checks and stricter validation
        
        Args:
            face_img: BGR face image from OpenCV
            
        Returns:
            Tuple (is_mrdavid, confidence, quality_info)
            - is_mrdavid: True if recognized as David, False otherwise
            - confidence: Confidence score (0.0-1.0)
            - quality_info: Dictionary with quality metrics
        """
        if not self.model_available:
            return False, 0.0, {"error": "model_not_available"}
        
        try:
            # Quality check
            is_good_quality, quality_score, issues = self.check_image_quality(face_img)
            
            quality_info = {
                "good_quality": is_good_quality,
                "quality_score": quality_score,
                "issues": issues
            }
            
            if not is_good_quality:
                logger.warning(f"⚠️ Poor image quality: {issues} (score: {quality_score:.2f})")
                # Return as unknown if quality is too poor
                return False, 0.0, quality_info
            
            # Preprocess image
            input_data = self.preprocess(face_img)
            
            # Run inference
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            
            # Get output
            output = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
            
            # Handle different output formats
            if len(output) == 2:
                # Binary classification with 2 outputs [class_0_prob, class_1_prob]
                class_0_prob = output[0]  # Unknown person probability
                class_1_prob = output[1]  # David probability
                
                # David is class 1
                david_confidence = float(class_1_prob)
                
            elif len(output) == 1:
                # Single output (sigmoid) - value close to 1 = David, close to 0 = Unknown
                david_confidence = float(output[0])
                
            else:
                logger.warning(f"Unexpected output shape: {output.shape}")
                return False, 0.0, quality_info
            
            # CRITICAL DECISION LOGIC with multiple checks
            
            # Check 1: Minimum confidence threshold (reject if too uncertain)
            if david_confidence < self.min_confidence and (1 - david_confidence) < self.min_confidence:
                logger.warning(f"⚠️ Very uncertain prediction: {david_confidence:.3f}")
                quality_info["rejection_reason"] = "too_uncertain"
                return False, david_confidence, quality_info
            
            # Check 2: David threshold (main decision)
            is_mrdavid = david_confidence >= self.david_threshold
            
            # Check 3: Additional validation for borderline cases
            if 0.85 <= david_confidence < self.david_threshold:
                # Borderline case - be extra cautious
                logger.warning(f"⚠️ Borderline case: {david_confidence:.3f} (threshold: {self.david_threshold:.3f})")
                is_mrdavid = False  # Reject borderline cases to avoid false positives
                quality_info["rejection_reason"] = "borderline_confidence"
            
            # Logging with detail
            decision = "DAVID ✓" if is_mrdavid else "UNKNOWN ✗"
            logger.info(f"Recognition: confidence={david_confidence:.4f} | threshold={self.david_threshold:.2f} | quality={quality_score:.2f} | Result={decision}")
            
            quality_info["david_confidence"] = david_confidence
            quality_info["decision"] = decision
            
            return is_mrdavid, david_confidence, quality_info
            
        except Exception as e:
            logger.error(f"Recognition error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False, 0.0, {"error": str(e)}
    
    def recognize_with_details(self, face_img):
        """
        Recognize face and return detailed results
        
        Args:
            face_img: BGR face image from OpenCV
            
        Returns:
            Dictionary with:
            - is_mrdavid: bool - True if David, False if unknown
            - confidence: float - Confidence score (0.0-1.0)
            - label: str - "Mr. David" or "Unknown"
            - quality_info: dict - Image quality metrics
        """
        is_mrdavid, confidence, quality_info = self.recognize(face_img)
        
        return {
            'is_mrdavid': is_mrdavid,
            'confidence': confidence,
            'label': "Mr. David" if is_mrdavid else "Unknown",
            'quality_info': quality_info
        }
    
    def get_model_info(self):
        """Get model information"""
        if not self.model_available:
            return "Model not loaded"
        
        return {
            'model_path': self.model_path,
            'input_size': f"{self.input_width}x{self.input_height}",
            'david_threshold': self.david_threshold,
            'min_confidence': self.min_confidence,
            'quality_check': self.enable_quality_check,
            'available': self.model_available
        }


# Test function
if __name__ == "__main__":
    print("="*70)
    print("TinyCNN Face Recognizer - Test (Camera-Enhanced)")
    print("="*70)
    
    # Initialize recognizer with STRICT settings for camera
    recognizer = TinyCNNRecognizer(
        model_path="models/tinycnn_mrdavid.tflite",
        david_threshold=0.88,  # STRICT threshold for live camera
        min_confidence=0.80,    # Minimum confidence to make any decision
        enable_quality_check=True  # Enable quality validation
    )
    
    if recognizer.model_available:
        print("\n✓ Model loaded successfully!")
        print(f"✓ Input size: {recognizer.input_width}x{recognizer.input_height}")
        print(f"✓ David threshold: {recognizer.david_threshold} (STRICT)")
        print(f"✓ Min confidence: {recognizer.min_confidence}")
        print("\nModel Info:")
        print(recognizer.get_model_info())
        
        # Test with webcam
        print("\nStarting webcam test...")
        print("Press 'q' to quit")
        
        cap = cv2.VideoCapture(0)
        
        # Try to load face detector for testing
        try:
            from blazeface_detector import BlazeFaceDetector
            detector = BlazeFaceDetector()
            print("✓ Using BlazeFace detector")
        except:
            detector = None
            print("⚠ Using OpenCV face detection")
        
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Detect faces
            if detector:
                detections = detector.detect(frame)
            else:
                # OpenCV fallback
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier(
                    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                detections = [(x, y, x+w, y+h) for (x, y, w, h) in faces]
            
            # Process each face
            for bbox in detections:
                x1, y1, x2, y2 = bbox
                
                # Extract face
                face_img = frame[y1:y2, x1:x2]
                
                if face_img.size > 0:
                    # Recognize (every 5th frame to reduce load)
                    if frame_count % 5 == 0:
                        result = recognizer.recognize_with_details(face_img)
                        
                        is_mrdavid = result['is_mrdavid']
                        confidence = result['confidence']
                        label = result['label']
                        quality_info = result['quality_info']
                        
                        # Draw result
                        if is_mrdavid:
                            # GREEN for David
                            color = (0, 255, 0)
                            text = f"Welcome Mr. David! ({confidence:.2%})"
                        else:
                            # RED for Unknown
                            color = (0, 0, 255)
                            text = f"Unknown Person ({confidence:.2%})"
                        
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                        cv2.putText(frame, text, (x1, y1-10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                        
                        # Show quality info
                        if 'quality_score' in quality_info:
                            quality_text = f"Q: {quality_info['quality_score']:.2f}"
                            cv2.putText(frame, quality_text, (x1, y2+25),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.imshow('Face Recognition Test', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
    else:
        print("\n❌ Model not available")
        print("Make sure the model file exists:")
        print("  models/tinycnn_mrdavid.tflite")
