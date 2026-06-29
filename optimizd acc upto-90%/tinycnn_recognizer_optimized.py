#!/usr/bin/env python3
"""
TinyCNN Face Recognizer - OPTIMIZED VERSION
Recognizes Mr. David using an optimized lightweight CNN model
Compatible with main.py and blazeface_detector.py
Updated for 112x112 input size and better preprocessing
"""

import cv2
import numpy as np
import logging
import os

# Try to import TFLite runtime (lightweight), fallback to full TensorFlow
try:
    from tflite_runtime.interpreter import Interpreter
    print("✓ Using TFLite Runtime (lightweight)")
except (ImportError, ModuleNotFoundError):
    try:
        import tensorflow as tf
        Interpreter = tf.lite.Interpreter
        print("✓ Using TensorFlow Lite")
    except (ImportError, ModuleNotFoundError):
        print("\n" + "=" * 70)
        print("ERROR: Neither tflite_runtime nor tensorflow is installed!")
        print("=" * 70)
        print("\nPlease install TensorFlow:")
        print("  pip3 install tensorflow --break-system-packages")
        print("=" * 70)
        exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TinyCNNRecognizer:
    """TinyCNN face recognizer using TensorFlow Lite - Optimized"""
    
    def __init__(self, model_path="models/tinycnn_mrdavid.tflite", confidence_threshold=0.80):
        """
        Initialize TinyCNN recognizer
        
        Args:
            model_path: Path to TinyCNN TFLite model
            confidence_threshold: Minimum confidence for positive recognition (0.0-1.0)
                                 Default 0.80 for better precision with optimized model
        """
        self.logger = logger
        self.confidence_threshold = confidence_threshold
        self.model_path = model_path
        self.model_available = False
        
        # Check if model exists
        if not os.path.exists(model_path):
            self.logger.warning("=" * 70)
            self.logger.warning(f"❌ MODEL NOT FOUND: {model_path}")
            self.logger.warning("=" * 70)
            self.logger.warning("")
            self.logger.warning("To train the optimized model:")
            self.logger.warning("  1. Collect Mr. David's face images:")
            self.logger.warning("     python3 collect_faces.py --person mrdavid --count 120 --auto")
            self.logger.warning("")
            self.logger.warning("  2. Collect other people's faces:")
            self.logger.warning("     python3 collect_faces.py --person others --count 120 --auto")
            self.logger.warning("")
            self.logger.warning("  3. Train the optimized model:")
            self.logger.warning("     python3 train_model_optimized.py --epochs 100 --img-size 112")
            self.logger.warning("")
            self.logger.warning("=" * 70)
            return
        
        try:
            # Load TFLite model
            self.logger.info(f"Loading TinyCNN model: {model_path}")
            self.interpreter = Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()
            
            # Get input/output details
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            # Model input shape
            self.input_shape = self.input_details[0]['shape']
            self.input_height = self.input_shape[1]
            self.input_width = self.input_shape[2]
            
            # Class labels
            self.class_labels = ["Others", "Mr. David"]
            self.model_available = True
            
            self.logger.info(f"✓ TinyCNN loaded successfully")
            self.logger.info(f"  Input size: {self.input_width}x{self.input_height}")
            self.logger.info(f"  Confidence threshold: {confidence_threshold}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load model: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            self.model_available = False
    
    def preprocess_face(self, face_image):
        """
        Preprocess face image for recognition with enhanced preprocessing
        
        Args:
            face_image: Cropped face image (BGR from OpenCV)
            
        Returns:
            Preprocessed tensor or None if error
        """
        try:
            if face_image is None or face_image.size == 0:
                return None
            
            # Validate image
            if len(face_image.shape) != 3:
                self.logger.warning("Invalid face image shape")
                return None
            
            # Check minimum size
            if face_image.shape[0] < 20 or face_image.shape[1] < 20:
                self.logger.warning(f"Face too small: {face_image.shape}")
                return None
            
            # Resize to model input size
            resized = cv2.resize(face_image, (self.input_width, self.input_height),
                               interpolation=cv2.INTER_AREA)  # Better for downsampling
            
            # Apply histogram equalization for consistent lighting
            # This improves robustness across different lighting conditions
            img_yuv = cv2.cvtColor(resized, cv2.COLOR_BGR2YUV)
            img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
            resized = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
            
            # Convert BGR to RGB
            rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            
            # Normalize to [0, 1]
            normalized = rgb.astype(np.float32) / 255.0
            
            # Add batch dimension
            input_tensor = np.expand_dims(normalized, axis=0)
            
            return input_tensor
            
        except Exception as e:
            self.logger.error(f"Preprocessing error: {e}")
            return None
    
    def recognize(self, face_image):
        """
        Recognize if face is Mr. David
        
        Args:
            face_image: Cropped face image (BGR from OpenCV)
            
        Returns:
            Tuple (is_target, confidence)
            - is_target: True if Mr. David, False otherwise
            - confidence: Recognition confidence (0.0 to 1.0)
        """
        # Check if model is available
        if not self.model_available:
            self.logger.debug("Model not available")
            return False, 0.0
        
        try:
            # Preprocess face
            input_tensor = self.preprocess_face(face_image)
            
            if input_tensor is None:
                return False, 0.0
            
            # Run inference
            self.interpreter.set_tensor(self.input_details[0]['index'], input_tensor)
            self.interpreter.invoke()
            
            # Get output
            output = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
            
            # Handle different output formats
            if len(output) == 2:
                # Two-class output: [Others, Mr. David]
                # Apply softmax if not already applied
                exp_scores = np.exp(output - np.max(output))
                probabilities = exp_scores / exp_scores.sum()
                
                # Confidence for Mr. David (class 1)
                mrdavid_confidence = float(probabilities[1])
            else:
                # Single output (sigmoid)
                mrdavid_confidence = float(output[0])
                # Apply sigmoid if needed
                if mrdavid_confidence > 1.0 or mrdavid_confidence < 0.0:
                    mrdavid_confidence = 1.0 / (1.0 + np.exp(-mrdavid_confidence))
            
            # Clamp to [0, 1]
            mrdavid_confidence = max(0.0, min(1.0, mrdavid_confidence))
            
            # Check threshold
            is_mrdavid = mrdavid_confidence >= self.confidence_threshold
            
            # Log results
            if is_mrdavid:
                self.logger.info(f"✓ Recognized Mr. David (confidence: {mrdavid_confidence:.2%})")
            else:
                self.logger.debug(f"Not Mr. David (confidence: {mrdavid_confidence:.2%})")
            
            return is_mrdavid, mrdavid_confidence
            
        except Exception as e:
            self.logger.error(f"Recognition error: {e}")
            import traceback
            self.logger.debug(traceback.format_exc())
            return False, 0.0
    
    def recognize_with_details(self, face_image):
        """Get detailed recognition results"""
        is_target, confidence = self.recognize(face_image)
        
        return {
            'is_mrdavid': is_target,
            'confidence': confidence,
            'label': self.class_labels[1] if is_target else self.class_labels[0],
            'threshold': self.confidence_threshold,
            'model_available': self.model_available
        }
    
    def set_threshold(self, new_threshold):
        """Update confidence threshold"""
        if 0.0 <= new_threshold <= 1.0:
            self.confidence_threshold = new_threshold
            self.logger.info(f"Confidence threshold updated to {new_threshold}")
        else:
            self.logger.warning(f"Invalid threshold {new_threshold}")
    
    def calibrate_threshold(self, test_images, test_labels, target_metric='f1'):
        """
        Calibrate confidence threshold on a validation set
        
        Args:
            test_images: List of face images
            test_labels: List of labels (1 for Mr. David, 0 for others)
            target_metric: 'precision', 'recall', or 'f1' (default)
            
        Returns:
            Optimal threshold value
        """
        if not self.model_available:
            self.logger.warning("Model not available for calibration")
            return self.confidence_threshold
        
        self.logger.info("Calibrating threshold...")
        
        # Test thresholds from 0.5 to 0.95
        thresholds = np.arange(0.5, 0.96, 0.05)
        best_score = 0
        best_threshold = self.confidence_threshold
        
        for thresh in thresholds:
            self.confidence_threshold = thresh
            
            correct = 0
            tp = fp = tn = fn = 0
            
            for img, label in zip(test_images, test_labels):
                is_david, conf = self.recognize(img)
                pred = 1 if is_david else 0
                
                if pred == label:
                    correct += 1
                
                if pred == 1 and label == 1:
                    tp += 1
                elif pred == 1 and label == 0:
                    fp += 1
                elif pred == 0 and label == 0:
                    tn += 1
                else:
                    fn += 1
            
            # Calculate metrics
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            # Select metric
            if target_metric == 'precision':
                score = precision
            elif target_metric == 'recall':
                score = recall
            else:
                score = f1
            
            if score > best_score:
                best_score = score
                best_threshold = thresh
        
        self.confidence_threshold = best_threshold
        self.logger.info(f"Optimal threshold: {best_threshold:.2f} ({target_metric}: {best_score:.2%})")
        
        return best_threshold


def test_recognizer():
    """Test the recognizer"""
    print("=" * 70)
    print("OPTIMIZED TINYCNN RECOGNIZER TEST")
    print("=" * 70)
    print()
    
    # Initialize with optimized threshold
    recognizer = TinyCNNRecognizer(
        model_path="models/tinycnn_mrdavid.tflite",
        confidence_threshold=0.80  # Higher threshold for better precision
    )
    
    if recognizer.model_available:
        print("✓ Recognizer ready!")
        print(f"  Model: {recognizer.model_path}")
        print(f"  Input size: {recognizer.input_width}x{recognizer.input_height}")
        print(f"  Threshold: {recognizer.confidence_threshold}")
        print()
        
        # Test with dummy image
        print("Testing with dummy image...")
        test_img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        is_david, conf = recognizer.recognize(test_img)
        print(f"  Result: {is_david}, Confidence: {conf:.2%}")
        print()
        
        print("💡 Tips for best performance:")
        print("  - Ensure good lighting when capturing faces")
        print("  - Keep face centered and upright")
        print("  - Train with 100+ diverse images per class")
        print("  - Adjust threshold based on your precision/recall needs:")
        print("    * Lower (0.70-0.75): More sensitive, may have false positives")
        print("    * Higher (0.85-0.90): More strict, fewer false positives")
        
    else:
        print("❌ Model not available")
        print("\nFollow the optimized training workflow:")
        print("  1. python3 collect_faces.py --person mrdavid --count 120 --auto")
        print("  2. python3 collect_faces.py --person others --count 120 --auto")
        print("  3. python3 train_model_optimized.py --epochs 100 --img-size 112")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_recognizer()
