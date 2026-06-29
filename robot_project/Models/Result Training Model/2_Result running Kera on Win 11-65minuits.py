======================================================================
DATASET LOADED
======================================================================
Total: 8056 images
  Mr. David (label=1): 4028 images
  Others (label=0): 4028 images
  Ratio: 50.0% David
======================================================================

Train/Val Split:
  TRAIN: 6444 total (3222 David, 3222 Others)
  VAL:   1612 total (806 David, 806 Others)

🏗️  Building collapse-resistant model...
✓ Model created: 490,689 parameters

Class Weights (for loss balancing):
  Others (0): 1.000
  Mr. David (1): 1.000

======================================================================
CREATING BALANCED TRAINING BATCHES
======================================================================
Creating balanced batches:
  David samples: 3222
  Others samples: 3222
  → Balanced dataset size: 6444
  → David %: 50.0%
  → Others %: 50.0%

======================================================================
======================================================================
======================================================================
Epochs: 150
Batch size: 8
Initial LR: 0.00005 (very conservative)
======================================================================

Epoch 1: val_accuracy improved from None to 0.50000, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 30s 34ms/step - accuracy: 0.5008 - loss: 0.9732 - precision: 0.5006 - recall: 0.6058 - val_accuracy: 0.5000 - val_loss: 0.8722 - val_precision: 0.5000 - val_recall: 1.0000 - learning_rate: 5.0000e-05
Epoch 2/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.4978 - loss: 0.9560 - precision: 0.4970 - recall: 0.5455
Epoch 2: val_accuracy improved from 0.50000 to 0.55769, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.4978 - loss: 0.9561 - precision: 0.4980 - recall: 0.5341 - val_accuracy: 0.5577 - val_loss: 0.8444 - val_precision: 0.5306 - val_recall: 1.0000 - learning_rate: 5.0000e-05
Epoch 3/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.5082 - loss: 0.9358 - precision: 0.5232 - recall: 0.5064
Epoch 3: val_accuracy did not improve from 0.55769
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 33ms/step - accuracy: 0.5115 - loss: 0.9320 - precision: 0.5115 - recall: 0.5115 - val_accuracy: 0.5000 - val_loss: 0.8608 - val_precision: 0.5000 - val_recall: 1.0000 - learning_rate: 5.0000e-05
Epoch 4/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.5183 - loss: 0.9200 - precision: 0.5217 - recall: 0.5122  
Epoch 4: val_accuracy did not improve from 0.55769
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 33ms/step - accuracy: 0.5287 - loss: 0.9097 - precision: 0.5287 - recall: 0.5292 - val_accuracy: 0.5000 - val_loss: 0.8568 - val_precision: 0.5000 - val_recall: 1.0000 - learning_rate: 5.0000e-05
Epoch 5/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.5664 - loss: 0.8816 - precision: 0.5652 - recall: 0.5717  
  📊 Per-class accuracy:
     Mr. David: 98.8%
     Others: 37.6%

Epoch 5: val_accuracy improved from 0.55769 to 0.68176, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.5841 - loss: 0.8685 - precision: 0.5838 - recall: 0.5860 - val_accuracy: 0.6818 - val_loss: 0.8150 - val_precision: 0.6128 - val_recall: 0.9876 - learning_rate: 5.0000e-05
Epoch 6/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.5852 - loss: 0.8713 - precision: 0.5797 - recall: 0.5947  
Epoch 6: val_accuracy did not improve from 0.68176
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 33ms/step - accuracy: 0.5813 - loss: 0.8651 - precision: 0.5812 - recall: 0.5822 - val_accuracy: 0.5174 - val_loss: 0.8589 - val_precision: 0.5088 - val_recall: 1.0000 - learning_rate: 5.0000e-05
Epoch 7/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.5864 - loss: 0.8523 - precision: 0.5904 - recall: 0.6146  
Epoch 7: val_accuracy improved from 0.68176 to 0.79963, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 33ms/step - accuracy: 0.5947 - loss: 0.8484 - precision: 0.5920 - recall: 0.6092 - val_accuracy: 0.7996 - val_loss: 0.7826 - val_precision: 0.7723 - val_recall: 0.8499 - learning_rate: 5.0000e-05
Epoch 8/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.5907 - loss: 0.8448 - precision: 0.5854 - recall: 0.5784   
Epoch 8: val_accuracy did not improve from 0.79963
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 33ms/step - accuracy: 0.5973 - loss: 0.8492 - precision: 0.5992 - recall: 0.5878 - val_accuracy: 0.5050 - val_loss: 0.9070 - val_precision: 0.5025 - val_recall: 1.0000 - learning_rate: 5.0000e-05
Epoch 9/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.6006 - loss: 0.8456 - precision: 0.5941 - recall: 0.6145  
Epoch 9: val_accuracy did not improve from 0.79963
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 33ms/step - accuracy: 0.5993 - loss: 0.8461 - precision: 0.5989 - recall: 0.6015 - val_accuracy: 0.7481 - val_loss: 0.7625 - val_precision: 0.6706 - val_recall: 0.9752 - learning_rate: 5.0000e-05
Epoch 10/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.6142 - loss: 0.8278 - precision: 0.6227 - recall: 0.6070  
  📊 Per-class accuracy:
     Mr. David: 95.7%
     Others: 60.3%

Epoch 10: val_accuracy did not improve from 0.79963
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6089 - loss: 0.8302 - precision: 0.6095 - recall: 0.6065 - val_accuracy: 0.7798 - val_loss: 0.7109 - val_precision: 0.7067 - val_recall: 0.9566 - learning_rate: 5.0000e-05
Epoch 11/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.6086 - loss: 0.8291 - precision: 0.6116 - recall: 0.5957  
Epoch 11: val_accuracy did not improve from 0.79963
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 33ms/step - accuracy: 0.6096 - loss: 0.8289 - precision: 0.6126 - recall: 0.5959 - val_accuracy: 0.7574 - val_loss: 0.7157 - val_precision: 0.6784 - val_recall: 0.9789 - learning_rate: 5.0000e-05
Epoch 12/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.6001 - loss: 0.8370 - precision: 0.5934 - recall: 0.6049  
Epoch 12: val_accuracy did not improve from 0.79963
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 33ms/step - accuracy: 0.6088 - loss: 0.8320 - precision: 0.6070 - recall: 0.6173 - val_accuracy: 0.5527 - val_loss: 0.8027 - val_precision: 0.5278 - val_recall: 1.0000 - learning_rate: 5.0000e-05
Epoch 13/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6082 - loss: 0.8268 - precision: 0.6007 - recall: 0.6369  
Epoch 13: val_accuracy improved from 0.79963 to 0.85112, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.6089 - loss: 0.8245 - precision: 0.6048 - recall: 0.6288 - val_accuracy: 0.8511 - val_loss: 0.7225 - val_precision: 0.8942 - val_recall: 0.7965 - learning_rate: 5.0000e-05
Epoch 14/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6116 - loss: 0.8200 - precision: 0.6126 - recall: 0.6076  
Epoch 14: val_accuracy did not improve from 0.85112
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.6195 - loss: 0.8131 - precision: 0.6167 - recall: 0.6313 - val_accuracy: 0.8511 - val_loss: 0.7173 - val_precision: 0.8345 - val_recall: 0.8759 - learning_rate: 5.0000e-05
Epoch 15/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6371 - loss: 0.8027 - precision: 0.6418 - recall: 0.6447  
  📊 Per-class accuracy:
     Mr. David: 82.5%
     Others: 87.6%

Epoch 15: val_accuracy did not improve from 0.85112
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 36ms/step - accuracy: 0.6282 - loss: 0.8120 - precision: 0.6278 - recall: 0.6297 - val_accuracy: 0.8505 - val_loss: 0.7082 - val_precision: 0.8693 - val_recall: 0.8251 - learning_rate: 5.0000e-05
Epoch 16/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6103 - loss: 0.8154 - precision: 0.6012 - recall: 0.6261  
Epoch 16: val_accuracy did not improve from 0.85112
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.6124 - loss: 0.8165 - precision: 0.6102 - recall: 0.6223 - val_accuracy: 0.7072 - val_loss: 0.7554 - val_precision: 0.6330 - val_recall: 0.9864 - learning_rate: 5.0000e-05
Epoch 17/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6161 - loss: 0.8154 - precision: 0.6234 - recall: 0.6161   
Epoch 17: val_accuracy did not improve from 0.85112
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.6113 - loss: 0.8140 - precision: 0.6101 - recall: 0.6167 - val_accuracy: 0.7345 - val_loss: 0.7257 - val_precision: 0.6578 - val_recall: 0.9777 - learning_rate: 5.0000e-05
Epoch 18/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6276 - loss: 0.7980 - precision: 0.6275 - recall: 0.6323    
Epoch 18: val_accuracy did not improve from 0.85112
806/806 ━━━━━━━━━━━━━━━━━━━━ 41s 34ms/step - accuracy: 0.6245 - loss: 0.8016 - precision: 0.6259 - recall: 0.6186 - val_accuracy: 0.8344 - val_loss: 0.7177 - val_precision: 0.8759 - val_recall: 0.7792 - learning_rate: 5.0000e-05
Epoch 19/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6320 - loss: 0.7915 - precision: 0.6313 - recall: 0.6295   
Epoch 19: val_accuracy did not improve from 0.85112
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.6170 - loss: 0.8016 - precision: 0.6146 - recall: 0.6276 - val_accuracy: 0.7792 - val_loss: 0.7057 - val_precision: 0.7031 - val_recall: 0.9665 - learning_rate: 5.0000e-05
Epoch 20/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6126 - loss: 0.8061 - precision: 0.6099 - recall: 0.6363  
  📊 Per-class accuracy:
     Mr. David: 99.6%
     Others: 35.1%

