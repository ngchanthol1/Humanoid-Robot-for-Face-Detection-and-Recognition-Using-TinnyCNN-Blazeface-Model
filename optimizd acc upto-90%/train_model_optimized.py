#!/usr/bin/env python3
"""
TinyCNN Model Training Script - OPTIMIZED FOR >90% ACCURACY
Trains a lightweight CNN to recognize Mr. David
Enhanced with better architecture and training strategies
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import cv2
import os
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.utils import class_weight
import argparse
import json
import matplotlib.pyplot as plt


class TinyCNNTrainer:
    """Train TinyCNN face recognition model"""
    
    def __init__(self, dataset_dir="dataset", img_size=112):
        """Initialize trainer - using 112x112 for better feature extraction"""
        self.dataset_dir = Path(dataset_dir)
        self.img_size = img_size
        self.model = None
        
        print("=" * 70)
        print("🎯 TinyCNN Face Recognition Trainer - OPTIMIZED")
        print("=" * 70)
        print(f"Dataset: {self.dataset_dir}")
        print(f"Image size: {self.img_size}x{self.img_size}")
        print()
    
    def load_dataset(self, apply_histogram_equalization=True):
        """Load and preprocess dataset with enhanced preprocessing"""
        print("📁 Loading dataset...")
        print()
        
        images = []
        labels = []
        
        # Load Mr. David images (label = 1)
        mrdavid_dir = self.dataset_dir / "mrdavid"
        mrdavid_count = 0
        
        if mrdavid_dir.exists():
            print(f"Loading Mr. David from: {mrdavid_dir}")
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
                for img_file in mrdavid_dir.glob(ext):
                    img = cv2.imread(str(img_file))
                    if img is not None:
                        # Enhanced preprocessing
                        img = cv2.resize(img, (self.img_size, self.img_size))
                        
                        # Apply histogram equalization for better contrast
                        if apply_histogram_equalization:
                            img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
                            img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
                            img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
                        
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        images.append(img)
                        labels.append(1)
                        mrdavid_count += 1
            print(f"  ✓ Loaded {mrdavid_count} images")
        else:
            print(f"  ❌ Directory not found: {mrdavid_dir}")
            print("     Run: python3 collect_faces.py --person mrdavid --count 100 --auto")
        
        # Load others (label = 0)
        others_dir = self.dataset_dir / "others"
        others_count = 0
        
        if others_dir.exists():
            print(f"Loading Others from: {others_dir}")
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
                for img_file in others_dir.glob(ext):
                    img = cv2.imread(str(img_file))
                    if img is not None:
                        # Enhanced preprocessing
                        img = cv2.resize(img, (self.img_size, self.img_size))
                        
                        # Apply histogram equalization
                        if apply_histogram_equalization:
                            img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
                            img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
                            img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
                        
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        images.append(img)
                        labels.append(0)
                        others_count += 1
            print(f"  ✓ Loaded {others_count} images")
        else:
            print(f"  ❌ Directory not found: {others_dir}")
            print("     Run: python3 collect_faces.py --person others --count 100 --auto")
        
        if len(images) == 0:
            print("\n" + "=" * 70)
            print("❌ NO IMAGES FOUND!")
            print("=" * 70)
            print("\nPlease collect face images first:")
            print("  1. python3 collect_faces.py --person mrdavid --count 100 --auto")
            print("  2. python3 collect_faces.py --person others --count 100 --auto")
            print("=" * 70)
            return None, None
        
        # Convert to arrays and normalize
        images = np.array(images, dtype=np.float32) / 255.0
        labels = np.array(labels)
        
        print()
        print("=" * 70)
        print("DATASET SUMMARY")
        print("=" * 70)
        print(f"Total images: {len(images)}")
        print(f"  Mr. David: {np.sum(labels == 1)}")
        print(f"  Others: {np.sum(labels == 0)}")
        print("=" * 70)
        print()
        
        # Check minimum requirements
        if mrdavid_count < 30 or others_count < 30:
            print("⚠ WARNING: Few images detected!")
            print("  Recommended: 80-150 images per class for >90% accuracy")
            print("  Current setup may result in lower accuracy")
            print()
        
        return images, labels
    
    def build_model(self):
        """Build optimized TinyCNN architecture for >90% accuracy"""
        print("🏗️ Building Optimized TinyCNN model...")
        
        model = keras.Sequential([
            # Input
            layers.Input(shape=(self.img_size, self.img_size, 3)),
            
            # Block 1 - Initial feature extraction
            layers.Conv2D(32, (3, 3), activation='relu', padding='same',
                         kernel_initializer='he_normal'),
            layers.BatchNormalization(),
            layers.Conv2D(32, (3, 3), activation='relu', padding='same',
                         kernel_initializer='he_normal'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.2),
            
            # Block 2 - Deeper features
            layers.Conv2D(64, (3, 3), activation='relu', padding='same',
                         kernel_initializer='he_normal'),
            layers.BatchNormalization(),
            layers.Conv2D(64, (3, 3), activation='relu', padding='same',
                         kernel_initializer='he_normal'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.3),
            
            # Block 3 - High-level features
            layers.Conv2D(128, (3, 3), activation='relu', padding='same',
                         kernel_initializer='he_normal'),
            layers.BatchNormalization(),
            layers.Conv2D(128, (3, 3), activation='relu', padding='same',
                         kernel_initializer='he_normal'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.4),
            
            # Block 4 - Additional depth for better accuracy
            layers.Conv2D(256, (3, 3), activation='relu', padding='same',
                         kernel_initializer='he_normal'),
            layers.BatchNormalization(),
            layers.GlobalAveragePooling2D(),  # Better than Flatten
            
            # Dense layers with L2 regularization
            layers.Dense(512, activation='relu',
                        kernel_regularizer=keras.regularizers.l2(0.001)),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            
            layers.Dense(256, activation='relu',
                        kernel_regularizer=keras.regularizers.l2(0.001)),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            
            layers.Dense(128, activation='relu',
                        kernel_regularizer=keras.regularizers.l2(0.001)),
            layers.Dropout(0.4),
            
            # Output: 2 classes [Others, Mr. David]
            layers.Dense(2, activation='softmax')
        ])
        
        # Compile with custom metrics
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.0003),
            loss='sparse_categorical_crossentropy',
            metrics=[
                'accuracy',
                keras.metrics.Precision(name='precision'),
                keras.metrics.Recall(name='recall')
            ]
        )
        
        self.model = model
        
        print("\nOptimized Model Architecture:")
        print("=" * 70)
        model.summary()
        print("=" * 70)
        print()
        
        return model
    
    def create_augmentation_pipeline(self):
        """Create aggressive data augmentation pipeline"""
        return keras.Sequential([
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.15),  # ±15 degrees
            layers.RandomZoom(0.15),  # ±15% zoom
            layers.RandomTranslation(0.1, 0.1),  # ±10% shift
            layers.RandomContrast(0.2),
            layers.RandomBrightness(0.2),
        ], name="augmentation")
    
    def train(self, epochs=100, batch_size=16, validation_split=0.2):
        """Train the model with optimized strategy"""
        print("🚀 Starting optimized training...")
        print()
        
        # Load dataset
        images, labels = self.load_dataset()
        
        if images is None:
            return None
        
        # Split dataset with stratification
        X_train, X_val, y_train, y_val = train_test_split(
            images, labels,
            test_size=validation_split,
            random_state=42,
            stratify=labels
        )
        
        print("Dataset Split:")
        print(f"  Training: {len(X_train)} ({np.sum(y_train==1)} David, {np.sum(y_train==0)} Others)")
        print(f"  Validation: {len(X_val)} ({np.sum(y_val==1)} David, {np.sum(y_val==0)} Others)")
        print()
        
        # Build model
        if self.model is None:
            self.build_model()
        
        # Data augmentation
        augmentation = self.create_augmentation_pipeline()
        
        # Create models directory
        Path("models").mkdir(exist_ok=True)
        
        # Calculate class weights for balanced training
        class_weights = class_weight.compute_class_weight(
            'balanced',
            classes=np.unique(y_train),
            y=y_train
        )
        class_weight_dict = {i: weight for i, weight in enumerate(class_weights)}
        
        print(f"Class weights: {class_weight_dict}")
        print()
        
        # Enhanced callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=20,
                restore_best_weights=True,
                verbose=1,
                min_delta=0.001
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=8,
                min_lr=1e-7,
                verbose=1,
                min_delta=0.001
            ),
            keras.callbacks.ModelCheckpoint(
                'models/tinycnn_best.keras',
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),
            # Cosine annealing learning rate schedule
            keras.callbacks.LearningRateScheduler(
                lambda epoch: 0.0003 * (0.95 ** epoch)
            )
        ]
        
        # Train with augmentation applied on-the-fly
        print("=" * 70)
        print("TRAINING STARTED - Target: >90% Accuracy")
        print("=" * 70)
        print()
        
        # Create a custom training loop with augmentation
        train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
        train_dataset = train_dataset.shuffle(buffer_size=len(X_train))
        train_dataset = train_dataset.batch(batch_size)
        train_dataset = train_dataset.map(
            lambda x, y: (augmentation(x, training=True), y),
            num_parallel_calls=tf.data.AUTOTUNE
        )
        train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)
        
        val_dataset = tf.data.Dataset.from_tensor_slices((X_val, y_val))
        val_dataset = val_dataset.batch(batch_size)
        val_dataset = val_dataset.prefetch(tf.data.AUTOTUNE)
        
        history = self.model.fit(
            train_dataset,
            validation_data=val_dataset,
            epochs=epochs,
            callbacks=callbacks,
            class_weight=class_weight_dict,
            verbose=1
        )
        
        print()
        print("=" * 70)
        print("✅ TRAINING COMPLETE")
        print("=" * 70)
        print()
        
        # Detailed evaluation
        print("📊 Final Evaluation:")
        results = self.model.evaluate(X_val, y_val, verbose=0, return_dict=True)
        
        print(f"  Validation Loss: {results['loss']:.4f}")
        print(f"  Validation Accuracy: {results['accuracy']*100:.2f}%")
        print(f"  Precision: {results['precision']*100:.2f}%")
        print(f"  Recall: {results['recall']*100:.2f}%")
        
        # F1 Score
        f1 = 2 * (results['precision'] * results['recall']) / (results['precision'] + results['recall'] + 1e-7)
        print(f"  F1 Score: {f1*100:.2f}%")
        print()
        
        # Per-class accuracy
        y_pred = np.argmax(self.model.predict(X_val, verbose=0), axis=1)
        
        david_mask = y_val == 1
        if np.any(david_mask):
            david_acc = np.mean(y_pred[david_mask] == y_val[david_mask])
            print(f"  Mr. David Accuracy: {david_acc*100:.2f}%")
        
        others_mask = y_val == 0
        if np.any(others_mask):
            others_acc = np.mean(y_pred[others_mask] == y_val[others_mask])
            print(f"  Others Accuracy: {others_acc*100:.2f}%")
        print()
        
        # Check if target achieved
        if results['accuracy'] >= 0.90:
            print("🎉 TARGET ACHIEVED: >90% Validation Accuracy!")
        else:
            print(f"⚠ Target not reached. Current: {results['accuracy']*100:.2f}%")
            print("  Tips to improve:")
            print("  - Collect more diverse training images (150+ per class)")
            print("  - Ensure good lighting variety in images")
            print("  - Include different angles and expressions")
            print("  - Train for more epochs (100-150)")
        print()
        
        # Save training plot
        self.plot_training_history(history)
        
        return history
    
    def plot_training_history(self, history):
        """Plot and save detailed training history"""
        try:
            plt.figure(figsize=(15, 5))
            
            # Accuracy
            plt.subplot(1, 3, 1)
            plt.plot(history.history['accuracy'], label='Train', linewidth=2)
            plt.plot(history.history['val_accuracy'], label='Validation', linewidth=2)
            plt.axhline(y=0.9, color='r', linestyle='--', label='90% Target')
            plt.title('Model Accuracy', fontsize=12, fontweight='bold')
            plt.xlabel('Epoch')
            plt.ylabel('Accuracy')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Loss
            plt.subplot(1, 3, 2)
            plt.plot(history.history['loss'], label='Train', linewidth=2)
            plt.plot(history.history['val_loss'], label='Validation', linewidth=2)
            plt.title('Model Loss', fontsize=12, fontweight='bold')
            plt.xlabel('Epoch')
            plt.ylabel('Loss')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Precision & Recall
            plt.subplot(1, 3, 3)
            if 'precision' in history.history:
                plt.plot(history.history['precision'], label='Train Precision', linewidth=2)
                plt.plot(history.history['val_precision'], label='Val Precision', linewidth=2)
            if 'recall' in history.history:
                plt.plot(history.history['recall'], label='Train Recall', linewidth=2, linestyle='--')
                plt.plot(history.history['val_recall'], label='Val Recall', linewidth=2, linestyle='--')
            plt.title('Precision & Recall', fontsize=12, fontweight='bold')
            plt.xlabel('Epoch')
            plt.ylabel('Score')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('models/training_history.png', dpi=150, bbox_inches='tight')
            print("📊 Training plot saved: models/training_history.png")
            print()
        except Exception as e:
            print(f"⚠ Could not save plot: {e}")
    
    def export_tflite(self, output_path="models/tinycnn_mrdavid.tflite", quantize=True):
        """Export to TFLite with optimization"""
        print("=" * 70)
        print("📦 Exporting to TensorFlow Lite...")
        print("=" * 70)
        print()
        
        if self.model is None:
            print("❌ No model to export")
            return
        
        # Convert
        converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
        
        if quantize:
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            # Add representative dataset for better quantization
            def representative_dataset():
                for _ in range(100):
                    yield [np.random.random((1, self.img_size, self.img_size, 3)).astype(np.float32)]
            converter.representative_dataset = representative_dataset
        
        tflite_model = converter.convert()
        
        # Save
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(tflite_model)
        
        size_kb = len(tflite_model) / 1024
        
        print(f"✓ Model exported!")
        print(f"  Path: {output_path}")
        print(f"  Size: {size_kb:.2f} KB")
        print()
        
        # Metadata
        metadata = {
            'model_type': 'TinyCNN Face Recognizer - Optimized',
            'target_person': 'Mr. David',
            'input_size': self.img_size,
            'classes': ['Others', 'Mr. David'],
            'size_kb': round(size_kb, 2),
            'optimization': 'quantized' if quantize else 'none'
        }
        
        metadata_path = output_path.replace('.tflite', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return output_path


def main():
    parser = argparse.ArgumentParser(description='Train optimized TinyCNN face recognition model')
    parser.add_argument('--dataset', type=str, default='dataset',
                       help='Path to dataset directory')
    parser.add_argument('--img-size', type=int, default=112,
                       help='Image size (default: 112 for better accuracy)')
    parser.add_argument('--epochs', type=int, default=100,
                       help='Number of training epochs (100+ recommended)')
    parser.add_argument('--batch-size', type=int, default=16,
                       help='Batch size for training')
    parser.add_argument('--output', type=str, default='models/tinycnn_mrdavid.tflite',
                       help='Output TFLite model path')
    
    args = parser.parse_args()
    
    print()
    print("=" * 70)
    print("🎯 TinyCNN FACE RECOGNITION TRAINER - OPTIMIZED FOR >90%")
    print("=" * 70)
    print()
    
    # Check dataset
    if not Path(args.dataset).exists():
        print(f"❌ Dataset not found: {args.dataset}")
        print()
        print("Please collect face images first:")
        print("  1. python3 collect_faces.py --person mrdavid --count 120 --auto")
        print("  2. python3 collect_faces.py --person others --count 120 --auto")
        print()
        print("💡 Tip: More images (100-150 per class) = Better accuracy!")
        print()
        return
    
    # Train
    trainer = TinyCNNTrainer(dataset_dir=args.dataset, img_size=args.img_size)
    history = trainer.train(epochs=args.epochs, batch_size=args.batch_size)
    
    if history is None:
        return
    
    # Export
    trainer.export_tflite(output_path=args.output)
    
    print("=" * 70)
    print("✅ ALL DONE!")
    print("=" * 70)
    print()
    print("Next steps:")
    print(f"  1. Model ready: {args.output}")
    print("  2. Update recognizer to use new image size (112x112)")
    print("  3. Test with: python3 main.py")
    print("  4. Adjust threshold in tinycnn_recognizer.py if needed (try 0.80-0.85)")
    print()


if __name__ == "__main__":
    main()
