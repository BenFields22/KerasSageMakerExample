import numpy as np
import tensorflow as tf

# 1. Load the model
model = tf.keras.models.load_model("my_model.h5")

# 2. Prepare a test input, e.g., one sample with 4 features (adjust to your model's input shape)
sample_input = np.array([[1, 0, 0, 0]], dtype="float32")

# 3. Run inference
predictions = model.predict(sample_input)

# 4. Print results
print("Input shape:", sample_input.shape)
print("Raw predictions:", predictions)

# If it's a classification model with multiple classes, you might do:
predicted_class = np.argmax(predictions, axis=1)
print("Predicted class:", predicted_class)