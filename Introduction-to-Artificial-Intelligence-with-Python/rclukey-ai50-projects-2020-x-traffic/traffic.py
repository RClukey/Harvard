import cv2
import numpy as np
import os
os.environ["CUDA_VISIBLE_DEVICES"] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])
    
    print(len(images))
    print(len(labels))
    print(images[0].shape)
    
    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels, NUM_CATEGORIES, 'int')
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )
    
    print(len(labels))
    print("x_train:", x_train.shape)
    print("x_test:", x_test.shape)
    print("y_train:", len(y_train))
    print("y_test:", len(y_test))

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
    
    images = list()
    labels = list()
    
    for category in os.listdir(data_dir):
        image_directory_path = os.path.join(data_dir, category)
        for file in os.listdir(image_directory_path):
            file_path = os.path.join(image_directory_path, file)
            image = cv2.imread(file_path, cv2.IMREAD_COLOR)
            image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_AREA)
            images.append(image)
            labels.append(int(category))
    
    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation = "relu", input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.MaxPooling2D(pool_size = (2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.40),
        tf.keras.layers.Dense(NUM_CATEGORIES * 5, activation = "relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES * 12, activation = "relu"),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation = "softmax")
        ])
    
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
        )
    
    return model


if __name__ == "__main__":
    main()