Epoch 20: val_accuracy did not improve from 0.85112
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 36ms/step - accuracy: 0.6220 - loss: 0.8029 - precision: 0.6177 - recall: 0.6400 - val_accuracy: 0.6737 - val_loss: 0.7435 - val_precision: 0.6056 - val_recall: 0.9963 - learning_rate: 5.0000e-05
Epoch 21/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6251 - loss: 0.7901 - precision: 0.6289 - recall: 0.6130  
Epoch 21: val_accuracy did not improve from 0.85112
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.6263 - loss: 0.7954 - precision: 0.6262 - recall: 0.6269 - val_accuracy: 0.8313 - val_loss: 0.6769 - val_precision: 0.7781 - val_recall: 0.9268 - learning_rate: 5.0000e-05
Epoch 22/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6365 - loss: 0.7876 - precision: 0.6310 - recall: 0.6552  
Epoch 22: val_accuracy did not improve from 0.85112
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.6307 - loss: 0.7882 - precision: 0.6277 - recall: 0.6421 - val_accuracy: 0.8046 - val_loss: 0.6629 - val_precision: 0.7367 - val_recall: 0.9479 - learning_rate: 5.0000e-05
Epoch 23/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6214 - loss: 0.8007 - precision: 0.6236 - recall: 0.6370   
Epoch 23: val_accuracy did not improve from 0.85112
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.6224 - loss: 0.7931 - precision: 0.6216 - recall: 0.6260 - val_accuracy: 0.6328 - val_loss: 0.7437 - val_precision: 0.5766 - val_recall: 0.9988 - learning_rate: 5.0000e-05
Epoch 24/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6292 - loss: 0.7864 - precision: 0.6287 - recall: 0.6403   
Epoch 24: val_accuracy did not improve from 0.85112
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.6286 - loss: 0.7879 - precision: 0.6269 - recall: 0.6356 - val_accuracy: 0.8139 - val_loss: 0.7024 - val_precision: 0.7510 - val_recall: 0.9392 - learning_rate: 5.0000e-05
Epoch 25/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6313 - loss: 0.7934 - precision: 0.6352 - recall: 0.6368   
  📊 Per-class accuracy:
     Mr. David: 100.0%
     Others: 17.0%

Epoch 25: val_accuracy did not improve from 0.85112
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 36ms/step - accuracy: 0.6257 - loss: 0.7877 - precision: 0.6244 - recall: 0.6310 - val_accuracy: 0.5850 - val_loss: 0.7546 - val_precision: 0.5464 - val_recall: 1.0000 - learning_rate: 5.0000e-05
Epoch 26/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6244 - loss: 0.7846 - precision: 0.6193 - recall: 0.6567  
Epoch 26: val_accuracy did not improve from 0.85112
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.6282 - loss: 0.7774 - precision: 0.6262 - recall: 0.6359 - val_accuracy: 0.8164 - val_loss: 0.7073 - val_precision: 0.7505 - val_recall: 0.9479 - learning_rate: 5.0000e-05
Epoch 27/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6292 - loss: 0.7799 - precision: 0.6362 - recall: 0.6357   
Epoch 27: val_accuracy improved from 0.85112 to 0.85360, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6344 - loss: 0.7781 - precision: 0.6334 - recall: 0.6381 - val_accuracy: 0.8536 - val_loss: 0.6616 - val_precision: 0.9107 - val_recall: 0.7841 - learning_rate: 5.0000e-05
Epoch 28/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6236 - loss: 0.7777 - precision: 0.6238 - recall: 0.6174  
Epoch 28: val_accuracy improved from 0.85360 to 0.86166, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.6254 - loss: 0.7789 - precision: 0.6265 - recall: 0.6210 - val_accuracy: 0.8617 - val_loss: 0.6657 - val_precision: 0.8568 - val_recall: 0.8685 - learning_rate: 5.0000e-05
Epoch 29/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6412 - loss: 0.7699 - precision: 0.6441 - recall: 0.6495  
Epoch 29: val_accuracy improved from 0.86166 to 0.86352, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6259 - loss: 0.7743 - precision: 0.6253 - recall: 0.6279 - val_accuracy: 0.8635 - val_loss: 0.6379 - val_precision: 0.8728 - val_recall: 0.8511 - learning_rate: 5.0000e-05
Epoch 30/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6226 - loss: 0.7792 - precision: 0.6180 - recall: 0.6074  
  📊 Per-class accuracy:
     Mr. David: 81.1%
     Others: 91.3%

Epoch 30: val_accuracy did not improve from 0.86352
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 36ms/step - accuracy: 0.6251 - loss: 0.7757 - precision: 0.6283 - recall: 0.6127 - val_accuracy: 0.8623 - val_loss: 0.6170 - val_precision: 0.9033 - val_recall: 0.8114 - learning_rate: 5.0000e-05
Epoch 31/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6374 - loss: 0.7660 - precision: 0.6344 - recall: 0.6593   
Epoch 31: val_accuracy did not improve from 0.86352
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6327 - loss: 0.7664 - precision: 0.6293 - recall: 0.6456 - val_accuracy: 0.8356 - val_loss: 0.6389 - val_precision: 0.7827 - val_recall: 0.9293 - learning_rate: 5.0000e-05
Epoch 32/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6304 - loss: 0.7596 - precision: 0.6184 - recall: 0.6569   
Epoch 32: val_accuracy did not improve from 0.86352
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.6307 - loss: 0.7642 - precision: 0.6276 - recall: 0.6428 - val_accuracy: 0.8567 - val_loss: 0.6362 - val_precision: 0.8563 - val_recall: 0.8573 - learning_rate: 4.9744e-05
Epoch 33/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6419 - loss: 0.7599 - precision: 0.6426 - recall: 0.6530   
Epoch 33: val_accuracy did not improve from 0.86352
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6390 - loss: 0.7600 - precision: 0.6369 - recall: 0.6468 - val_accuracy: 0.8077 - val_loss: 0.6500 - val_precision: 0.9460 - val_recall: 0.6526 - learning_rate: 4.9490e-05
Epoch 34/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6381 - loss: 0.7568 - precision: 0.6369 - recall: 0.6439   
Epoch 34: val_accuracy did not improve from 0.86352
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6324 - loss: 0.7613 - precision: 0.6303 - recall: 0.6403 - val_accuracy: 0.8009 - val_loss: 0.6267 - val_precision: 0.9385 - val_recall: 0.6439 - learning_rate: 4.9236e-05
Epoch 35/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6393 - loss: 0.7644 - precision: 0.6315 - recall: 0.6482  
  📊 Per-class accuracy:
     Mr. David: 84.5%
     Others: 88.3%

