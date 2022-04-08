from concurrent.futures import process
from pathlib import Path
import os
import os
import glob
import gin

import numpy as np
import tensorflow as tf
import subprocess
from ddsp.training.data_preparation.prepare_tfrecord_lib import prepare_tfrecord
from ddsp.colab import colab_utils
from ddsp.colab.colab_utils import play, specplot

from matplotlib import pyplot as plt

# Check for project path
PROJECT_PATH = Path('.').resolve()
print("PROJECT_PATH:", PROJECT_PATH)

if not PROJECT_PATH.exists():
    raise Exception(f'Project path {PROJECT_PATH} does not exist')

# Check if separated data exists
TRAINING_DATASET_PATH = f"{str(PROJECT_PATH)}/training_data"
if not Path(TRAINING_DATASET_PATH).exists():
    raise Exception(
        f"Training dataset path not found at '{TRAINING_DATASET_PATH}'")

# Check for checkpoints path
CHECKPOINTS_PATH = f"{str(PROJECT_PATH)}/checkpoints"
if not Path(CHECKPOINTS_PATH).exists():
    os.mkdir(CHECKPOINTS_PATH)
    assert Path(CHECKPOINTS_PATH).exists()

# Check for gins path
GINS_PATH = f"{str(PROJECT_PATH)}/gins"
if not Path(GINS_PATH).exists():
    raise Exception(f"Gins path not found at '{GINS_PATH}'")

# Environment variables:
SAMPLE_RATE = 16000
FRAME_RATE = 250


def train(relative_path, gin_file="singing_default.gin", save_tag=None):
    dataset_pattern = f"{TRAINING_DATASET_PATH}/{str(relative_path)}/*"

    if not Path(dataset_pattern[:-2]).exists():
        raise Exception(
            f"The dataset path {dataset_pattern[:-2]} doesn't exist")

    gin_file_path = f"{GINS_PATH}/{gin_file}"

    # Make custom save path
    if save_tag is None:
        save_path = f"{CHECKPOINTS_PATH}/{relative_path}"
    else:
        save_path = f"{CHECKPOINTS_PATH}/{save_tag}"

    if not Path(save_path).exists():
        os.mkdir(save_path)
        assert Path(save_path).exists()

        # Load gin config
        gin.parse_config_file(gin_file_path)

        prepare_tfrecord()


def train_multiple(relative_path, n_pairs):
    for pair in n_pairs:
        save_tag = f"{relative_path}_h{pair[0]}_n{pair[1]}"
        print(f"Training {save_tag}")
        train(relative_path, "z.gin", save_tag=save_tag)


if __name__ == "__main__":
    pairs = [
        (20, 10),
        (20, 30),
        (20, 60),
        (20, 80),
        (60, 10),
        (60, 30),
        (60, 60),
        (60, 80),
        (100, 10),
        (100, 30),
        (100, 60),
        (100, 80),
    ]

    train_multiple("ColdplaySelected", pairs)
