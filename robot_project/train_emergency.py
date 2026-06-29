#!/usr/bin/env python3
"""
EMERGENCY ULTRA-CONSERVATIVE TRAINER
====================================

EXTREME MEASURES FOR STUBBORN COLLAPSE:
✅ Learning rate: 0.000005 (100x lower than original!)
✅ Simpler architecture (less prone to collapse)
✅ Extremely aggressive monitoring (every epoch)
✅ Visual debugging output
✅ Forced diversity in predictions
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import cv2
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path
from sklearn.model_selection import train_test_split
import sys

print(f"TensorFlow: {tf.__version__}")
print()


class EmergencyTrainer:
    """Last resort trainer for extreme collapse cases"""
    
    def __init__(self, dataset_dir='dataset', img_size=96):
        self.dataset_dir = Path(dataset_dir)
        self.img_size = img_size
        self.model = None
        
        print("=" * 70)
        print("🚨 EMERGENCY ULTRA-CONSERVATIVE TRAINER")
        print("=" * 70)
        print("EXTREME MEASURES:")
        print("  - Learning rate: 0.000005 (VERY LOW)")
        print("  - Simple architecture (fewer parameters)")
        print("  - Aggressive monitoring (every epoch)")
        print("  - Maximum safeguards")
        print("=" * 70)
        print()
    
    def load_dataset(self):
        """Load dataset with detailed logging"""
        print("📁 Loading dataset...")
        
        images, labels, paths = [], [], []
        
        # Load Mr. David
        mrdavid_dir = self.dataset_dir / "mrdavid"
        if mrdavid_dir.exists():
            print(f"\nLoading Mr. David from: {mrdavid_dir}")
            count = 0
            for img_file in sorted(mrdavid_dir.glob('*.jpg')) + sorted(mrdavid_dir.glob('*.png')):
                img = cv2.imread(str(img_file))
                if img is not None and img.shape[0] >= 30 and img.shape[1] >= 30:
                    img = cv2.resize(img, (self.img_size, self.img_size))
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    images.append(img)
                    labels.append(1)
                    paths.append(str(img_file))
                    count += 1
                    if count <= 5:
                        print(f"  ✓ Loaded: {img_file.name} → Label: 1 (David)")
            print(f"  Total David: {count}")
        
        # Load Others
        others_dir = self.dataset_dir / "others"
        if others_dir.exists():
            print(f"\nLoading Others from: {others_dir}")
            count = 0
            for img_file in sorted(others_dir.glob('*.jpg')) + sorted(others_dir.glob('*.png')):
                img = cv2.imread(str(img_file))
                if img is not None and img.shape[0] >= 30 and img.shape[1] >= 30:
                    img = cv2.resize(img, (self.img_size, self.img_size))
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    images.append(img)
                    labels.append(0)
                    paths.append(str(img_file))
                    count += 1
                    if count <= 5:
                        print(f"  ✓ Loaded: {img_file.name} → Label: 0 (Others)")
            print(f"  Total Others: {count}")
        
        if len(images) == 0:
            print("\n❌ No images found!")
            return None, None, None, None, None, None
        
        images = np.array(images, dtype=np.float32) / 255.0
        labels = np.array(labels, dtype=np.float32)
        
        print()
        print("=" * 70)
        print("DATASET SUMMARY")
        print("=" * 70)
        david_count = int(np.sum(labels == 1))
        others_count = int(np.sum(labels == 0))
        print(f"Total: {len(images)} images")
        print(f"  Mr. David (label=1): {david_count}")
        print(f"  Others (label=0): {others_count}")
        print(f"  Balance: {david_count/(david_count+others_count)*100:.1f}% David")
        print("=" * 70)
        print()
        
        # Split
        X_train, X_val, y_train, y_val, paths_train, paths_val = train_test_split(
            images, labels, paths, test_size=0.15, random_state=42, stratify=labels
        )
        
        print("Split:")
        print(f"  Train: {len(X_train)} ({int(np.sum(y_train==1))} David, {int(np.sum(y_train==0))} Others)")
        print(f"  Val: {len(X_val)} ({int(np.sum(y_val==1))} David, {int(np.sum(y_val==0))} Others)")
        print()
        
        return X_train, X_val, y_train, y_val, paths_train, paths_val
    
    def build_simple_model(self):
        """Build VERY simple model (less prone to collapse)"""
        print("🏗️ Building simple model...")
        
        inputs = layers.Input(shape=(self.img_size, self.img_size, 3))
        
        # Very simple architecture
        x = layers.Conv2D(16, 3, padding='same', activation='relu')(inputs)
        x = layers.MaxPooling2D(2)(x)
        x = layers.Dropout(0.1)(x)
        
        x = layers.Conv2D(32, 3, padding='same', activation='relu')(x)
        x = layers.MaxPooling2D(2)(x)
        x = layers.Dropout(0.1)(x)
        
        x = layers.Conv2D(64, 3, padding='same', activation='relu')(x)
        x = layers.MaxPooling2D(2)(x)
        x = layers.Dropout(0.15)(x)
        
        x = layers.GlobalAveragePooling2D()(x)
        
        x = layers.Dense(64, activation='relu')(x)
        x = layers.Dropout(0.2)(x)
        
        # Output with explicit bias initialization
        outputs = layers.Dense(1, activation='sigmoid',
                              bias_initializer=keras.initializers.Constant(0.0))(x)
        
        model = keras.Model(inputs=inputs, outputs=outputs)
        
        print(f"✓ Model: {model.count_params():,} parameters (SIMPLE!)")
        print()
        
        return model
    
    def create_ultra_balanced_batches(self, X, y, batch_size=8):
        """Create perfectly balanced batches"""
        david_idx = np.where(y == 1)[0]
        others_idx = np.where(y == 0)[0]
        
        # Make equal
        min_count = min(len(david_idx), len(others_idx))
        max_count = max(len(david_idx), len(others_idx))
        
        if len(david_idx) < max_count:
            david_idx = np.random.choice(david_idx, size=max_count, replace=True)
        if len(others_idx) < max_count:
            others_idx = np.random.choice(others_idx, size=max_count, replace=True)
        
        # Interleave for perfect balance
        all_idx = []
        for i in range(len(david_idx)):
            all_idx.append(david_idx[i])
            all_idx.append(others_idx[i])
        
        all_idx = np.array(all_idx)
        np.random.shuffle(all_idx)
        
        X_balanced = X[all_idx]
        y_balanced = y[all_idx]
        
        dataset = tf.data.Dataset.from_tensor_slices((X_balanced, y_balanced))
        dataset = dataset.batch(batch_size)
        dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        return dataset
    
    class AggressiveMonitor(keras.callbacks.Callback):
        """Monitor EVERY epoch with detailed output"""
        
        def __init__(self, X_val, y_val, trainer):
            super().__init__()
            self.X_val = X_val
            self.y_val = y_val
            self.trainer = trainer
            self.best_val_acc = 0
            self.collapse_count = 0
        
        def on_epoch_end(self, epoch, logs=None):
            # Predict
            y_pred_prob = self.model.predict(self.X_val, verbose=0).flatten()
            y_pred = (y_pred_prob > 0.5).astype(int)
            
            # Per-class
            david_mask = self.y_val == 1
            others_mask = self.y_val == 0
            
            david_acc = np.mean(y_pred[david_mask] == 1)
            others_acc = np.mean(y_pred[others_mask] == 0)
            overall_acc = np.mean(y_pred == self.y_val)
            
            # Prediction distribution
            n_predict_david = np.sum(y_pred == 1)
            n_predict_others = np.sum(y_pred == 0)
            
            print(f"\n  📊 Epoch {epoch+1} Detailed Results:")
            print(f"     Overall: {overall_acc:.1%}")
            print(f"     David: {david_acc:.1%} (correct: {int(david_acc*np.sum(david_mask))}/{int(np.sum(david_mask))})")
            print(f"     Others: {others_acc:.1%} (correct: {int(others_acc*np.sum(others_mask))}/{int(np.sum(others_mask))})")
            print(f"     Predictions: {n_predict_david} David, {n_predict_others} Others")
            print(f"     Avg confidence: David {np.mean(y_pred_prob[david_mask]):.3f}, Others {np.mean(1-y_pred_prob[others_mask]):.3f}")
            
            # Check for collapse
            if david_acc < 0.1 or others_acc < 0.1:
                self.collapse_count += 1
                print(f"     ⚠️  WARNING: Collapse detected! (count: {self.collapse_count})")
                
                if self.collapse_count >= 5:
                    print(f"\n❌ STOPPING: Persistent collapse")
                    print(f"   Model is predicting {n_predict_david} David vs {n_predict_others} Others")
                    print(f"   This indicates a fundamental training issue")
                    self.model.stop_training = True
            else:
                self.collapse_count = 0
                
            # Check if improving
            if overall_acc > self.best_val_acc:
                self.best_val_acc = overall_acc
                print(f"     ✓ New best accuracy: {overall_acc:.1%}")
    
    def train(self, epochs=200, batch_size=8):
        """Train with extreme conservatism"""
        
        print("🚀 Starting emergency training...")
        print()
        
        data = self.load_dataset()
        if data[0] is None:
            sys.exit(1)
        
        X_train, X_val, y_train, y_val, paths_train, paths_val = data
        
        # Save val paths for later inspection
        self.val_paths = paths_val
        self.y_val = y_val
        
        # Build simple model
        self.model = self.build_simple_model()
        
        # Calculate class weights
        n_david = np.sum(y_train == 1)
        n_others = np.sum(y_train == 0)
        total = len(y_train)
        
        david_weight = total / (2 * n_david)
        others_weight = total / (2 * n_others)
        
        class_weight_dict = {
            0: float(others_weight),
            1: float(david_weight)
        }
        
        print("Class Weights:")
        print(f"  David: {david_weight:.3f}")
        print(f"  Others: {others_weight:.3f}")
        print()
        
        # EXTREME conservative settings
        self.model.compile(
            optimizer=keras.optimizers.Adam(
                learning_rate=0.000005,  # EXTREMELY low!
                clipnorm=0.5  # Aggressive clipping
            ),
            loss=keras.losses.BinaryCrossentropy(label_smoothing=0.15),
            metrics=['accuracy']
        )
        
        # Minimal augmentation
        aug = keras.Sequential([
            layers.RandomFlip("horizontal"),
            layers.RandomContrast(0.1),
        ])
        
        # Balanced datasets
        train_ds = self.create_ultra_balanced_batches(X_train, y_train, batch_size)
        train_ds = train_ds.map(lambda x, y: (aug(x, training=True), y))
        
        val_ds = tf.data.Dataset.from_tensor_slices((X_val, y_val))
        val_ds = val_ds.batch(batch_size)
        
        Path("models").mkdir(exist_ok=True)
        
        callbacks = [
            self.AggressiveMonitor(X_val, y_val, self),
            keras.callbacks.ModelCheckpoint(
                'models/emergency_best.h5',
                monitor='val_accuracy',
                save_best_only=True,
                verbose=0
            ),
        ]
        
        print("=" * 70)
        print("EMERGENCY TRAINING START")
        print("=" * 70)
        print(f"Learning rate: 0.000005 (EXTREMELY LOW)")
        print(f"Epochs: {epochs}")
        print(f"Architecture: Simple (less prone to collapse)")
        print("=" * 70)
        print()
        
        history = self.model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs,
            callbacks=callbacks,
            class_weight=class_weight_dict,
            verbose=2  # Less verbose
        )
        
        print()
        print("=" * 70)
        print("TRAINING COMPLETE")
        print("=" * 70)
        print()
        
        # Final evaluation
        self.evaluate_and_diagnose(X_train, y_train, X_val, y_val)
        
        # Export
        self.export_model()
        
        return history
    
    def evaluate_and_diagnose(self, X_train, y_train, X_val, y_val):
        """Detailed evaluation with diagnosis"""
        
        print("=" * 70)
        print("FINAL EVALUATION")
        print("=" * 70)
        print()
        
        # Training
        y_train_pred_prob = self.model.predict(X_train, verbose=0).flatten()
        y_train_pred = (y_train_pred_prob > 0.5).astype(int)
        
        train_acc = np.mean(y_train_pred == y_train)
        train_david_acc = np.mean(y_train_pred[y_train==1] == 1)
        train_others_acc = np.mean(y_train_pred[y_train==0] == 0)
        
        print("TRAINING SET:")
        print(f"  Overall: {train_acc:.1%}")
        print(f"  David: {train_david_acc:.1%}")
        print(f"  Others: {train_others_acc:.1%}")
        print()
        
        # Validation
        y_val_pred_prob = self.model.predict(X_val, verbose=0).flatten()
        y_val_pred = (y_val_pred_prob > 0.5).astype(int)
        
        val_acc = np.mean(y_val_pred == y_val)
        val_david_acc = np.mean(y_val_pred[y_val==1] == 1)
        val_others_acc = np.mean(y_val_pred[y_val==0] == 0)
        
        print("VALIDATION SET:")
        print(f"  Overall: {val_acc:.1%}")
        print(f"  David: {val_david_acc:.1%}")
        print(f"  Others: {val_others_acc:.1%}")
        print()
        
        # Diagnosis
        print("=" * 70)
        print("DIAGNOSIS")
        print("=" * 70)
        
        if val_david_acc < 0.2 and val_others_acc > 0.8:
            print("❌ COLLAPSE: Model only predicts Others")
            print("\nPossible causes:")
            print("1. David images look too similar to Others")
            print("2. David images have poor quality")
            print("3. Mislabeled images")
            print("\nShow me some misclassified David images:")
            self.show_mistakes(y_val, y_val_pred, y_val_pred_prob, is_david=True)
            
        elif val_others_acc < 0.2 and val_david_acc > 0.8:
            print("❌ REVERSE COLLAPSE: Model only predicts David")
            print("\nShow me some misclassified Others images:")
            self.show_mistakes(y_val, y_val_pred, y_val_pred_prob, is_david=False)
            
        elif val_acc < 0.65:
            print("⚠️  LOW ACCURACY: Model struggling with both classes")
            print("\nSuggestions:")
            print("1. Collect more data")
            print("2. Improve image quality")
            print("3. Train much longer (500+ epochs)")
            
        elif val_acc >= 0.75:
            print("✅ WORKING! Model learned both classes")
            if val_acc >= 0.85:
                print("🎉 EXCELLENT PERFORMANCE!")
        
        print()
    
    def show_mistakes(self, y_true, y_pred, y_pred_prob, is_david=True):
        """Show which images are being misclassified"""
        
        if is_david:
            mask = y_true == 1
            mistakes_idx = np.where((y_true == 1) & (y_pred == 0))[0]
            label_str = "David"
        else:
            mask = y_true == 0
            mistakes_idx = np.where((y_true == 0) & (y_pred == 1))[0]
            label_str = "Others"
        
        if len(mistakes_idx) == 0:
            print(f"  ✓ No mistakes on {label_str}!")
            return
        
        print(f"\n  Misclassified {label_str} images (showing first 5):")
        for i, idx in enumerate(mistakes_idx[:5]):
            path = self.val_paths[idx]
            conf = y_pred_prob[idx]
            print(f"    {i+1}. {Path(path).name} (predicted as {'David' if not is_david else 'Others'}, conf: {conf:.3f})")
    
    def export_model(self):
        """Export model"""
        print("📦 Exporting...")
        
        try:
            converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
            tflite_model = converter.convert()
            
            Path("models/emergency.tflite").write_bytes(tflite_model)
            print("✅ Exported: models/emergency.tflite")
        except:
            self.model.save('models/emergency.h5')
            print("✅ Saved: models/emergency.h5")
        
        print()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='dataset')
    parser.add_argument('--img-size', type=int, default=96)
    parser.add_argument('--epochs', type=int, default=200)
    parser.add_argument('--batch-size', type=int, default=8)
    args = parser.parse_args()
    
    print("=" * 70)
    print("🚨 EMERGENCY ULTRA-CONSERVATIVE TRAINING")
    print("=" * 70)
    print()
    
    trainer = EmergencyTrainer(args.dataset, args.img_size)
    trainer.train(args.epochs, args.batch_size)


if __name__ == "__main__":
    main()
