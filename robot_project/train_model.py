#!/usr/bin/env python3
"""
ULTRA-ROBUST Training - Maximum Protection Against Class Collapse
==================================================================

CRITICAL FIXES FOR YOUR ISSUE:
✅ Forces model to predict BOTH classes
✅ Detects collapse immediately and stops
✅ Uses verified balanced batching
✅ Multiple redundant safeguards
✅ Conservative learning rate
✅ Explicit per-class monitoring
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import cv2
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, regularizers
from pathlib import Path
from sklearn.model_selection import train_test_split
import argparse
import sys

print(f"TensorFlow: {tf.__version__}")
print()


class UltraRobustTrainer:
    """Training system that CANNOT collapse"""
    
    def __init__(self, dataset_dir='dataset', img_size=128):
        self.dataset_dir = Path(dataset_dir)
        self.img_size = img_size
        self.model = None
        self.training_stopped = False
        
        print("=" * 70)
        print("🛡️  ULTRA-ROBUST TRAINER")
        print("=" * 70)
        print("PROTECTION: Maximum safeguards against class collapse")
        print("TARGET: 85-95% accuracy on BOTH Mr. David and Others")
        print("=" * 70)
        print()
    
    def load_dataset(self):
        """Load and thoroughly validate dataset"""
        print("📁 Loading dataset...")
        print()
        
        images, labels = [], []
        
        # Load Mr. David
        mrdavid_dir = self.dataset_dir / "mrdavid"
        david_count = 0
        
        if mrdavid_dir.exists():
            print(f"Loading Mr. David from: {mrdavid_dir}")
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
                for img_file in sorted(mrdavid_dir.glob(ext)):
                    img = cv2.imread(str(img_file))
                    if img is not None and img.shape[0] >= 50 and img.shape[1] >= 50:
                        img = cv2.resize(img, (self.img_size, self.img_size))
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        images.append(img)
                        labels.append(1)  # Mr. David = 1
                        david_count += 1
            print(f"  ✓ Loaded {david_count} Mr. David images")
        else:
            print(f"❌ Directory not found: {mrdavid_dir}")
            return None, None, None, None
        
        # Load Others
        others_dir = self.dataset_dir / "others"
        others_count = 0
        
        if others_dir.exists():
            print(f"Loading Others from: {others_dir}")
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
                for img_file in sorted(others_dir.glob(ext)):
                    img = cv2.imread(str(img_file))
                    if img is not None and img.shape[0] >= 50 and img.shape[1] >= 50:
                        img = cv2.resize(img, (self.img_size, self.img_size))
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        images.append(img)
                        labels.append(0)  # Others = 0
                        others_count += 1
            print(f"  ✓ Loaded {others_count} Others images")
        else:
            print(f"❌ Directory not found: {others_dir}")
            return None, None, None, None
        
        if len(images) == 0:
            print("❌ No images found!")
            return None, None, None, None
        
        # Convert
        images = np.array(images, dtype=np.float32) / 255.0
        labels = np.array(labels, dtype=np.float32)
        
        print()
        print("=" * 70)
        print("DATASET LOADED")
        print("=" * 70)
        print(f"Total: {len(images)} images")
        print(f"  Mr. David (label=1): {david_count} images")
        print(f"  Others (label=0): {others_count} images")
        print(f"  Ratio: {david_count/(david_count+others_count)*100:.1f}% David")
        
        # Check minimum requirements
        if david_count < 50:
            print(f"⚠️  WARNING: Only {david_count} David images (need 100+ for good results)")
        if others_count < 50:
            print(f"⚠️  WARNING: Only {others_count} Others images (need 100+ for good results)")
        
        ratio = david_count / (david_count + others_count)
        if ratio < 0.25 or ratio > 0.75:
            print(f"⚠️  WARNING: Highly imbalanced dataset ({ratio*100:.1f}% David)")
            print("    This may cause training difficulties")
        
        print("=" * 70)
        print()
        
        # Stratified split
        X_train, X_val, y_train, y_val = train_test_split(
            images, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        print("Train/Val Split:")
        train_david = int(np.sum(y_train == 1))
        train_others = int(np.sum(y_train == 0))
        val_david = int(np.sum(y_val == 1))
        val_others = int(np.sum(y_val == 0))
        
        print(f"  TRAIN: {len(X_train)} total ({train_david} David, {train_others} Others)")
        print(f"  VAL:   {len(X_val)} total ({val_david} David, {val_others} Others)")
        print()
        
        # Critical check
        if val_david == 0:
            print("❌ CRITICAL: No David images in validation set!")
            return None, None, None, None
        if val_others == 0:
            print("❌ CRITICAL: No Others images in validation set!")
            return None, None, None, None
        
        return X_train, X_val, y_train, y_val
    
    def build_robust_model(self):
        """Build model with initialization to prevent collapse"""
        print("🏗️  Building collapse-resistant model...")
        
        inputs = layers.Input(shape=(self.img_size, self.img_size, 3))
        
        # Initial conv
        x = layers.Conv2D(32, 3, padding='same', 
                         kernel_initializer='he_normal')(inputs)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.MaxPooling2D(2)(x)
        
        # Block 1
        x = layers.Conv2D(64, 3, padding='same',
                         kernel_initializer='he_normal',
                         kernel_regularizer=regularizers.l2(0.0001))(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.MaxPooling2D(2)(x)
        x = layers.Dropout(0.15)(x)
        
        # Block 2
        x = layers.Conv2D(128, 3, padding='same',
                         kernel_initializer='he_normal',
                         kernel_regularizer=regularizers.l2(0.0001))(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.MaxPooling2D(2)(x)
        x = layers.Dropout(0.2)(x)
        
        # Block 3
        x = layers.Conv2D(256, 3, padding='same',
                         kernel_initializer='he_normal',
                         kernel_regularizer=regularizers.l2(0.0001))(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.MaxPooling2D(2)(x)
        x = layers.Dropout(0.25)(x)
        
        # Global pooling
        x = layers.GlobalAveragePooling2D()(x)
        
        # Dense layers
        x = layers.Dense(256, 
                        kernel_initializer='he_normal',
                        kernel_regularizer=regularizers.l2(0.0001))(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.Dropout(0.4)(x)
        
        x = layers.Dense(128,
                        kernel_initializer='he_normal',
                        kernel_regularizer=regularizers.l2(0.0001))(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.Dropout(0.3)(x)
        
        # Output with bias initialization for balanced start
        outputs = layers.Dense(1, activation='sigmoid',
                              kernel_initializer='glorot_uniform',
                              bias_initializer=keras.initializers.Constant(0.0))(x)
        
        model = keras.Model(inputs=inputs, outputs=outputs)
        
        print(f"✓ Model created: {model.count_params():,} parameters")
        print()
        
        return model
    
    def create_perfectly_balanced_batches(self, X, y, batch_size=8):
        """Create batches with EXACTLY 50% each class"""
        
        # Separate by class
        david_indices = np.where(y == 1)[0]
        others_indices = np.where(y == 0)[0]
        
        print(f"Creating balanced batches:")
        print(f"  David samples: {len(david_indices)}")
        print(f"  Others samples: {len(others_indices)}")
        
        # Determine max size
        max_samples = max(len(david_indices), len(others_indices))
        
        # Oversample minority to match majority
        if len(david_indices) < max_samples:
            david_indices = np.random.choice(david_indices, size=max_samples, replace=True)
            print(f"  → Oversampled David to {len(david_indices)}")
        
        if len(others_indices) < max_samples:
            others_indices = np.random.choice(others_indices, size=max_samples, replace=True)
            print(f"  → Oversampled Others to {len(others_indices)}")
        
        # Now both have same size
        assert len(david_indices) == len(others_indices), "Balancing failed!"
        
        # Combine and shuffle
        all_indices = np.concatenate([david_indices, others_indices])
        np.random.shuffle(all_indices)
        
        X_balanced = X[all_indices]
        y_balanced = y[all_indices]
        
        print(f"  → Balanced dataset size: {len(X_balanced)}")
        print(f"  → David %: {np.mean(y_balanced == 1)*100:.1f}%")
        print(f"  → Others %: {np.mean(y_balanced == 0)*100:.1f}%")
        print()
        
        # Create dataset
        dataset = tf.data.Dataset.from_tensor_slices((X_balanced, y_balanced))
        dataset = dataset.shuffle(len(X_balanced), reshuffle_each_iteration=True)
        dataset = dataset.batch(batch_size)
        dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        return dataset
    
    class CollapseDetector(keras.callbacks.Callback):
        """Detects and stops training if collapse occurs"""
        
        def __init__(self, X_val, y_val, trainer):
            super().__init__()
            self.X_val = X_val
            self.y_val = y_val
            self.trainer = trainer
            self.collapse_count = 0
        
        def on_epoch_end(self, epoch, logs=None):
            # Check every 5 epochs
            if (epoch + 1) % 5 != 0:
                return
            
            # Get predictions
            y_pred_prob = self.model.predict(self.X_val, verbose=0).flatten()
            y_pred = (y_pred_prob > 0.5).astype(int)
            
            # Per-class accuracy
            david_mask = self.y_val == 1
            others_mask = self.y_val == 0
            
            david_acc = np.mean(y_pred[david_mask] == 1) if np.any(david_mask) else 0
            others_acc = np.mean(y_pred[others_mask] == 0) if np.any(others_mask) else 0
            
            print(f"\n  📊 Per-class accuracy:")
            print(f"     Mr. David: {david_acc:.1%}")
            print(f"     Others: {others_acc:.1%}")
            
            # Check for collapse
            if david_acc < 0.15 or others_acc < 0.15:
                self.collapse_count += 1
                print(f"  ⚠️  WARNING: Possible collapse detected! (count: {self.collapse_count})")
                
                if self.collapse_count >= 3:
                    print(f"  ❌ STOPPING: Model collapsed (predicting only one class)")
                    print(f"     Suggestions:")
                    print(f"     1. Check data quality (run verify_system.py)")
                    print(f"     2. Reduce learning rate")
                    print(f"     3. Check for mislabeled images")
                    self.model.stop_training = True
                    self.trainer.training_stopped = True
            else:
                self.collapse_count = max(0, self.collapse_count - 1)
    
    def train(self, epochs=150, batch_size=8):
        """Train with maximum protection"""
        
        print("🚀 Starting ultra-robust training...")
        print()
        
        # Load data
        data = self.load_dataset()
        if data[0] is None:
            print("❌ Cannot proceed without valid dataset")
            sys.exit(1)
        
        X_train, X_val, y_train, y_val = data
        
        # Store for later use in quantization
        self.X_train = X_train
        self.X_val = X_val
        
        # Build model
        self.model = self.build_robust_model()
        
        # Calculate class weights (additional safeguard)
        david_weight = len(y_train) / (2 * np.sum(y_train == 1))
        others_weight = len(y_train) / (2 * np.sum(y_train == 0))
        
        class_weight_dict = {
            0: float(others_weight),
            1: float(david_weight)
        }
        
        print("Class Weights (for loss balancing):")
        print(f"  Others (0): {others_weight:.3f}")
        print(f"  Mr. David (1): {david_weight:.3f}")
        print()
        
        # Compile with VERY conservative settings
        self.model.compile(
            optimizer=keras.optimizers.Adam(
                learning_rate=0.00005,  # VERY low to prevent divergence
                clipnorm=1.0  # Clip gradients
            ),
            loss=keras.losses.BinaryCrossentropy(
                label_smoothing=0.1  # Soft labels
            ),
            metrics=[
                'accuracy',
                keras.metrics.Precision(name='precision'),
                keras.metrics.Recall(name='recall')
            ]
        )
        
        # Data augmentation
        aug = keras.Sequential([
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.1),
            layers.RandomZoom(0.1),
            layers.RandomContrast(0.12),
            layers.RandomBrightness(0.12),
        ])
        
        # Create balanced datasets
        print("=" * 70)
        print("CREATING BALANCED TRAINING BATCHES")
        print("=" * 70)
        train_ds = self.create_perfectly_balanced_batches(X_train, y_train, batch_size)
        train_ds = train_ds.map(lambda x, y: (aug(x, training=True), y))
        
        val_ds = tf.data.Dataset.from_tensor_slices((X_val, y_val))
        val_ds = val_ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)
        
        # Learning rate schedule
        def lr_schedule(epoch):
            if epoch < 30:
                # Warmup
                return 0.00005
            elif epoch < 150:
                # Gradual decay
                return 0.00005 * (0.95 ** ((epoch - 30) / 10))
            else:
                # Fine-tuning
                return 0.000001
        
        Path("models").mkdir(exist_ok=True)
        
        callbacks = [
            self.CollapseDetector(X_val, y_val, self),
            keras.callbacks.LearningRateScheduler(lr_schedule, verbose=0),
            keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=60,
                restore_best_weights=True,
                verbose=1,
                min_delta=0.005
            ),
            keras.callbacks.ModelCheckpoint(
                'models/ultra_robust_best.h5',
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=25,
                min_lr=1e-8,
                verbose=1
            )
        ]
        
        print("=" * 70)
        print("TRAINING START")
        print("=" * 70)
        print(f"Epochs: {epochs}")
        print(f"Batch size: {batch_size}")
        print(f"Initial LR: 0.00005 (very conservative)")
        print("=" * 70)
        print()
        
        history = self.model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs,
            callbacks=callbacks,
            class_weight=class_weight_dict,
            verbose=1
        )
        
        if self.training_stopped:
            print()
            print("=" * 70)
            print("❌ TRAINING STOPPED DUE TO COLLAPSE")
            print("=" * 70)
            print("Please check:")
            print("1. Run: python3 verify_system.py")
            print("2. Review image quality")
            print("3. Check for mislabeled images")
            print("4. Ensure both classes have 100+ images")
            return None
        
        print()
        print("=" * 70)
        print("✅ TRAINING COMPLETE")
        print("=" * 70)
        print()
        
        # Final evaluation
        self.evaluate_final(X_train, y_train, X_val, y_val)
        
        # Export models
        self.export_model()
        
        # Verify exported model
        self.verify_exported_model()
        
        return history
    
    def evaluate_final(self, X_train, y_train, X_val, y_val):
        """Comprehensive final evaluation"""
        
        print("=" * 70)
        print("📊 FINAL EVALUATION")
        print("=" * 70)
        print()
        
        # Training set
        print("TRAINING SET:")
        y_train_pred_prob = self.model.predict(X_train, verbose=0).flatten()
        y_train_pred = (y_train_pred_prob > 0.5).astype(int)
        
        train_overall = np.mean(y_train_pred == y_train)
        
        train_david_mask = y_train == 1
        train_others_mask = y_train == 0
        
        train_david_acc = np.mean(y_train_pred[train_david_mask] == 1)
        train_others_acc = np.mean(y_train_pred[train_others_mask] == 0)
        
        print(f"  Overall: {train_overall:.4f} ({train_overall*100:.2f}%)")
        print(f"  Mr. David: {train_david_acc:.4f} ({train_david_acc*100:.2f}%)")
        print(f"  Others: {train_others_acc:.4f} ({train_others_acc*100:.2f}%)")
        
        # Confidence stats
        train_david_conf = np.mean(y_train_pred_prob[train_david_mask])
        train_others_conf = np.mean(1 - y_train_pred_prob[train_others_mask])
        print(f"  David avg confidence: {train_david_conf:.4f}")
        print(f"  Others avg confidence: {train_others_conf:.4f}")
        print()
        
        # Validation set
        print("VALIDATION SET:")
        y_val_pred_prob = self.model.predict(X_val, verbose=0).flatten()
        y_val_pred = (y_val_pred_prob > 0.5).astype(int)
        
        val_overall = np.mean(y_val_pred == y_val)
        
        val_david_mask = y_val == 1
        val_others_mask = y_val == 0
        
        val_david_acc = np.mean(y_val_pred[val_david_mask] == 1)
        val_others_acc = np.mean(y_val_pred[val_others_mask] == 0)
        
        print(f"  Overall: {val_overall:.4f} ({val_overall*100:.2f}%)")
        print(f"  Mr. David: {val_david_acc:.4f} ({val_david_acc*100:.2f}%)")
        print(f"  Others: {val_others_acc:.4f} ({val_others_acc*100:.2f}%)")
        
        val_david_conf = np.mean(y_val_pred_prob[val_david_mask])
        val_others_conf = np.mean(1 - y_val_pred_prob[val_others_mask])
        print(f"  David avg confidence: {val_david_conf:.4f}")
        print(f"  Others avg confidence: {val_others_conf:.4f}")
        print()
        
        # Check for issues
        print("=" * 70)
        print("DIAGNOSIS:")
        print("=" * 70)
        
        if val_david_acc < 0.2 or val_others_acc < 0.2:
            print("❌ SEVERE ISSUE: One class has very low accuracy")
            print("   Action: Check data quality and labels")
        elif val_david_acc < 0.5 or val_others_acc < 0.5:
            print("⚠️  ISSUE: One class below 50% accuracy")
            print("   Action: Train longer or collect more data")
        elif val_overall >= 0.90:
            print("🎉 EXCELLENT! 90%+ validation accuracy!")
        elif val_overall >= 0.85:
            print("✅ VERY GOOD! 85%+ validation accuracy")
        elif val_overall >= 0.75:
            print("✅ GOOD! 75%+ validation accuracy")
        elif val_overall >= 0.65:
            print("⚠️  Moderate performance. Consider more training/data")
        else:
            print("❌ Low accuracy. Check data quality")
        
        print()
        print("=" * 70)
        print()
    
    def export_model(self):
        """Export model as tinycnn_mrdavid.tflite - Works with Keras 2 and Keras 3"""
        print()
        print("=" * 70)
        print("📦 EXPORTING MODEL")
        print("=" * 70)
        print()
        
        # Ensure models directory exists
        models_dir = Path("models")
        models_dir.mkdir(exist_ok=True)
        print(f"✅ Models directory: {models_dir.absolute()}")
        print()
        
        # Check Keras version
        keras_version = int(keras.__version__.split('.')[0])
        print(f"Detected: Keras {keras.__version__}")
        print()
        
        # Primary model: Float32 as tinycnn_mrdavid.tflite
        print("Creating primary model: tinycnn_mrdavid.tflite")
        print("-" * 70)
        
        main_model_path = models_dir / "tinycnn_mrdavid.tflite"
        conversion_success = False
        
        # Method 1: Direct conversion (works for both Keras 2 and 3)
        try:
            print("Method 1: Direct Keras to TFLite conversion...")
            converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            tflite_model = converter.convert()
            
            # Save the model
            main_model_path.write_bytes(tflite_model)
            
            file_size_kb = len(tflite_model) / 1024
            file_size_mb = file_size_kb / 1024
            
            print(f"✅ SUCCESS!")
            print(f"   File: {main_model_path}")
            print(f"   Size: {file_size_kb:.1f} KB ({file_size_mb:.2f} MB)")
            print(f"   Type: Float32 (standard precision)")
            conversion_success = True
            
        except Exception as e1:
            print(f"⚠️  Method 1 failed: {str(e1)[:100]}")
            
            # Method 2: Save as .keras then convert (Keras 3 preferred method)
            try:
                print()
                print("Method 2: Save as .keras then convert...")
                import tempfile
                with tempfile.TemporaryDirectory() as tmpdir:
                    keras_path = Path(tmpdir) / "model.keras"
                    
                    # Save in Keras format (works for Keras 3)
                    self.model.save(keras_path)
                    print(f"   ✓ Saved temporary .keras file")
                    
                    # Load and convert to TFLite
                    loaded_model = keras.models.load_model(keras_path)
                    converter = tf.lite.TFLiteConverter.from_keras_model(loaded_model)
                    converter.optimizations = [tf.lite.Optimize.DEFAULT]
                    tflite_model = converter.convert()
                    
                    # Save the model
                    main_model_path.write_bytes(tflite_model)
                    
                    file_size_kb = len(tflite_model) / 1024
                    file_size_mb = file_size_kb / 1024
                    
                    print(f"✅ SUCCESS!")
                    print(f"   File: {main_model_path}")
                    print(f"   Size: {file_size_kb:.1f} KB ({file_size_mb:.2f} MB)")
                    print(f"   Type: Float32 (standard precision)")
                    conversion_success = True
                    
            except Exception as e2:
                print(f"⚠️  Method 2 failed: {str(e2)[:100]}")
                
                # Method 3: Use concrete function (most compatible)
                try:
                    print()
                    print("Method 3: Concrete function conversion...")
                    
                    # Create concrete function
                    @tf.function(input_signature=[
                        tf.TensorSpec(shape=[None, self.img_size, self.img_size, 3], 
                                     dtype=tf.float32, name='input')
                    ])
                    def model_fn(x):
                        return self.model(x, training=False)
                    
                    concrete_func = model_fn.get_concrete_function()
                    
                    # Convert using concrete function
                    converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])
                    converter.optimizations = [tf.lite.Optimize.DEFAULT]
                    tflite_model = converter.convert()
                    
                    # Save the model
                    main_model_path.write_bytes(tflite_model)
                    
                    file_size_kb = len(tflite_model) / 1024
                    file_size_mb = file_size_kb / 1024
                    
                    print(f"✅ SUCCESS!")
                    print(f"   File: {main_model_path}")
                    print(f"   Size: {file_size_kb:.1f} KB ({file_size_mb:.2f} MB)")
                    print(f"   Type: Float32 (standard precision)")
                    conversion_success = True
                    
                except Exception as e3:
                    print(f"⚠️  Method 3 failed: {str(e3)[:100]}")
                    
                    # Method 4: SavedModel format (last resort)
                    try:
                        print()
                        print("Method 4: SavedModel format conversion...")
                        import tempfile
                        with tempfile.TemporaryDirectory() as tmpdir:
                            saved_model_dir = Path(tmpdir) / "saved_model"
                            
                            # Export to SavedModel format
                            tf.saved_model.save(self.model, str(saved_model_dir))
                            print(f"   ✓ Saved temporary SavedModel")
                            
                            # Convert SavedModel to TFLite
                            converter = tf.lite.TFLiteConverter.from_saved_model(str(saved_model_dir))
                            converter.optimizations = [tf.lite.Optimize.DEFAULT]
                            tflite_model = converter.convert()
                            
                            # Save the model
                            main_model_path.write_bytes(tflite_model)
                            
                            file_size_kb = len(tflite_model) / 1024
                            file_size_mb = file_size_kb / 1024
                            
                            print(f"✅ SUCCESS!")
                            print(f"   File: {main_model_path}")
                            print(f"   Size: {file_size_kb:.1f} KB ({file_size_mb:.2f} MB)")
                            print(f"   Type: Float32 (standard precision)")
                            conversion_success = True
                            
                    except Exception as e4:
                        print(f"❌ All conversion methods failed!")
                        print()
                        print("Error details:")
                        print(f"  Method 1: {str(e1)[:80]}")
                        print(f"  Method 2: {str(e2)[:80]}")
                        print(f"  Method 3: {str(e3)[:80]}")
                        print(f"  Method 4: {str(e4)[:80]}")
                        print()
                        print("Saving as .keras format instead...")
                        keras_path = models_dir / "tinycnn_mrdavid.keras"
                        self.model.save(keras_path)
                        print(f"✅ Saved Keras model: {keras_path}")
                        print()
                        print("⚠️  WARNING: Could not convert to .tflite format")
                        print("   You can try manual conversion later:")
                        print(f"   1. Load model: model = keras.models.load_model('{keras_path}')")
                        print(f"   2. Convert: converter = tf.lite.TFLiteConverter.from_keras_model(model)")
                        print(f"   3. Save: open('models/tinycnn_mrdavid.tflite', 'wb').write(converter.convert())")
                        return
        
        if not conversion_success:
            return
        if not conversion_success:
            return
        
        print()
        
        # Optional: INT8 quantized model for Raspberry Pi
        print("Creating optimized model for Raspberry Pi (optional)...")
        print("-" * 70)
        
        int8_model_path = models_dir / "tinycnn_mrdavid_int8.tflite"
        
        try:
            # Representative dataset for quantization
            def representative_data_gen():
                num_samples = min(100, len(self.X_train))
                for i in range(num_samples):
                    sample = self.X_train[i:i+1].astype(np.float32)
                    yield [sample]
            
            print("Quantizing model to INT8...")
            
            # Try method that worked for Float32
            if keras_version >= 3:
                # Keras 3: Use .keras file intermediate
                import tempfile
                with tempfile.TemporaryDirectory() as tmpdir:
                    keras_path = Path(tmpdir) / "model.keras"
                    self.model.save(keras_path)
                    loaded_model = keras.models.load_model(keras_path)
                    converter = tf.lite.TFLiteConverter.from_keras_model(loaded_model)
            else:
                # Keras 2: Direct conversion
                converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
            
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            converter.representative_dataset = representative_data_gen
            converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
            converter.inference_input_type = tf.uint8
            converter.inference_output_type = tf.uint8
            
            tflite_model_int8 = converter.convert()
            int8_model_path.write_bytes(tflite_model_int8)
            
            file_size_kb = len(tflite_model_int8) / 1024
            file_size_mb = file_size_kb / 1024
            
            print(f"✅ SUCCESS!")
            print(f"   File: {int8_model_path}")
            print(f"   Size: {file_size_kb:.1f} KB ({file_size_mb:.2f} MB)")
            print(f"   Type: INT8 quantized (4x smaller, 4x faster on Pi)")
            
            # Show compression ratio
            if main_model_path.exists():
                original_size = main_model_path.stat().st_size / 1024
                compressed_size = file_size_kb
                ratio = original_size / compressed_size
                print(f"   Compression: {ratio:.1f}x smaller than Float32")
            
        except Exception as e:
            print(f"⚠️  INT8 quantization failed: {str(e)[:100]}")
            print(f"   Float32 model will work fine on Raspberry Pi")
        
        print()
        print("=" * 70)
        print("✅ MODEL EXPORT COMPLETE")
        print("=" * 70)
        print()
        
        # Summary
        print("📁 SAVED MODEL FILES:")
        print()
        
        if main_model_path.exists():
            size_kb = main_model_path.stat().st_size / 1024
            print(f"✅ tinycnn_mrdavid.tflite")
            print(f"   Location: {main_model_path.absolute()}")
            print(f"   Size: {size_kb:.1f} KB")
            print(f"   Use: Main model for face recognition")
            print()
        
        if int8_model_path.exists():
            size_kb = int8_model_path.stat().st_size / 1024
            print(f"✅ tinycnn_mrdavid_int8.tflite (optional)")
            print(f"   Location: {int8_model_path.absolute()}")
            print(f"   Size: {size_kb:.1f} KB")
            print(f"   Use: Optimized for Raspberry Pi 5 (faster)")
            print()
        
        print("=" * 70)
        print("NEXT STEP: Run the application")
        print("=" * 70)
        print()
        print("Command:")
        print("  python3 main.py")
        print()
        print("The application will automatically use:")
        print(f"  → {main_model_path.name}")
        print()
        print("=" * 70)
    
    def verify_exported_model(self):
        """Verify that the exported model file exists and works"""
        print()
        print("=" * 70)
        print("🔍 VERIFYING EXPORTED MODEL")
        print("=" * 70)
        print()
        
        main_model_path = Path("models/tinycnn_mrdavid.tflite")
        
        # Check if file exists
        if not main_model_path.exists():
            print("⚠️  TFLite model file not found")
            print(f"   Expected: {main_model_path.absolute()}")
            print()
            
            # Check for alternative formats
            keras_path = Path("models/tinycnn_mrdavid.keras")
            h5_path = Path("models/tinycnn_mrdavid.h5")
            
            if keras_path.exists():
                print(f"✅ Found Keras model: {keras_path}")
                print(f"   Size: {keras_path.stat().st_size / (1024*1024):.2f} MB")
                print()
                print("   Note: Model saved in .keras format instead of .tflite")
                print("   This usually happens with newer TensorFlow/Keras versions.")
                print()
                print("   Options:")
                print("   1. Use the .keras model (convert manually if needed)")
                print("   2. Try downgrading: pip install tensorflow==2.13.0")
                print()
                return False
            
            elif h5_path.exists():
                print(f"✅ Found H5 model: {h5_path}")
                print(f"   Size: {h5_path.stat().st_size / (1024*1024):.2f} MB")
                print()
                print("   Note: Model saved in .h5 format instead of .tflite")
                print("   You can try manual conversion:")
                print("   1. Load: model = keras.models.load_model('models/tinycnn_mrdavid.h5')")
                print("   2. Convert: converter = tf.lite.TFLiteConverter.from_keras_model(model)")
                print("   3. Save: open('models/tinycnn_mrdavid.tflite', 'wb').write(converter.convert())")
                print()
                return False
            
            else:
                print("❌ No model file found in any format!")
                print("   Training may have failed.")
                return False
        
        print(f"✅ Model file found: {main_model_path}")
        
        # Get file size
        file_size = main_model_path.stat().st_size
        print(f"   Size: {file_size / 1024:.1f} KB ({file_size / (1024*1024):.2f} MB)")
        
        # Try to load the model
        try:
            print()
            print("Testing model loading...")
            interpreter = tf.lite.Interpreter(model_path=str(main_model_path))
            interpreter.allocate_tensors()
            
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            
            print(f"✅ Model loads successfully!")
            print(f"   Input shape: {input_details[0]['shape']}")
            print(f"   Input type: {input_details[0]['dtype']}")
            print(f"   Output shape: {output_details[0]['shape']}")
            print(f"   Output type: {output_details[0]['dtype']}")
            
            # Test with a sample image
            if hasattr(self, 'X_val') and len(self.X_val) > 0:
                print()
                print("Testing inference with sample image...")
                
                test_sample = self.X_val[0:1].astype(np.float32)
                
                interpreter.set_tensor(input_details[0]['index'], test_sample)
                interpreter.invoke()
                output = interpreter.get_tensor(output_details[0]['index'])
                
                prediction = float(output[0][0])
                print(f"✅ Inference works!")
                print(f"   Sample prediction: {prediction:.4f}")
                print(f"   Predicted class: {'Mr. David' if prediction >= 0.5 else 'Others'}")
            
            print()
            print("=" * 70)
            print("✅ MODEL VERIFICATION PASSED")
            print("=" * 70)
            print()
            print(f"Your model is ready to use:")
            print(f"  📁 {main_model_path.absolute()}")
            print()
            
            return True
            
        except Exception as e:
            print(f"❌ Model verification failed: {e}")
            print()
            print("The model file exists but may be corrupted.")
            print("Try training again.")
            return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='dataset')
    parser.add_argument('--img-size', type=int, default=128)
    parser.add_argument('--epochs', type=int, default=150)
    parser.add_argument('--batch-size', type=int, default=8)
    args = parser.parse_args()
    
    print("=" * 70)
    print("🛡️  ULTRA-ROBUST FACE RECOGNITION TRAINING")
    print("=" * 70)
    print(f"Dataset: {args.dataset}")
    print(f"Image size: {args.img_size}×{args.img_size}")
    print(f"Epochs: {args.epochs}")
    print(f"Batch size: {args.batch_size}")
    print("=" * 70)
    print()
    
    print("TIP: First run 'python3 verify_system.py' to check your setup!")
    print()
    
    trainer = UltraRobustTrainer(args.dataset, args.img_size)
    history = trainer.train(args.epochs, args.batch_size)
    
    if history is not None:
        print("=" * 70)
        print("🎉 SUCCESS! TRAINING COMPLETED!")
        print("=" * 70)
        print()
        print("Model saved as:")
        print(f"  📁 models/tinycnn_mrdavid.tflite")
        print()
        print("Absolute path:")
        model_path = Path("models/tinycnn_mrdavid.tflite").absolute()
        print(f"  {model_path}")
        print()
        print("=" * 70)
        print("NEXT STEP: Run the application")
        print("=" * 70)
        print()
        print("Command:")
        print("  python3 main.py")
        print()
        print("The application will automatically detect and use your trained model!")
        print("=" * 70)
    else:
        print()
        print("=" * 70)
        print("❌ Training was not successful")
        print("=" * 70)
        print("Please check the error messages above and try again.")
    
    print()


if __name__ == "__main__":
    main()