Epoch 35: val_accuracy improved from 0.86352 to 0.86414, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 30s 37ms/step - accuracy: 0.6359 - loss: 0.7649 - precision: 0.6346 - recall: 0.6409 - val_accuracy: 0.8641 - val_loss: 0.6334 - val_precision: 0.8787 - val_recall: 0.8449 - learning_rate: 4.8985e-05
Epoch 36/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6348 - loss: 0.7594 - precision: 0.6245 - recall: 0.6519  
Epoch 36: val_accuracy did not improve from 0.86414
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6328 - loss: 0.7618 - precision: 0.6348 - recall: 0.6257 - val_accuracy: 0.7066 - val_loss: 0.6734 - val_precision: 0.9744 - val_recall: 0.4243 - learning_rate: 4.8734e-05
Epoch 37/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6453 - loss: 0.7472 - precision: 0.6401 - recall: 0.6424   
Epoch 37: val_accuracy did not improve from 0.86414
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6439 - loss: 0.7523 - precision: 0.6438 - recall: 0.6440 - val_accuracy: 0.8635 - val_loss: 0.6186 - val_precision: 0.8795 - val_recall: 0.8424 - learning_rate: 4.8485e-05
Epoch 38/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6390 - loss: 0.7469 - precision: 0.6381 - recall: 0.6570   
Epoch 38: val_accuracy did not improve from 0.86414
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6387 - loss: 0.7504 - precision: 0.6325 - recall: 0.6623 - val_accuracy: 0.8065 - val_loss: 0.6120 - val_precision: 0.7335 - val_recall: 0.9628 - learning_rate: 4.8237e-05
Epoch 39/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6465 - loss: 0.7393 - precision: 0.6554 - recall: 0.6404   
Epoch 39: val_accuracy did not improve from 0.86414
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6466 - loss: 0.7416 - precision: 0.6494 - recall: 0.6375 - val_accuracy: 0.8009 - val_loss: 0.6368 - val_precision: 0.7256 - val_recall: 0.9677 - learning_rate: 4.7990e-05
Epoch 40/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6336 - loss: 0.7533 - precision: 0.6482 - recall: 0.6325   
  📊 Per-class accuracy:
     Mr. David: 98.4%
     Others: 51.7%

Epoch 40: val_accuracy did not improve from 0.86414
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 35ms/step - accuracy: 0.6398 - loss: 0.7488 - precision: 0.6403 - recall: 0.6381 - val_accuracy: 0.7506 - val_loss: 0.6670 - val_precision: 0.6709 - val_recall: 0.9839 - learning_rate: 4.7744e-05
Epoch 41/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.6366 - loss: 0.7422 - precision: 0.6432 - recall: 0.6252  
Epoch 41: val_accuracy did not improve from 0.86414
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 33ms/step - accuracy: 0.6349 - loss: 0.7447 - precision: 0.6376 - recall: 0.6248 - val_accuracy: 0.8517 - val_loss: 0.6250 - val_precision: 0.8218 - val_recall: 0.8983 - learning_rate: 4.7500e-05
Epoch 42/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.6429 - loss: 0.7478 - precision: 0.6482 - recall: 0.6418  
Epoch 42: val_accuracy did not improve from 0.86414
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 33ms/step - accuracy: 0.6417 - loss: 0.7438 - precision: 0.6428 - recall: 0.6378 - val_accuracy: 0.8555 - val_loss: 0.5821 - val_precision: 0.8490 - val_recall: 0.8648 - learning_rate: 4.7257e-05
Epoch 43/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.6390 - loss: 0.7422 - precision: 0.6411 - recall: 0.6210    
Epoch 43: val_accuracy did not improve from 0.86414
806/806 ━━━━━━━━━━━━━━━━━━━━ 41s 33ms/step - accuracy: 0.6390 - loss: 0.7432 - precision: 0.6452 - recall: 0.6179 - val_accuracy: 0.7308 - val_loss: 0.6693 - val_precision: 0.6522 - val_recall: 0.9888 - learning_rate: 4.7015e-05
Epoch 44/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.6466 - loss: 0.7379 - precision: 0.6539 - recall: 0.6039  
Epoch 44: val_accuracy improved from 0.86414 to 0.86600, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 33ms/step - accuracy: 0.6490 - loss: 0.7404 - precision: 0.6612 - recall: 0.6111 - val_accuracy: 0.8660 - val_loss: 0.6113 - val_precision: 0.8660 - val_recall: 0.8660 - learning_rate: 4.6775e-05
Epoch 45/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.6422 - loss: 0.7408 - precision: 0.6400 - recall: 0.6415  
  📊 Per-class accuracy:
     Mr. David: 63.2%
     Others: 95.4%

Epoch 45: val_accuracy did not improve from 0.86600
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6426 - loss: 0.7380 - precision: 0.6423 - recall: 0.6437 - val_accuracy: 0.7928 - val_loss: 0.5993 - val_precision: 0.9322 - val_recall: 0.6315 - learning_rate: 4.6535e-05
Epoch 46/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.6571 - loss: 0.7275 - precision: 0.6582 - recall: 0.6424  
Epoch 46: val_accuracy did not improve from 0.86600
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 33ms/step - accuracy: 0.6611 - loss: 0.7225 - precision: 0.6649 - recall: 0.6496 - val_accuracy: 0.8641 - val_loss: 0.5649 - val_precision: 0.9116 - val_recall: 0.8065 - learning_rate: 4.6297e-05
Epoch 47/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6480 - loss: 0.7346 - precision: 0.6458 - recall: 0.6612  
Epoch 47: val_accuracy improved from 0.86600 to 0.87283, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6470 - loss: 0.7329 - precision: 0.6438 - recall: 0.6580 - val_accuracy: 0.8728 - val_loss: 0.5545 - val_precision: 0.8770 - val_recall: 0.8672 - learning_rate: 4.6060e-05
Epoch 48/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6422 - loss: 0.7324 - precision: 0.6365 - recall: 0.6500  
Epoch 48: val_accuracy did not improve from 0.87283
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6418 - loss: 0.7336 - precision: 0.6377 - recall: 0.6567 - val_accuracy: 0.8542 - val_loss: 0.5645 - val_precision: 0.8073 - val_recall: 0.9305 - learning_rate: 4.5825e-05
Epoch 49/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.6561 - loss: 0.7248 - precision: 0.6551 - recall: 0.6692  
Epoch 49: val_accuracy did not improve from 0.87283
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 33ms/step - accuracy: 0.6533 - loss: 0.7245 - precision: 0.6518 - recall: 0.6583 - val_accuracy: 0.8226 - val_loss: 0.5895 - val_precision: 0.9362 - val_recall: 0.6923 - learning_rate: 4.5590e-05
Epoch 50/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.6410 - loss: 0.7305 - precision: 0.6505 - recall: 0.6020  
  📊 Per-class accuracy:
     Mr. David: 95.5%
     Others: 66.6%

Epoch 50: val_accuracy did not improve from 0.87283
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6375 - loss: 0.7338 - precision: 0.6442 - recall: 0.6142 - val_accuracy: 0.8108 - val_loss: 0.6009 - val_precision: 0.7411 - val_recall: 0.9553 - learning_rate: 4.5357e-05
Epoch 51/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.6556 - loss: 0.7243 - precision: 0.6680 - recall: 0.6317  
Epoch 51: val_accuracy did not improve from 0.87283
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 33ms/step - accuracy: 0.6437 - loss: 0.7338 - precision: 0.6491 - recall: 0.6257 - val_accuracy: 0.8679 - val_loss: 0.5542 - val_precision: 0.8767 - val_recall: 0.8561 - learning_rate: 4.5125e-05
Epoch 52/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.6442 - loss: 0.7174 - precision: 0.6321 - recall: 0.6107  
Epoch 52: val_accuracy improved from 0.87283 to 0.87531, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 33ms/step - accuracy: 0.6457 - loss: 0.7192 - precision: 0.6519 - recall: 0.6254 - val_accuracy: 0.8753 - val_loss: 0.5591 - val_precision: 0.9050 - val_recall: 0.8387 - learning_rate: 4.4894e-05
Epoch 53/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6610 - loss: 0.7182 - precision: 0.6592 - recall: 0.6629  
Epoch 53: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 33ms/step - accuracy: 0.6550 - loss: 0.7231 - precision: 0.6614 - recall: 0.6353 - val_accuracy: 0.8300 - val_loss: 0.5689 - val_precision: 0.9209 - val_recall: 0.7221 - learning_rate: 4.4664e-05
Epoch 54/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6296 - loss: 0.7338 - precision: 0.6288 - recall: 0.6417  
Epoch 54: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6505 - loss: 0.7172 - precision: 0.6505 - recall: 0.6505 - val_accuracy: 0.8629 - val_loss: 0.5600 - val_precision: 0.8643 - val_recall: 0.8610 - learning_rate: 4.4436e-05
Epoch 55/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6500 - loss: 0.7198 - precision: 0.6616 - recall: 0.6320   
  📊 Per-class accuracy:
     Mr. David: 52.1%
     Others: 97.5%

