#!/usr/bin/env python3
"""
Manual TFLite Converter
Converts .keras or .h5 models to .tflite format
Use this if automatic conversion during training failed
"""

import sys
from pathlib import Path
import tensorflow as tf
from tensorflow import keras
import numpy as np

print("=" * 70)
print("🔧 MANUAL TFLITE CONVERTER")
print("=" * 70)
print()

# Check for model files
models_dir = Path("models")
if not models_dir.exists():
    print("❌ 'models' directory not found!")
    sys.exit(1)

# Look for source model files
keras_path = models_dir / "tinycnn_mrdavid.keras"
h5_path = models_dir / "tinycnn_mrdavid.h5"

source_model = None
source_path = None

if keras_path.exists():
    source_model = "keras"
    source_path = keras_path
    print(f"✅ Found: {keras_path}")
elif h5_path.exists():
    source_model = "h5"
    source_path = h5_path
    print(f"✅ Found: {h5_path}")
else:
    print("❌ No source model found!")
    print()
    print("Looking for:")
    print(f"  - {keras_path}")
    print(f"  - {h5_path}")
    print()
    print("These files should be created during training.")
    sys.exit(1)

print(f"   Size: {source_path.stat().st_size / (1024*1024):.2f} MB")
print()

# Load the model
print("Loading model...")
try:
    model = keras.models.load_model(source_path)
    print(f"✅ Model loaded successfully!")
    print(f"   Input shape: {model.input_shape}")
    print(f"   Output shape: {model.output_shape}")
    print()
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    sys.exit(1)

# Convert to TFLite
output_path = models_dir / "tinycnn_mrdavid.tflite"

print("Converting to TFLite format...")
print("-" * 70)

conversion_methods = []

# Method 1: Direct conversion
conversion_methods.append(("Direct conversion", lambda: tf.lite.TFLiteConverter.from_keras_model(model)))

# Method 2: Concrete function
def method2():
    img_size = model.input_shape[1]
    @tf.function(input_signature=[
        tf.TensorSpec(shape=[None, img_size, img_size, 3], dtype=tf.float32)
    ])
    def model_fn(x):
        return model(x, training=False)
    concrete_func = model_fn.get_concrete_function()
    return tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])

conversion_methods.append(("Concrete function", method2))

# Method 3: SavedModel
def method3():
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        saved_model_dir = Path(tmpdir) / "saved_model"
        tf.saved_model.save(model, str(saved_model_dir))
        return tf.lite.TFLiteConverter.from_saved_model(str(saved_model_dir))

conversion_methods.append(("SavedModel", method3))

# Try each method
success = False
for method_name, method_func in conversion_methods:
    print(f"\nTrying: {method_name}...")
    try:
        converter = method_func()
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        tflite_model = converter.convert()
        
        # Save the model
        output_path.write_bytes(tflite_model)
        
        file_size_kb = len(tflite_model) / 1024
        file_size_mb = file_size_kb / 1024
        
        print(f"✅ SUCCESS!")
        print(f"   Method: {method_name}")
        print(f"   Output: {output_path}")
        print(f"   Size: {file_size_kb:.1f} KB ({file_size_mb:.2f} MB)")
        
        success = True
        break
        
    except Exception as e:
        print(f"⚠️  Failed: {str(e)[:100]}")

if not success:
    print()
    print("=" * 70)
    print("❌ ALL CONVERSION METHODS FAILED")
    print("=" * 70)
    print()
    print("This might be due to:")
    print("  1. Incompatible TensorFlow version")
    print("  2. Custom layers in model")
    print("  3. Model architecture issues")
    print()
    print("Solutions:")
    print("  1. Try different TensorFlow version:")
    print("     pip install tensorflow==2.13.0")
    print()
    print("  2. Use the .keras model directly:")
    print("     (Some applications can load .keras files)")
    print()
    print("  3. Retrain with different architecture")
    print()
    sys.exit(1)

# Verify the converted model
print()
print("=" * 70)
print("🔍 VERIFYING CONVERTED MODEL")
print("=" * 70)
print()

try:
    interpreter = tf.lite.Interpreter(model_path=str(output_path))
    interpreter.allocate_tensors()
    
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    print("✅ Verification successful!")
    print(f"   Input shape: {input_details[0]['shape']}")
    print(f"   Input type: {input_details[0]['dtype']}")
    print(f"   Output shape: {output_details[0]['shape']}")
    print(f"   Output type: {output_details[0]['dtype']}")
    
    # Test inference
    print()
    print("Testing inference...")
    test_input = np.random.random((1, input_details[0]['shape'][1], 
                                   input_details[0]['shape'][2], 3)).astype(np.float32)
    
    interpreter.set_tensor(input_details[0]['index'], test_input)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    
    print(f"✅ Inference works!")
    print(f"   Test output: {output[0][0]:.4f}")
    
except Exception as e:
    print(f"❌ Verification failed: {e}")
    print()
    print("The .tflite file was created but may not work correctly.")
    sys.exit(1)

print()
print("=" * 70)
print("🎉 CONVERSION SUCCESSFUL!")
print("=" * 70)
print()
print(f"Output file: {output_path.absolute()}")
print(f"Size: {output_path.stat().st_size / 1024:.1f} KB")
print()
print("You can now use this model with:")
print("  python3 main.py")
print()
print("=" * 70)
