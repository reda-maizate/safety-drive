import os
import config as conf
import tensorflow as tf
from tensorflow import keras
from tqdm.keras import TqdmCallback

from model import model
from preprocess import train_ds, val_ds


if __name__ == "__main__":
    # Create needed directories
    if not os.path.exists(conf.OUTPUT_PATH):
        os.makedirs(conf.OUTPUT_PATH, exist_ok=True)
    if not os.path.exists(conf.LOG_DIR):
        os.makedirs(conf.LOG_DIR, exist_ok=True)

    # Add callbacks
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            filepath=os.path.join(
                conf.OUTPUT_PATH, "base_model_ep_{epoch}_val_acc_{val_accuracy:.2f}.h5"
            ),
            save_best_only=True,
            monitor="val_accuracy",
        ),
        keras.callbacks.TensorBoard(log_dir=conf.LOG_DIR),
        TqdmCallback(),
    ]

    # Compile the model
    model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    # Train the model
    with tf.device("/gpu:0"):
        model.fit(
            train_ds,
            epochs=conf.NUM_EPOCHS,
            callbacks=callbacks,
            validation_data=val_ds,
            verbose=0,
        )