Epoch 55: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 30s 37ms/step - accuracy: 0.6488 - loss: 0.7213 - precision: 0.6507 - recall: 0.6425 - val_accuracy: 0.7481 - val_loss: 0.6108 - val_precision: 0.9545 - val_recall: 0.5211 - learning_rate: 4.4209e-05
Epoch 56/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6536 - loss: 0.7136 - precision: 0.6664 - recall: 0.6254   
Epoch 56: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6572 - loss: 0.7137 - precision: 0.6602 - recall: 0.6477 - val_accuracy: 0.8716 - val_loss: 0.5908 - val_precision: 0.8495 - val_recall: 0.9032 - learning_rate: 4.3982e-05
Epoch 57/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6449 - loss: 0.7154 - precision: 0.6448 - recall: 0.6248   
Epoch 57: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6435 - loss: 0.7172 - precision: 0.6509 - recall: 0.6192 - val_accuracy: 0.8480 - val_loss: 0.5926 - val_precision: 0.8013 - val_recall: 0.9256 - learning_rate: 4.3757e-05
Epoch 58/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6612 - loss: 0.7114 - precision: 0.6651 - recall: 0.6566   
Epoch 58: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6651 - loss: 0.7065 - precision: 0.6668 - recall: 0.6601 - val_accuracy: 0.8679 - val_loss: 0.5310 - val_precision: 0.8846 - val_recall: 0.8462 - learning_rate: 4.3534e-05
Epoch 59/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6441 - loss: 0.7139 - precision: 0.6452 - recall: 0.6097  
Epoch 59: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6421 - loss: 0.7171 - precision: 0.6505 - recall: 0.6145 - val_accuracy: 0.8703 - val_loss: 0.5386 - val_precision: 0.8774 - val_recall: 0.8610 - learning_rate: 4.3311e-05
Epoch 60/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6349 - loss: 0.7276 - precision: 0.6410 - recall: 0.6270  
  📊 Per-class accuracy:
     Mr. David: 75.1%
     Others: 93.2%

Epoch 60: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 36ms/step - accuracy: 0.6397 - loss: 0.7231 - precision: 0.6416 - recall: 0.6328 - val_accuracy: 0.8412 - val_loss: 0.5490 - val_precision: 0.9167 - val_recall: 0.7506 - learning_rate: 4.3089e-05
Epoch 61/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6608 - loss: 0.7045 - precision: 0.6746 - recall: 0.6374  
Epoch 61: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6510 - loss: 0.7102 - precision: 0.6555 - recall: 0.6366 - val_accuracy: 0.7959 - val_loss: 0.5734 - val_precision: 0.9475 - val_recall: 0.6266 - learning_rate: 4.2869e-05
Epoch 62/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6624 - loss: 0.7058 - precision: 0.6623 - recall: 0.6660  
Epoch 62: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6560 - loss: 0.7089 - precision: 0.6567 - recall: 0.6536 - val_accuracy: 0.8536 - val_loss: 0.5452 - val_precision: 0.8409 - val_recall: 0.8722 - learning_rate: 4.2649e-05
Epoch 63/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6517 - loss: 0.7010 - precision: 0.6616 - recall: 0.6387  
Epoch 63: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6515 - loss: 0.7031 - precision: 0.6542 - recall: 0.6425 - val_accuracy: 0.8449 - val_loss: 0.5522 - val_precision: 0.7939 - val_recall: 0.9318 - learning_rate: 4.2431e-05
Epoch 64/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6483 - loss: 0.7159 - precision: 0.6486 - recall: 0.6520  
Epoch 64: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6547 - loss: 0.7080 - precision: 0.6584 - recall: 0.6431 - val_accuracy: 0.8083 - val_loss: 0.5533 - val_precision: 0.8913 - val_recall: 0.7022 - learning_rate: 4.2214e-05
Epoch 65/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6515 - loss: 0.7084 - precision: 0.6657 - recall: 0.6032  
  📊 Per-class accuracy:
     Mr. David: 82.0%
     Others: 89.7%

Epoch 65: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 36ms/step - accuracy: 0.6525 - loss: 0.7051 - precision: 0.6601 - recall: 0.6288 - val_accuracy: 0.8586 - val_loss: 0.5482 - val_precision: 0.8884 - val_recall: 0.8201 - learning_rate: 4.1998e-05
Epoch 66/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6567 - loss: 0.7010 - precision: 0.6659 - recall: 0.6556  
Epoch 66: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6583 - loss: 0.6952 - precision: 0.6592 - recall: 0.6555 - val_accuracy: 0.8499 - val_loss: 0.5289 - val_precision: 0.8365 - val_recall: 0.8697 - learning_rate: 4.1783e-05
Epoch 67/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6495 - loss: 0.7024 - precision: 0.6496 - recall: 0.6248 
Epoch 67: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6636 - loss: 0.6998 - precision: 0.6715 - recall: 0.6403 - val_accuracy: 0.8009 - val_loss: 0.5603 - val_precision: 0.9262 - val_recall: 0.6538 - learning_rate: 4.1570e-05
Epoch 68/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6471 - loss: 0.7074 - precision: 0.6590 - recall: 0.6562  
Epoch 68: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6546 - loss: 0.7024 - precision: 0.6542 - recall: 0.6558 - val_accuracy: 0.8468 - val_loss: 0.5416 - val_precision: 0.9178 - val_recall: 0.7618 - learning_rate: 4.1357e-05
Epoch 69/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6555 - loss: 0.7029 - precision: 0.6532 - recall: 0.6429  
Epoch 69: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6598 - loss: 0.6955 - precision: 0.6609 - recall: 0.6564 - val_accuracy: 0.8418 - val_loss: 0.5292 - val_precision: 0.9118 - val_recall: 0.7568 - learning_rate: 4.1145e-05
Epoch 70/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6582 - loss: 0.6893 - precision: 0.6597 - recall: 0.6818  
  📊 Per-class accuracy:
     Mr. David: 69.0%
     Others: 95.8%

Epoch 70: val_accuracy did not improve from 0.87531
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 36ms/step - accuracy: 0.6625 - loss: 0.6918 - precision: 0.6558 - recall: 0.6837 - val_accuracy: 0.8238 - val_loss: 0.5360 - val_precision: 0.9424 - val_recall: 0.6898 - learning_rate: 4.0935e-05
Epoch 71/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6555 - loss: 0.6993 - precision: 0.6677 - recall: 0.6413  
Epoch 71: val_accuracy improved from 0.87531 to 0.87655, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6538 - loss: 0.7000 - precision: 0.6557 - recall: 0.6477 - val_accuracy: 0.8766 - val_loss: 0.5038 - val_precision: 0.8936 - val_recall: 0.8548 - learning_rate: 4.0725e-05
Epoch 72/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6563 - loss: 0.6956 - precision: 0.6571 - recall: 0.6454  
Epoch 72: val_accuracy did not improve from 0.87655
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6626 - loss: 0.6947 - precision: 0.6650 - recall: 0.6555 - val_accuracy: 0.8648 - val_loss: 0.5176 - val_precision: 0.9188 - val_recall: 0.8002 - learning_rate: 4.0517e-05
Epoch 73/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6465 - loss: 0.6972 - precision: 0.6336 - recall: 0.6856  
Epoch 73: val_accuracy did not improve from 0.87655
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6581 - loss: 0.6911 - precision: 0.6546 - recall: 0.6695 - val_accuracy: 0.8623 - val_loss: 0.5159 - val_precision: 0.9056 - val_recall: 0.8089 - learning_rate: 4.0310e-05
Epoch 74/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6662 - loss: 0.6838 - precision: 0.6602 - recall: 0.6719  
Epoch 74: val_accuracy did not improve from 0.87655
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6646 - loss: 0.6862 - precision: 0.6648 - recall: 0.6642 - val_accuracy: 0.8071 - val_loss: 0.5633 - val_precision: 0.9412 - val_recall: 0.6551 - learning_rate: 4.0103e-05
Epoch 75/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6537 - loss: 0.6937 - precision: 0.6520 - recall: 0.6580  
  📊 Per-class accuracy:
     Mr. David: 72.0%
     Others: 93.4%

