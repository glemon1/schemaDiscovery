#!/usr/bin/env python3
import numpy as np

np.random.seed(1)
import tensorflow as tf

# tf.set_random_seed(1)
from tensorflow import keras
import csv
import math
from utils import normalize_input

data = []
labels = []

model = keras.models.Sequential()
model.add(keras.layers.Dense(64, input_shape=(4,), activation="relu"))
model.add(keras.layers.Dense(64, activation="relu"))
model.add(keras.layers.Dense(2))

print(model.summary())

model.compile(
    loss="mse",
    optimizer=keras.optimizers.SGD(learning_rate=0.1, nesterov=True),
    metrics=["mae"],
)

history = model.fit(
    train_data,
    train_labels,
    validation_data=(test_data, test_labels),
    epochs=2000,
    batch_size=2000,
)

print(test_data[3:6])
p = model.predict(test_data[3:6])
print(test_labels[3:6])
print(p)

import matplotlib.pyplot as plt

history_dict = history.history
loss_values = history_dict["loss"]
val_loss_values = history_dict["val_loss"]
accuracy = history_dict["mae"]
val_accuracy = history_dict["val_mae"]

epochs = range(1, len(loss_values) + 1)
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

model.save("model_weights")
#
# Plot the model accuracy (MAE) vs Epochs
#
ax[0].plot(epochs, accuracy, "bo", label="Training accuracy")
ax[0].plot(epochs, val_accuracy, "b", label="Validation accuracy")
ax[0].set_title("Training & Validation Accuracy", fontsize=16)
ax[0].set_xlabel("Epochs", fontsize=16)
ax[0].set_ylabel("Accuracy", fontsize=16)
ax[0].legend()
#
# Plot the loss vs Epochs
#
ax[1].plot(epochs, loss_values, "bo", label="Training loss")
ax[1].plot(epochs, val_loss_values, "b", label="Validation loss")
ax[1].set_title("Training & Validation Loss", fontsize=16)
ax[1].set_xlabel("Epochs", fontsize=16)
ax[1].set_ylabel("Loss", fontsize=16)
ax[1].legend()
plt.show()

# The results would be in the range of 0.98 or 0.02 cause we might #still be left with some error rate(which could've been fixed if we #used a bigger training set or different model parameters.
# Since we desire binary results, we just round the results using the #round function of Python.
# The predictions are actually in
# print([x for x in model.predict(test_data)])
