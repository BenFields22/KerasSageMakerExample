import os

import keras
import numpy as np
import tensorflow as tf
from keras.models import load_model
from sagemaker import Session
from sagemaker.tensorflow.model import TensorFlowModel
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

sess = Session(default_bucket="bucket-name")
bucket = sess.default_bucket()
tf_framework_version = tf.__version__
# Generate synthetic dataset
np.random.seed(42)
num_samples = 1000  # Total number of samples
num_classes = 4  # Number of classes

# Generate inputs: One-hot encoded vectors of length 4
X = np.eye(num_classes)[np.random.choice(num_classes, num_samples)]

# Labels: Integer values representing the class (0, 1, 2, 3)
y = np.argmax(X, axis=1)

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Define the model
model = keras.Sequential(
    [
        keras.layers.Dense(8, activation="relu", input_shape=(4,)),
        keras.layers.Dense(8, activation="relu"),
        keras.layers.Dense(4, activation="softmax"),  # for 4 classes
    ]
)

# Compile the model
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",  # Sparse labels
    metrics=["accuracy"],
)


# Callback for printing during training
class PrintEpochCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        print(
            f"Epoch {epoch + 1}/{self.params['epochs']}: loss = {logs['loss']:.4f}, accuracy = {logs['accuracy']:.4f}, val_loss = {logs['val_loss']:.4f}, val_accuracy = {logs['val_accuracy']:.4f}"
        )


# Train the model
history = model.fit(
    X_train,
    y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.2,
    callbacks=[PrintEpochCallback()],
)

# Evaluate the model on test data
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"\nTest Accuracy: {test_accuracy:.2f}")

# Generate classification report
y_pred = np.argmax(model.predict(X_test), axis=1)
print("\nClassification Report:\n")
print(
    classification_report(
        y_test, y_pred, target_names=[f"Class {i}" for i in range(num_classes)]
    )
)

# Save the model in TensorFlow's SavedModel format
model.save("my_model.h5")

MODEL_LOCATION = "my_model.h5"

loaded_model = load_model(MODEL_LOCATION)  # load the model
print("loaded model from MODEL_LOCATION")


def convert_h5_to_aws_tf2(loaded_model):
    loaded_model.export(
        "export/servo/1", format="tf_saved_model", verbose=True, input_signature=None
    )

    import tarfile

    # Tar up the export directory
    with tarfile.open("model.tar.gz", mode="w:gz") as archive:
        archive.add("export", recursive=True)


convert_h5_to_aws_tf2(loaded_model)

inputs = sess.upload_data(path="model.tar.gz", key_prefix="model")

role = "arn for sagemaker execution role"

sagemaker_model = TensorFlowModel(
    model_data="s3://" + sess.default_bucket() + "/model/model.tar.gz",
    role=role,
    framework_version=tf_framework_version,
    entry_point="train.py",
)  # train.py can just be an empty file

# Deploy to an endpoint
predictor = sagemaker_model.deploy(
    initial_instance_count=1, instance_type="ml.m4.xlarge"
)