Epoch 75: val_accuracy did not improve from 0.87655
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 36ms/step - accuracy: 0.6566 - loss: 0.6929 - precision: 0.6551 - recall: 0.6614 - val_accuracy: 0.8269 - val_loss: 0.5360 - val_precision: 0.9163 - val_recall: 0.7196 - learning_rate: 3.9898e-05
Epoch 76/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6609 - loss: 0.6824 - precision: 0.6678 - recall: 0.6620   
Epoch 76: val_accuracy did not improve from 0.87655
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6681 - loss: 0.6797 - precision: 0.6680 - recall: 0.6682 - val_accuracy: 0.8176 - val_loss: 0.5458 - val_precision: 0.9211 - val_recall: 0.6948 - learning_rate: 3.9694e-05
Epoch 77/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 31ms/step - accuracy: 0.6570 - loss: 0.6791 - precision: 0.6572 - recall: 0.6468  
Epoch 77: val_accuracy did not improve from 0.87655
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 33ms/step - accuracy: 0.6660 - loss: 0.6793 - precision: 0.6714 - recall: 0.6505 - val_accuracy: 0.7426 - val_loss: 0.6859 - val_precision: 0.9734 - val_recall: 0.4988 - learning_rate: 3.9491e-05
Epoch 78/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6478 - loss: 0.6952 - precision: 0.6487 - recall: 0.6403   
Epoch 78: val_accuracy did not improve from 0.87655
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6594 - loss: 0.6899 - precision: 0.6596 - recall: 0.6586 - val_accuracy: 0.8393 - val_loss: 0.5210 - val_precision: 0.9307 - val_recall: 0.7333 - learning_rate: 3.9289e-05
Epoch 79/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6745 - loss: 0.6756 - precision: 0.6768 - recall: 0.6686  
Epoch 79: val_accuracy did not improve from 0.87655
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.6766 - loss: 0.6717 - precision: 0.6741 - recall: 0.6837 - val_accuracy: 0.7984 - val_loss: 0.5921 - val_precision: 0.9670 - val_recall: 0.6179 - learning_rate: 3.9088e-05
Epoch 80/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6701 - loss: 0.6709 - precision: 0.6786 - recall: 0.6734   
  📊 Per-class accuracy:
     Mr. David: 61.8%
     Others: 97.8%

Epoch 80: val_accuracy did not improve from 0.87655
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 36ms/step - accuracy: 0.6713 - loss: 0.6676 - precision: 0.6695 - recall: 0.6766 - val_accuracy: 0.7978 - val_loss: 0.5650 - val_precision: 0.9651 - val_recall: 0.6179 - learning_rate: 3.8888e-05
Epoch 81/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6772 - loss: 0.6631 - precision: 0.6670 - recall: 0.6999  
Epoch 81: val_accuracy did not improve from 0.87655
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6808 - loss: 0.6649 - precision: 0.6732 - recall: 0.7027 - val_accuracy: 0.8424 - val_loss: 0.5313 - val_precision: 0.9340 - val_recall: 0.7370 - learning_rate: 3.8689e-05
Epoch 82/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6919 - loss: 0.6610 - precision: 0.6834 - recall: 0.6929  
Epoch 82: val_accuracy did not improve from 0.87655
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6851 - loss: 0.6625 - precision: 0.6853 - recall: 0.6847 - val_accuracy: 0.8108 - val_loss: 0.5679 - val_precision: 0.9514 - val_recall: 0.6551 - learning_rate: 3.8491e-05
Epoch 83/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6808 - loss: 0.6695 - precision: 0.6790 - recall: 0.6773  
Epoch 83: val_accuracy did not improve from 0.87655
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6836 - loss: 0.6651 - precision: 0.6869 - recall: 0.6747 - val_accuracy: 0.7872 - val_loss: 0.6367 - val_precision: 0.9584 - val_recall: 0.6005 - learning_rate: 3.8294e-05
Epoch 84/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6972 - loss: 0.6532 - precision: 0.7009 - recall: 0.6946  
Epoch 84: val_accuracy improved from 0.87655 to 0.88896, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6867 - loss: 0.6639 - precision: 0.6884 - recall: 0.6822 - val_accuracy: 0.8890 - val_loss: 0.4833 - val_precision: 0.8809 - val_recall: 0.8995 - learning_rate: 3.8098e-05
Epoch 85/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6766 - loss: 0.6696 - precision: 0.6854 - recall: 0.6741   
  📊 Per-class accuracy:
     Mr. David: 83.1%
     Others: 92.8%

Epoch 85: val_accuracy did not improve from 0.88896
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 35ms/step - accuracy: 0.6808 - loss: 0.6656 - precision: 0.6858 - recall: 0.6673 - val_accuracy: 0.8797 - val_loss: 0.4775 - val_precision: 0.9203 - val_recall: 0.8313 - learning_rate: 3.7903e-05
Epoch 86/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6980 - loss: 0.6573 - precision: 0.7011 - recall: 0.6881   
Epoch 86: val_accuracy improved from 0.88896 to 0.89268, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6828 - loss: 0.6647 - precision: 0.6890 - recall: 0.6664 - val_accuracy: 0.8927 - val_loss: 0.4681 - val_precision: 0.8961 - val_recall: 0.8883 - learning_rate: 3.7709e-05
Epoch 87/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6743 - loss: 0.6675 - precision: 0.6899 - recall: 0.6519  
Epoch 87: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6890 - loss: 0.6587 - precision: 0.6909 - recall: 0.6840 - val_accuracy: 0.8592 - val_loss: 0.5040 - val_precision: 0.9474 - val_recall: 0.7605 - learning_rate: 3.7516e-05
Epoch 88/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6910 - loss: 0.6560 - precision: 0.6976 - recall: 0.6725  
Epoch 88: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6840 - loss: 0.6531 - precision: 0.6892 - recall: 0.6704 - val_accuracy: 0.8710 - val_loss: 0.4926 - val_precision: 0.9423 - val_recall: 0.7903 - learning_rate: 3.7325e-05
Epoch 89/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6766 - loss: 0.6674 - precision: 0.6824 - recall: 0.6695  
Epoch 89: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6831 - loss: 0.6601 - precision: 0.6820 - recall: 0.6862 - val_accuracy: 0.7816 - val_loss: 0.6042 - val_precision: 0.9809 - val_recall: 0.5744 - learning_rate: 3.7134e-05
Epoch 90/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6876 - loss: 0.6581 - precision: 0.6879 - recall: 0.6918  
  📊 Per-class accuracy:
     Mr. David: 66.0%
     Others: 97.8%

Epoch 90: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 35ms/step - accuracy: 0.6805 - loss: 0.6581 - precision: 0.6769 - recall: 0.6906 - val_accuracy: 0.8189 - val_loss: 0.5461 - val_precision: 0.9673 - val_recall: 0.6600 - learning_rate: 3.6944e-05
Epoch 91/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6872 - loss: 0.6510 - precision: 0.6844 - recall: 0.6962  
Epoch 91: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6831 - loss: 0.6555 - precision: 0.6793 - recall: 0.6937 - val_accuracy: 0.8524 - val_loss: 0.5040 - val_precision: 0.9479 - val_recall: 0.7457 - learning_rate: 3.6755e-05
Epoch 92/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6881 - loss: 0.6569 - precision: 0.6902 - recall: 0.7073  
Epoch 92: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6923 - loss: 0.6486 - precision: 0.6873 - recall: 0.7055 - val_accuracy: 0.8598 - val_loss: 0.4992 - val_precision: 0.9328 - val_recall: 0.7754 - learning_rate: 3.6567e-05
Epoch 93/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6990 - loss: 0.6408 - precision: 0.7041 - recall: 0.6803  
Epoch 93: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6943 - loss: 0.6423 - precision: 0.6987 - recall: 0.6831 - val_accuracy: 0.7965 - val_loss: 0.5644 - val_precision: 0.9799 - val_recall: 0.6055 - learning_rate: 3.6379e-05
Epoch 94/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6876 - loss: 0.6496 - precision: 0.6793 - recall: 0.6974  
Epoch 94: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.6889 - loss: 0.6440 - precision: 0.6880 - recall: 0.6912 - val_accuracy: 0.7717 - val_loss: 0.6042 - val_precision: 0.9803 - val_recall: 0.5546 - learning_rate: 3.6193e-05
Epoch 95/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.6819 - loss: 0.6556 - precision: 0.6745 - recall: 0.7073  
  📊 Per-class accuracy:
     Mr. David: 74.3%
     Others: 96.2%

Epoch 95: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 36ms/step - accuracy: 0.6934 - loss: 0.6487 - precision: 0.6804 - recall: 0.7294 - val_accuracy: 0.8524 - val_loss: 0.5002 - val_precision: 0.9508 - val_recall: 0.7432 - learning_rate: 3.6008e-05
Epoch 96/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6919 - loss: 0.6409 - precision: 0.6878 - recall: 0.7151  
Epoch 96: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6918 - loss: 0.6416 - precision: 0.6829 - recall: 0.7160 - val_accuracy: 0.7823 - val_loss: 0.6263 - val_precision: 0.9830 - val_recall: 0.5744 - learning_rate: 3.5824e-05
Epoch 97/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6889 - loss: 0.6404 - precision: 0.6871 - recall: 0.6968 
Epoch 97: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6924 - loss: 0.6435 - precision: 0.6845 - recall: 0.7138 - val_accuracy: 0.8598 - val_loss: 0.5079 - val_precision: 0.9517 - val_recall: 0.7581 - learning_rate: 3.5641e-05
Epoch 98/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6911 - loss: 0.6399 - precision: 0.6906 - recall: 0.6936  
Epoch 98: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6957 - loss: 0.6368 - precision: 0.6943 - recall: 0.6993 - val_accuracy: 0.8151 - val_loss: 0.5644 - val_precision: 0.9774 - val_recall: 0.6452 - learning_rate: 3.5458e-05
Epoch 99/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6988 - loss: 0.6403 - precision: 0.6980 - recall: 0.6969   
Epoch 99: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6951 - loss: 0.6380 - precision: 0.6930 - recall: 0.7005 - val_accuracy: 0.8821 - val_loss: 0.4625 - val_precision: 0.9254 - val_recall: 0.8313 - learning_rate: 3.5277e-05
Epoch 100/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7002 - loss: 0.6390 - precision: 0.6994 - recall: 0.7071  
  📊 Per-class accuracy:
     Mr. David: 64.6%
     Others: 98.6%

