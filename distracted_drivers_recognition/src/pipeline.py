import os
import random
import config as conf
import utils
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow import keras

image_size = (conf.IMG_ROWS, conf.IMG_COLS)
batch_size = conf.BATCH_SIZE


# Create the model
def make_model(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)
    # Image augmentation block
    x = data_augmentation(inputs)

    # Entry block
    x = layers.Rescaling(1.0 / 255)(x)
    x = layers.Conv2D(32, 3, strides=2, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.Conv2D(64, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    previous_block_activation = x  # Set aside residual

    for size in [128, 256, 512, 728]:
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)

        # Project residual
        residual = layers.Conv2D(size, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    x = layers.SeparableConv2D(1024, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.GlobalAveragePooling2D()(x)
    if num_classes == 2:
        activation = "sigmoid"
        units = 1
    else:
        activation = "softmax"
        units = num_classes

    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(units, activation=activation)(x)
    return keras.Model(inputs, outputs)


if __name__ == "__main__":
    # Load the data
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        conf.TRAINING_IMAGES_PATH,
        validation_split=conf.TRAIN_VAL_SPLIT,
        subset="training",
        seed=1337,
        image_size=image_size,
        batch_size=batch_size,
        shuffle=True,
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        conf.TRAINING_IMAGES_PATH,
        validation_split=conf.TRAIN_VAL_SPLIT,
        subset="validation",
        seed=1337,
        image_size=image_size,
        batch_size=batch_size,
        shuffle=True,
    )

    with tf.device('/cpu:0'):
        data_augmentation = keras.Sequential(
            [
                layers.RandomRotation(0.15),
            ]
        )

    train_ds = train_ds.prefetch(buffer_size=batch_size)
    val_ds = val_ds.prefetch(buffer_size=batch_size)

    model = make_model(input_shape=image_size + (3,), num_classes=conf.NUM_CLASSES)
    keras.utils.plot_model(model, "model.png", show_shapes=True)

    # Add callbacks
    callbacks = [
        keras.callbacks.ModelCheckpoint(filepath=os.path.join(conf.OUTPUT_PATH,
                                                              "base_model_ep_{epoch}_val_acc_{val_accuracy:.2f}.h5"),
                                        save_best_only=True,
                                        monitor="val_accuracy"),
        keras.callbacks.TensorBoard(log_dir=conf.LOG_DIR)
    ]

    # Compile the model
    model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    # Train the model
    # with tf.device("/gpu:0"):
    #     model.fit(
    #         train_ds, epochs=conf.NUM_EPOCHS, callbacks=callbacks, validation_data=val_ds,
    #     )

    # Use a trained model
    model = keras.models.load_model(os.path.join(conf.OUTPUT_PATH, "base_model_ep_10_val_acc_0.82.h5"))

    # Evaluate the model
    test_files = os.listdir(conf.TEST_IMAGES_PATH)
    random_img = random.choice(test_files)

    img = keras.preprocessing.image.load_img(
        os.path.join(conf.TEST_IMAGES_PATH, random_img), target_size=image_size
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    predictions = model.predict(img_array)

    # Show the random image and the predictions
    utils.show_image(img_array, predictions[0])
