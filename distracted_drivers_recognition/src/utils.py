import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import config as conf


# Visualize the data
def show_images(ds):
    plt.figure(figsize=(10, 10))
    for image, label in ds.take(1):
        for i in range(9):
            plt.subplot(3, 3, i + 1)
            plt.imshow(image[i].numpy().astype("uint8"))
            plt.title(int(label[i]))
            plt.axis("off")
    plt.show()


# Visualize the data augmentation
def show_images_augmented(ds, data_augmentation):
    plt.figure(figsize=(10, 10))
    for images, _ in ds.take(1):
        for i in range(9):
            augmented_images = data_augmentation(images)
            _ = plt.subplot(3, 3, i + 1)
            plt.imshow(augmented_images[0].numpy().astype("uint8"))
            plt.axis("off")
    plt.show()


# Visualize an image and its label
def show_image(image, score):
    plt.figure(figsize=(10, 10))
    plt.imshow(tf.squeeze(image).numpy().astype("uint8"))
    plt.title(f"Label: {conf.LABELS[np.argmax(score)]} / Score: {np.max(score):.2f}")
    plt.axis("off")
    plt.show()
