import cv2
import numpy as np
import os
import sys
import tensorflow as tf
from tensorflow.keras import layers

from sklearn.model_selection import train_test_split


os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU
EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4
dataDir = "Home/Desktop/CS50_50/5.\ Neural\ Networks/traffic"


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    path = os.path.normpath(data_dir)

    label = -1
    images = []
    labels = []

    for root, dirs, file in os.walk(path):
        for sub_dir in dirs:
            label += 1
            sub_dir_path = os.path.join(root, sub_dir)
            for file in os.listdir(sub_dir_path):
                file_path = os.path.join(sub_dir_path, file)
                img = cv2.imread(file_path, 1)
                if img is None:
                    raise NotImplementedError
                resizedImg = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
                images.append(resizedImg)
                labels.append(label)

    return (images, labels)

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    model = tf.keras.Sequential()

    model.add(layers.InputLayer(input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)))
    model.add(layers.Conv2D(32, (3,3), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2,2)))
    model.add(layers.Conv2D(32, (3,3), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Conv2D(32, (3, 3), activation='sigmoid'))
    model.add(layers.Flatten())


    model.add(layers.Dense(NUM_CATEGORIES, activation='softmax'))


    model.compile(
        optimizer='adam',
        # Loss function to minimize
        loss='categorical_crossentropy',
        # List of metrics to monitor
        metrics=['accuracy'],
    )

    return model

if __name__ == "__main__":
    main()