Epoch 100: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 30s 37ms/step - accuracy: 0.6963 - loss: 0.6353 - precision: 0.6923 - recall: 0.7067 - val_accuracy: 0.8164 - val_loss: 0.5318 - val_precision: 0.9793 - val_recall: 0.6464 - learning_rate: 3.5096e-05
Epoch 101/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7085 - loss: 0.6269 - precision: 0.7137 - recall: 0.7043  
Epoch 101: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7034 - loss: 0.6278 - precision: 0.7088 - recall: 0.6906 - val_accuracy: 0.8368 - val_loss: 0.5067 - val_precision: 0.9533 - val_recall: 0.7084 - learning_rate: 3.4917e-05
Epoch 102/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6929 - loss: 0.6342 - precision: 0.6811 - recall: 0.7048  
Epoch 102: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6980 - loss: 0.6296 - precision: 0.6933 - recall: 0.7101 - val_accuracy: 0.7624 - val_loss: 0.6898 - val_precision: 0.9930 - val_recall: 0.5285 - learning_rate: 3.4738e-05
Epoch 103/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6968 - loss: 0.6300 - precision: 0.6984 - recall: 0.6948   
Epoch 103: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7013 - loss: 0.6266 - precision: 0.7006 - recall: 0.7030 - val_accuracy: 0.8660 - val_loss: 0.4758 - val_precision: 0.9390 - val_recall: 0.7829 - learning_rate: 3.4560e-05
Epoch 104/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7202 - loss: 0.6267 - precision: 0.7212 - recall: 0.7231   
Epoch 104: val_accuracy did not improve from 0.89268
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7126 - loss: 0.6246 - precision: 0.7108 - recall: 0.7169 - val_accuracy: 0.7916 - val_loss: 0.5682 - val_precision: 0.9816 - val_recall: 0.5943 - learning_rate: 3.4384e-05
Epoch 105/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6995 - loss: 0.6352 - precision: 0.6956 - recall: 0.6945  
  📊 Per-class accuracy:
     Mr. David: 84.5%
     Others: 94.4%

Epoch 105: val_accuracy improved from 0.89268 to 0.89454, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 30s 37ms/step - accuracy: 0.7036 - loss: 0.6319 - precision: 0.6981 - recall: 0.7176 - val_accuracy: 0.8945 - val_loss: 0.4402 - val_precision: 0.9380 - val_recall: 0.8449 - learning_rate: 3.4208e-05
Epoch 106/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7165 - loss: 0.6224 - precision: 0.7025 - recall: 0.7452  
Epoch 106: val_accuracy improved from 0.89454 to 0.90695, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7041 - loss: 0.6256 - precision: 0.6947 - recall: 0.7281 - val_accuracy: 0.9069 - val_loss: 0.4319 - val_precision: 0.9327 - val_recall: 0.8772 - learning_rate: 3.4033e-05
Epoch 107/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6951 - loss: 0.6323 - precision: 0.6986 - recall: 0.6984  
Epoch 107: val_accuracy did not improve from 0.90695
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6991 - loss: 0.6271 - precision: 0.6994 - recall: 0.6983 - val_accuracy: 0.8610 - val_loss: 0.4757 - val_precision: 0.9634 - val_recall: 0.7506 - learning_rate: 3.3859e-05
Epoch 108/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7180 - loss: 0.6164 - precision: 0.7181 - recall: 0.7070   
Epoch 108: val_accuracy did not improve from 0.90695
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7098 - loss: 0.6263 - precision: 0.7110 - recall: 0.7070 - val_accuracy: 0.8964 - val_loss: 0.4320 - val_precision: 0.9419 - val_recall: 0.8449 - learning_rate: 3.3685e-05
Epoch 109/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7235 - loss: 0.6085 - precision: 0.7112 - recall: 0.7595   
Epoch 109: val_accuracy did not improve from 0.90695
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 35ms/step - accuracy: 0.7128 - loss: 0.6132 - precision: 0.7014 - recall: 0.7408 - val_accuracy: 0.8455 - val_loss: 0.5077 - val_precision: 0.9793 - val_recall: 0.7060 - learning_rate: 3.3513e-05
Epoch 110/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6979 - loss: 0.6254 - precision: 0.7024 - recall: 0.6872   
  📊 Per-class accuracy:
     Mr. David: 81.9%
     Others: 96.9%

Epoch 110: val_accuracy did not improve from 0.90695
806/806 ━━━━━━━━━━━━━━━━━━━━ 30s 37ms/step - accuracy: 0.7038 - loss: 0.6237 - precision: 0.7065 - recall: 0.6971 - val_accuracy: 0.8939 - val_loss: 0.4405 - val_precision: 0.9635 - val_recall: 0.8189 - learning_rate: 3.3342e-05
Epoch 111/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7175 - loss: 0.6176 - precision: 0.7142 - recall: 0.7362  
Epoch 111: val_accuracy did not improve from 0.90695
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7121 - loss: 0.6148 - precision: 0.7035 - recall: 0.7334 - val_accuracy: 0.8071 - val_loss: 0.5609 - val_precision: 0.9920 - val_recall: 0.6191 - learning_rate: 3.3171e-05
Epoch 112/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6899 - loss: 0.6310 - precision: 0.6944 - recall: 0.6881  
Epoch 112: val_accuracy did not improve from 0.90695
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.6948 - loss: 0.6267 - precision: 0.6945 - recall: 0.6955 - val_accuracy: 0.8741 - val_loss: 0.4720 - val_precision: 0.9660 - val_recall: 0.7754 - learning_rate: 3.3001e-05
Epoch 113/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7064 - loss: 0.6116 - precision: 0.7147 - recall: 0.6948   
Epoch 113: val_accuracy improved from 0.90695 to 0.91749, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7075 - loss: 0.6124 - precision: 0.7056 - recall: 0.7120 - val_accuracy: 0.9175 - val_loss: 0.4176 - val_precision: 0.9410 - val_recall: 0.8908 - learning_rate: 3.2832e-05
Epoch 114/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7058 - loss: 0.6278 - precision: 0.6904 - recall: 0.7485  
Epoch 114: val_accuracy did not improve from 0.91749
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7098 - loss: 0.6183 - precision: 0.7005 - recall: 0.7331 - val_accuracy: 0.8083 - val_loss: 0.5574 - val_precision: 0.9940 - val_recall: 0.6203 - learning_rate: 3.2664e-05
Epoch 115/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6953 - loss: 0.6196 - precision: 0.6872 - recall: 0.6830   
  📊 Per-class accuracy:
     Mr. David: 75.1%
     Others: 99.0%

Epoch 115: val_accuracy did not improve from 0.91749
806/806 ━━━━━━━━━━━━━━━━━━━━ 30s 37ms/step - accuracy: 0.7020 - loss: 0.6161 - precision: 0.7071 - recall: 0.6899 - val_accuracy: 0.8703 - val_loss: 0.4827 - val_precision: 0.9869 - val_recall: 0.7506 - learning_rate: 3.2497e-05
Epoch 116/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.6924 - loss: 0.6184 - precision: 0.6969 - recall: 0.6894  
Epoch 116: val_accuracy improved from 0.91749 to 0.93300, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7048 - loss: 0.6094 - precision: 0.7011 - recall: 0.7142 - val_accuracy: 0.9330 - val_loss: 0.3907 - val_precision: 0.9418 - val_recall: 0.9231 - learning_rate: 3.2331e-05
Epoch 117/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7034 - loss: 0.6199 - precision: 0.7091 - recall: 0.6805   
Epoch 117: val_accuracy did not improve from 0.93300
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7106 - loss: 0.6123 - precision: 0.7227 - recall: 0.6834 - val_accuracy: 0.8722 - val_loss: 0.4816 - val_precision: 0.9823 - val_recall: 0.7581 - learning_rate: 3.2166e-05
Epoch 118/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7180 - loss: 0.6015 - precision: 0.7455 - recall: 0.6701   
Epoch 118: val_accuracy did not improve from 0.93300
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7160 - loss: 0.6040 - precision: 0.7280 - recall: 0.6896 - val_accuracy: 0.9181 - val_loss: 0.4064 - val_precision: 0.9668 - val_recall: 0.8660 - learning_rate: 3.2001e-05
Epoch 119/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7090 - loss: 0.6132 - precision: 0.7069 - recall: 0.7314  
Epoch 119: val_accuracy did not improve from 0.93300
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7044 - loss: 0.6141 - precision: 0.6970 - recall: 0.7232 - val_accuracy: 0.9324 - val_loss: 0.3896 - val_precision: 0.9628 - val_recall: 0.8995 - learning_rate: 3.1837e-05
Epoch 120/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7159 - loss: 0.6026 - precision: 0.7128 - recall: 0.7254  
  📊 Per-class accuracy:
     Mr. David: 82.1%
     Others: 97.3%

