#!/usr/bin/env python3
"""
Face Collection Tool
Easily collect face images for training Mr. David recognition model
Uses BlazeFace detector to automatically crop and save faces
"""

import cv2
import os
import time
from pathlib import Path
from datetime import datetime
import argparse

try:
    from blazeface_detector import BlazeFaceDetector
    DETECTOR_AVAILABLE = True
except ImportError:
    print("⚠ BlazeFace detector not available, using OpenCV fallback")
    DETECTOR_AVAILABLE = False


class FaceCollector:
    """Collect face images for training"""
    
    def __init__(self, person_name="mrdavid", output_dir="dataset"):
        """
        Initialize face collector
        
        Args:
            person_name: Name of person (mrdavid or others)
            output_dir: Output directory for collected images
        """
        self.person_name = person_name
        self.output_dir = Path(output_dir) / person_name
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.collected_count = 0
        self.camera = None
        self.detector = None
        
        print("=" * 70)
        print("Face Collection Tool")
        print("=" * 70)
        print(f"Person: {person_name}")
        print(f"Output: {self.output_dir}")
        print()
    
    def initialize_camera(self):
        """Initialize camera"""
        print("📷 Opening camera...")
        self.camera = cv2.VideoCapture(0)
        
        if not self.camera.isOpened():
            print("❌ Failed to open camera")
            return False
        
        # Set camera properties
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.camera.set(cv2.CAP_PROP_FPS, 30)
        
        print("✓ Camera opened successfully")
        return True
    
    def initialize_detector(self):
        """Initialize face detector"""
        if DETECTOR_AVAILABLE:
            try:
                print("Loading BlazeFace detector...")
                self.detector = BlazeFaceDetector(
                    model_path="models/blazeface.tflite",
                    confidence_threshold=0.7
                )
                print("✓ BlazeFace detector loaded")
                return True
            except Exception as e:
                print(f"⚠ BlazeFace failed: {e}")
                print("Using OpenCV fallback")
        
        # OpenCV fallback
        self.detector = None
        return True
    
    def detect_faces(self, frame):
        """Detect faces in frame"""
        faces = []
        
        if self.detector is not None:
            # Use BlazeFace
            detections = self.detector.detect(frame)
            faces = [(x1, y1, x2-x1, y2-y1) for x1, y1, x2, y2 in detections]
        else:
            # OpenCV fallback
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        return faces
    
    def collect_faces(self, target_count=100, auto_mode=False, interval=0.5):
        """
        Collect face images
        
        Args:
            target_count: Number of images to collect
            auto_mode: Automatically capture faces
            interval: Seconds between auto captures
        """
        if not self.initialize_camera():
            return
        
        self.initialize_detector()
        
        print()
        print("=" * 70)
        print("COLLECTION MODE")
        print("=" * 70)
        print(f"Target: {target_count} images")
        print(f"Mode: {'Auto' if auto_mode else 'Manual'}")
        if auto_mode:
            print(f"Interval: {interval}s between captures")
        print()
        print("Controls:")
        print("  SPACE - Capture face (manual mode)")
        print("  Q - Quit")
        print("  A - Toggle auto mode")
        print()
        print("Tips:")
        print("  - Move your head to different angles")
        print("  - Change facial expressions")
        print("  - Vary lighting (move closer/farther from light)")
        print("  - Try with/without glasses")
        print("=" * 70)
        print()
        
        last_capture_time = 0
        auto_enabled = auto_mode
        
        while True:
            ret, frame = self.camera.read()
            if not ret:
                print("Failed to read frame")
                break
            
            # Detect faces
            faces = self.detect_faces(frame)
            
            # Draw detection boxes and info
            display_frame = frame.copy()
            
            for face in faces:
                if len(face) == 4:
                    x, y, w, h = face
                    
                    # Draw rectangle
                    color = (0, 255, 0) if len(faces) == 1 else (0, 255, 255)
                    cv2.rectangle(display_frame, (x, y), (x+w, y+h), color, 2)
                    
                    # Add label
                    label = f"Face {self.collected_count}/{target_count}"
                    cv2.putText(display_frame, label, (x, y-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Status overlay
            status_text = f"Collected: {self.collected_count}/{target_count}"
            mode_text = "Mode: AUTO" if auto_enabled else "Mode: MANUAL"
            
            cv2.putText(display_frame, status_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(display_frame, mode_text, (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, 
                       (0, 255, 0) if auto_enabled else (255, 0, 0), 2)
            
            if len(faces) == 0:
                cv2.putText(display_frame, "No face detected", (10, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            elif len(faces) > 1:
                cv2.putText(display_frame, "Multiple faces - please ensure only one person", 
                           (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
            
            # Show frame
            cv2.imshow('Face Collection', display_frame)
            
            # Auto capture
            current_time = time.time()
            if auto_enabled and len(faces) == 1:
                if current_time - last_capture_time >= interval:
                    self.save_face(frame, faces[0])
                    last_capture_time = current_time
                    
                    if self.collected_count >= target_count:
                        print(f"\n✅ Target reached! Collected {self.collected_count} images")
                        break
            
            # Handle keyboard
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\nStopping collection...")
                break
            elif key == ord(' ') and not auto_enabled:
                # Manual capture
                if len(faces) == 1:
                    self.save_face(frame, faces[0])
                elif len(faces) == 0:
                    print("⚠ No face detected")
                else:
                    print("⚠ Multiple faces detected - ensure only one person")
            elif key == ord('a'):
                # Toggle auto mode
                auto_enabled = not auto_enabled
                print(f"Auto mode: {'ON' if auto_enabled else 'OFF'}")
                last_capture_time = current_time
        
        # Cleanup
        self.camera.release()
        cv2.destroyAllWindows()
        
        print()
        print("=" * 70)
        print(f"✅ Collection complete!")
        print(f"   Total images: {self.collected_count}")
        print(f"   Saved to: {self.output_dir}")
        print("=" * 70)
    
    def save_face(self, frame, face):
        """Save detected face"""
        x, y, w, h = face
        
        # Add margin around face
        margin = int(0.2 * max(w, h))
        x1 = max(0, x - margin)
        y1 = max(0, y - margin)
        x2 = min(frame.shape[1], x + w + margin)
        y2 = min(frame.shape[0], y + h + margin)
        
        # Crop face
        face_img = frame[y1:y2, x1:x2]
        
        # Resize to consistent size
        face_img = cv2.resize(face_img, (160, 160))
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{self.person_name}_{timestamp}.jpg"
        filepath = self.output_dir / filename
        
        # Save
        cv2.imwrite(str(filepath), face_img)
        self.collected_count += 1
        
        print(f"[{self.collected_count:3d}] Saved: {filename}")


def main():
    parser = argparse.ArgumentParser(description='Collect face images for training')
    parser.add_argument('--person', type=str, default='mrdavid',
                       choices=['mrdavid', 'others'],
                       help='Person to collect (mrdavid or others)')
    parser.add_argument('--output', type=str, default='dataset',
                       help='Output directory (default: dataset/)')
    parser.add_argument('--count', type=int, default=100,
                       help='Number of images to collect (default: 100)')
    parser.add_argument('--auto', action='store_true',
                       help='Enable auto-capture mode')
    parser.add_argument('--interval', type=float, default=0.5,
                       help='Seconds between auto captures (default: 0.5)')
    
    args = parser.parse_args()
    
    print()
    print("=" * 70)
    print("🎯 FACE COLLECTION TOOL")
    print("=" * 70)
    print()
    print("This tool helps you collect face images for training.")
    print()
    print("Recommended workflow:")
    print("  1. Collect Mr. David's faces (100+ images)")
    print("     python3 collect_faces.py --person mrdavid --count 100 --auto")
    print()
    print("  2. Collect other people's faces (100+ images)")
    print("     python3 collect_faces.py --person others --count 100 --auto")
    print()
    print("  3. Train the model")
    print("     python3 train_model.py --epochs 50")
    print()
    print("=" * 70)
    print()
    
    # Create collector
    collector = FaceCollector(person_name=args.person, output_dir=args.output)
    
    # Start collection
    try:
        collector.collect_faces(
            target_count=args.count,
            auto_mode=args.auto,
            interval=args.interval
        )
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()