Epoch 120: val_accuracy did not improve from 0.93300
806/806 ━━━━━━━━━━━━━━━━━━━━ 30s 37ms/step - accuracy: 0.7123 - loss: 0.6062 - precision: 0.7136 - recall: 0.7092 - val_accuracy: 0.8970 - val_loss: 0.4313 - val_precision: 0.9678 - val_recall: 0.8213 - learning_rate: 3.1675e-05
Epoch 121/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7121 - loss: 0.6143 - precision: 0.7055 - recall: 0.7293  
Epoch 121: val_accuracy did not improve from 0.93300
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7132 - loss: 0.6094 - precision: 0.7084 - recall: 0.7247 - val_accuracy: 0.9088 - val_loss: 0.4220 - val_precision: 0.9881 - val_recall: 0.8275 - learning_rate: 3.1512e-05
Epoch 122/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7135 - loss: 0.6005 - precision: 0.7056 - recall: 0.7284  
Epoch 122: val_accuracy did not improve from 0.93300
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7103 - loss: 0.6066 - precision: 0.6989 - recall: 0.7390 - val_accuracy: 0.9206 - val_loss: 0.4138 - val_precision: 0.9857 - val_recall: 0.8536 - learning_rate: 3.1351e-05
Epoch 123/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7013 - loss: 0.6214 - precision: 0.6951 - recall: 0.7288   
Epoch 123: val_accuracy improved from 0.93300 to 0.94541, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7112 - loss: 0.6086 - precision: 0.7075 - recall: 0.7200 - val_accuracy: 0.9454 - val_loss: 0.3803 - val_precision: 0.9174 - val_recall: 0.9789 - learning_rate: 3.1191e-05
Epoch 124/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7152 - loss: 0.6131 - precision: 0.7128 - recall: 0.7117   
Epoch 124: val_accuracy did not improve from 0.94541
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 35ms/step - accuracy: 0.7166 - loss: 0.6079 - precision: 0.7199 - recall: 0.7092 - val_accuracy: 0.9417 - val_loss: 0.3832 - val_precision: 0.9552 - val_recall: 0.9268 - learning_rate: 3.1031e-05
Epoch 125/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7019 - loss: 0.6076 - precision: 0.6953 - recall: 0.7172   
  📊 Per-class accuracy:
     Mr. David: 73.2%
     Others: 99.1%

Epoch 125: val_accuracy did not improve from 0.94541
806/806 ━━━━━━━━━━━━━━━━━━━━ 30s 37ms/step - accuracy: 0.7072 - loss: 0.6047 - precision: 0.7053 - recall: 0.7117 - val_accuracy: 0.8617 - val_loss: 0.4652 - val_precision: 0.9883 - val_recall: 0.7320 - learning_rate: 3.0873e-05
Epoch 126/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7187 - loss: 0.6005 - precision: 0.7162 - recall: 0.7297  
Epoch 126: val_accuracy improved from 0.94541 to 0.94851, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 35ms/step - accuracy: 0.7214 - loss: 0.5998 - precision: 0.7210 - recall: 0.7225 - val_accuracy: 0.9485 - val_loss: 0.3711 - val_precision: 0.9689 - val_recall: 0.9268 - learning_rate: 3.0715e-05
Epoch 127/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7016 - loss: 0.6065 - precision: 0.7084 - recall: 0.6946  
Epoch 127: val_accuracy did not improve from 0.94851
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 35ms/step - accuracy: 0.7050 - loss: 0.6084 - precision: 0.7053 - recall: 0.7042 - val_accuracy: 0.9082 - val_loss: 0.4115 - val_precision: 0.9881 - val_recall: 0.8263 - learning_rate: 3.0557e-05
Epoch 128/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7296 - loss: 0.5925 - precision: 0.7328 - recall: 0.7148   
Epoch 128: val_accuracy did not improve from 0.94851
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 36ms/step - accuracy: 0.7171 - loss: 0.6014 - precision: 0.7262 - recall: 0.6971 - val_accuracy: 0.9460 - val_loss: 0.3719 - val_precision: 0.9838 - val_recall: 0.9069 - learning_rate: 3.0401e-05
Epoch 129/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7043 - loss: 0.6018 - precision: 0.7194 - recall: 0.6772  
Epoch 129: val_accuracy did not improve from 0.94851
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7138 - loss: 0.6000 - precision: 0.7289 - recall: 0.6809 - val_accuracy: 0.9212 - val_loss: 0.4014 - val_precision: 0.9857 - val_recall: 0.8548 - learning_rate: 3.0246e-05
Epoch 130/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7163 - loss: 0.6059 - precision: 0.7306 - recall: 0.6918   
  📊 Per-class accuracy:
     Mr. David: 88.1%
     Others: 98.5%

Epoch 130: val_accuracy did not improve from 0.94851
806/806 ━━━━━━━━━━━━━━━━━━━━ 30s 37ms/step - accuracy: 0.7128 - loss: 0.6076 - precision: 0.7228 - recall: 0.6903 - val_accuracy: 0.9330 - val_loss: 0.3855 - val_precision: 0.9834 - val_recall: 0.8809 - learning_rate: 3.0091e-05
Epoch 131/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7244 - loss: 0.5902 - precision: 0.7233 - recall: 0.7117   
Epoch 131: val_accuracy improved from 0.94851 to 0.95658, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 35ms/step - accuracy: 0.7202 - loss: 0.5955 - precision: 0.7237 - recall: 0.7123 - val_accuracy: 0.9566 - val_loss: 0.3597 - val_precision: 0.9543 - val_recall: 0.9591 - learning_rate: 2.9937e-05
Epoch 132/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7149 - loss: 0.5997 - precision: 0.7295 - recall: 0.7059  
Epoch 132: val_accuracy did not improve from 0.95658
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 36ms/step - accuracy: 0.7205 - loss: 0.5951 - precision: 0.7181 - recall: 0.7259 - val_accuracy: 0.8790 - val_loss: 0.4355 - val_precision: 0.9967 - val_recall: 0.7605 - learning_rate: 2.9784e-05
Epoch 133/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7095 - loss: 0.5984 - precision: 0.7108 - recall: 0.6968   
Epoch 133: val_accuracy did not improve from 0.95658
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7182 - loss: 0.5969 - precision: 0.7175 - recall: 0.7197 - val_accuracy: 0.9367 - val_loss: 0.3793 - val_precision: 0.9862 - val_recall: 0.8859 - learning_rate: 2.9631e-05
Epoch 134/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7188 - loss: 0.5945 - precision: 0.7259 - recall: 0.7169  
Epoch 134: val_accuracy improved from 0.95658 to 0.96340, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 35ms/step - accuracy: 0.7174 - loss: 0.5971 - precision: 0.7179 - recall: 0.7163 - val_accuracy: 0.9634 - val_loss: 0.3553 - val_precision: 0.9640 - val_recall: 0.9628 - learning_rate: 2.9480e-05
Epoch 135/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7163 - loss: 0.5836 - precision: 0.7125 - recall: 0.7178  
  📊 Per-class accuracy:
     Mr. David: 88.6%
     Others: 98.9%

Epoch 135: val_accuracy did not improve from 0.96340
806/806 ━━━━━━━━━━━━━━━━━━━━ 30s 37ms/step - accuracy: 0.7193 - loss: 0.5893 - precision: 0.7222 - recall: 0.7126 - val_accuracy: 0.9373 - val_loss: 0.3775 - val_precision: 0.9876 - val_recall: 0.8859 - learning_rate: 2.9329e-05
Epoch 136/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7118 - loss: 0.5997 - precision: 0.7236 - recall: 0.6873  
Epoch 136: val_accuracy did not improve from 0.96340
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 36ms/step - accuracy: 0.7132 - loss: 0.5940 - precision: 0.7216 - recall: 0.6943 - val_accuracy: 0.9578 - val_loss: 0.3503 - val_precision: 0.9805 - val_recall: 0.9342 - learning_rate: 2.9179e-05
Epoch 137/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7278 - loss: 0.5850 - precision: 0.7252 - recall: 0.7438   
Epoch 137: val_accuracy did not improve from 0.96340
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 35ms/step - accuracy: 0.7235 - loss: 0.5891 - precision: 0.7184 - recall: 0.7349 - val_accuracy: 0.9150 - val_loss: 0.3979 - val_precision: 0.9912 - val_recall: 0.8375 - learning_rate: 2.9030e-05
Epoch 138/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7278 - loss: 0.5911 - precision: 0.7422 - recall: 0.7157   
Epoch 138: val_accuracy did not improve from 0.96340
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 36ms/step - accuracy: 0.7277 - loss: 0.5875 - precision: 0.7276 - recall: 0.7278 - val_accuracy: 0.9262 - val_loss: 0.3925 - val_precision: 0.9886 - val_recall: 0.8623 - learning_rate: 2.8881e-05
Epoch 139/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7193 - loss: 0.5809 - precision: 0.7236 - recall: 0.7194   
Epoch 139: val_accuracy improved from 0.96340 to 0.96526, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 36ms/step - accuracy: 0.7173 - loss: 0.5919 - precision: 0.7179 - recall: 0.7157 - val_accuracy: 0.9653 - val_loss: 0.3395 - val_precision: 0.9795 - val_recall: 0.9504 - learning_rate: 2.8733e-05
Epoch 140/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7237 - loss: 0.5893 - precision: 0.7236 - recall: 0.7198  
  📊 Per-class accuracy:
     Mr. David: 93.2%
     Others: 97.8%

Epoch 140: val_accuracy did not improve from 0.96526
806/806 ━━━━━━━━━━━━━━━━━━━━ 30s 37ms/step - accuracy: 0.7204 - loss: 0.5877 - precision: 0.7204 - recall: 0.7204 - val_accuracy: 0.9547 - val_loss: 0.3577 - val_precision: 0.9766 - val_recall: 0.9318 - learning_rate: 2.8586e-05
Epoch 141/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.7244 - loss: 0.5883 - precision: 0.7232 - recall: 0.7215  
Epoch 141: val_accuracy did not improve from 0.96526
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.7278 - loss: 0.5868 - precision: 0.7280 - recall: 0.7275 - val_accuracy: 0.9510 - val_loss: 0.3595 - val_precision: 0.9840 - val_recall: 0.9169 - learning_rate: 2.8440e-05
Epoch 142/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.7178 - loss: 0.5833 - precision: 0.7040 - recall: 0.7250  
Epoch 142: val_accuracy improved from 0.96526 to 0.97333, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.7115 - loss: 0.5922 - precision: 0.7138 - recall: 0.7061 - val_accuracy: 0.9733 - val_loss: 0.3356 - val_precision: 0.9647 - val_recall: 0.9826 - learning_rate: 2.8295e-05
Epoch 143/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.7081 - loss: 0.6025 - precision: 0.7028 - recall: 0.7273  
Epoch 143: val_accuracy improved from 0.97333 to 0.97891, saving model to models/ultra_robust_best.h5
WARNING:absl:You are saving your model as an HDF5 file via `model.save()` or `keras.saving.save_model(model)`. This file format is considered legacy. We recommend using instead the native Keras format, e.g. `model.save('my_model.keras')` or `keras.saving.save_model(model, 'my_model.keras')`.    
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.7048 - loss: 0.6037 - precision: 0.7010 - recall: 0.7145 - val_accuracy: 0.9789 - val_loss: 0.3441 - val_precision: 0.9730 - val_recall: 0.9851 - learning_rate: 2.8150e-05
Epoch 144/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.7261 - loss: 0.5770 - precision: 0.7204 - recall: 0.7283  
Epoch 144: val_accuracy did not improve from 0.97891
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.7287 - loss: 0.5755 - precision: 0.7310 - recall: 0.7238 - val_accuracy: 0.9708 - val_loss: 0.3376 - val_precision: 0.9762 - val_recall: 0.9653 - learning_rate: 2.8006e-05
Epoch 145/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.7162 - loss: 0.5802 - precision: 0.7171 - recall: 0.7125  
  📊 Per-class accuracy:
     Mr. David: 93.1%
     Others: 98.6%

Epoch 145: val_accuracy did not improve from 0.97891
806/806 ━━━━━━━━━━━━━━━━━━━━ 29s 36ms/step - accuracy: 0.7216 - loss: 0.5802 - precision: 0.7255 - recall: 0.7129 - val_accuracy: 0.9584 - val_loss: 0.3438 - val_precision: 0.9855 - val_recall: 0.9305 - learning_rate: 2.7862e-05
Epoch 146/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.7194 - loss: 0.5876 - precision: 0.7261 - recall: 0.7087  
Epoch 146: val_accuracy did not improve from 0.97891
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.7245 - loss: 0.5838 - precision: 0.7259 - recall: 0.7216 - val_accuracy: 0.9721 - val_loss: 0.3308 - val_precision: 0.9669 - val_recall: 0.9777 - learning_rate: 2.7720e-05
Epoch 147/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.7228 - loss: 0.5763 - precision: 0.7442 - recall: 0.6918  
Epoch 147: val_accuracy did not improve from 0.97891
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 34ms/step - accuracy: 0.7228 - loss: 0.5822 - precision: 0.7333 - recall: 0.7005 - val_accuracy: 0.9770 - val_loss: 0.3332 - val_precision: 0.9594 - val_recall: 0.9963 - learning_rate: 2.7578e-05
Epoch 148/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 32ms/step - accuracy: 0.7237 - loss: 0.5804 - precision: 0.7135 - recall: 0.7237  
Epoch 148: val_accuracy did not improve from 0.97891
806/806 ━━━━━━━━━━━━━━━━━━━━ 27s 34ms/step - accuracy: 0.7273 - loss: 0.5816 - precision: 0.7226 - recall: 0.7381 - val_accuracy: 0.9504 - val_loss: 0.3487 - val_precision: 0.9840 - val_recall: 0.9156 - learning_rate: 2.7437e-05
Epoch 149/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7301 - loss: 0.5783 - precision: 0.7242 - recall: 0.7373  
Epoch 149: val_accuracy did not improve from 0.97891
806/806 ━━━━━━━━━━━━━━━━━━━━ 28s 35ms/step - accuracy: 0.7298 - loss: 0.5808 - precision: 0.7296 - recall: 0.7303 - val_accuracy: 0.9510 - val_loss: 0.3474 - val_precision: 0.9853 - val_recall: 0.9156 - learning_rate: 2.7297e-05
Epoch 150/150
805/806 ━━━━━━━━━━━━━━━━━━━━ 0s 33ms/step - accuracy: 0.7201 - loss: 0.5914 - precision: 0.7167 - recall: 0.7254   
  📊 Per-class accuracy:
     Mr. David: 92.3%
     Others: 99.0%

Epoch 150: val_accuracy did not improve from 0.97891
806/806 ━━━━━━━━━━━━━━━━━━━━ 30s 37ms/step - accuracy: 0.7277 - loss: 0.5842 - precision: 0.7251 - recall: 0.7334 - val_accuracy: 0.9566 - val_loss: 0.3492 - val_precision: 0.9894 - val_recall: 0.9231 - learning_rate: 2.7157e-05
Restoring model weights from the end of the best epoch: 143.

======================================================================
✅ TRAINING COMPLETE
======================================================================

======================================================================
📊 FINAL EVALUATION
======================================================================

TRAINING SET:
  Overall: 0.9814 (98.14%)
  Mr. David: 0.9926 (99.26%)
  Others: 0.9702 (97.02%)
  David avg confidence: 0.8804
  Others avg confidence: 0.8486

VALIDATION SET:
  Overall: 0.9789 (97.89%)
  Mr. David: 0.9851 (98.51%)
  Others: 0.9727 (97.27%)
  David avg confidence: 0.8735
  Others avg confidence: 0.8475

======================================================================
DIAGNOSIS:
======================================================================
🎉 EXCELLENT! 90%+ validation accuracy!

======================================================================


======================================================================
📦 EXPORTING MODELS
======================================================================

Creating Float32 model...
  ⚠️  Conversion failed: 'Functional' object has no attribute '_get_save_spec'

Creating INT8 quantized model...
  ⚠️  Quantization failed: 'Functional' object has no attribute '_get_save_spec'

======================================================================
✅ MODEL EXPORT COMPLETE
======================================================================

Use in application:
  python3 main.py

======================================================================
✅ DONE!
======================================================================

Next step: Test your model
  python3 main.py

PS C:\Users\엉찬톨\Music\robotproject> 1