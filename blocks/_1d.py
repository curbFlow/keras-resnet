# -*- coding: utf-8 -*-

"""
keras_resnet.blocks._1d
~~~~~~~~~~~~~~~~~~~~~~~

This module implements a number of popular one-dimensional residual blocks.
"""

import keras.layers
import keras.regularizers

from .. import layers

parameters = {
    "kernel_initializer": "he_normal"
}


def basic_1d(
    filters,
    stage=0,
    block=0,
    kernel_size=3,
    numerical_name=False,
    stride=None,
    freeze_bn=False
):
    """
    A one-dimensional basic block.

    :param filters: the output’s feature space

    :param stage: int representing the stage of this block (starting from 0)

    :param block: int representing this block (starting from 0)

    :param kernel_size: size of the kernel

    :param numerical_name: if true, uses numbers to represent blocks instead of chars (ResNet{101, 152, 200})

    :param stride: int representing the stride used in the shortcut and the first conv layer, default derives stride from block id

    :param freeze_bn: if true, freezes BatchNormalization layers (ie. no updates are done in these layers)

    Usage:

        >>> import keras_resnet.blocks

        >>> keras_resnet.blocks.basic_1d(64)
    """
    if stride is None:
        if block != 0 or stage == 0:
            stride = 1
        else:
            stride = 2

    if keras.backend.image_data_format() == "channels_last":
        axis = -1
    else:
        axis = 1

    if block > 0 and numerical_name:
        block_char = "b{}".format(block)
    else:
        block_char = chr(ord('a') + block)

    stage_char = str(stage + 2)

    def f(x):
        y = keras.layers.ZeroPadding1D(
            padding=1, 
            name="padding{}{}_branch2a".format(stage_char, block_char)
        )(x)
        
        y = keras.layers.Conv1D(
            filters,
            kernel_size,
            strides=stride,
            use_bias=False,
            name="res{}{}_branch2a".format(stage_char, block_char),
            **parameters
        )(y)
        
        y = layers.BatchNormalization(
            axis=axis,
            epsilon=1e-5,
            freeze=freeze_bn,
            name="bn{}{}_branch2a".format(stage_char, block_char)
        )(y)
        
        y = keras.layers.Activation(
            "relu",
            name="res{}{}_branch2a_relu".format(stage_char, block_char)
        )(y)

        y = keras.layers.ZeroPadding1D(
            padding=1,
            name="padding{}{}_branch2b".format(stage_char, block_char)
        )(y)
        
        y = keras.layers.Conv1D(
            filters,
            kernel_size,
            use_bias=False,
            name="res{}{}_branch2b".format(stage_char, block_char),
            **parameters
        )(y)
        
        y = layers.BatchNormalization(
            axis=axis,
            epsilon=1e-5,
            freeze=freeze_bn,
            name="bn{}{}_branch2b".format(stage_char, block_char)
        )(y)

        if block == 0:
            shortcut = keras.layers.Conv1D(
                filters,
                1,
                strides=stride,
                use_bias=False,
                name="res{}{}_branch1".format(stage_char, block_char),
                **parameters
            )(x)

            shortcut = layers.BatchNormalization(
                axis=axis,
                epsilon=1e-5,
                freeze=freeze_bn,
                name="bn{}{}_branch1".format(stage_char, block_char)
            )(shortcut)
        else:
            shortcut = x

        y = keras.layers.Add(
            name="res{}{}".format(stage_char, block_char)
        )([y, shortcut])
        
        y = keras.layers.Activation(
            "relu",
            name="res{}{}_relu".format(stage_char, block_char)
        )(y)

        return y

    return f


def bottleneck_1d(
    filters,
    stage=0,
    block=0,
    kernel_size=3,
    numerical_name=False,
    stride=None,
    freeze_bn=False
):
    """
    A one-dimensional bottleneck block.

    :param filters: the output’s feature space

    :param stage: int representing the stage of this block (starting from 0)

    :param block: int representing this block (starting from 0)

    :param kernel_size: size of the kernel

    :param numerical_name: if true, uses numbers to represent blocks instead of chars (ResNet{101, 152, 200})

    :param stride: int representing the stride used in the shortcut and the first conv layer, default derives stride from block id

    :param freeze_bn: if true, freezes BatchNormalization layers (ie. no updates are done in these layers)

    Usage:

        >>> import keras_resnet.blocks

        >>> keras_resnet.blocks.bottleneck_1d(64)
    """
    if stride is None:
        stride = 1 if block != 0 or stage == 0 else 2

    if keras.backend.image_data_format() == "channels_last":
        axis = -1
    else:
        axis = 1

    if block > 0 and numerical_name:
        block_char = "b{}".format(block)
    else:
        block_char = chr(ord('a') + block)

    stage_char = str(stage + 2)

    def f(x):
        y = keras.layers.Conv1D(
            filters,
            1,
            strides=stride,
            use_bias=False,
            name="res{}{}_branch2a".format(stage_char, block_char),
            **parameters
        )(x)

        y = layers.BatchNormalization(
            axis=axis,
            epsilon=1e-5,
            freeze=freeze_bn,
            name="bn{}{}_branch2a".format(stage_char, block_char)
        )(y)

        y = keras.layers.Activation(
            "relu",
            name="res{}{}_branch2a_relu".format(stage_char, block_char)
        )(y)

        y = keras.layers.ZeroPadding1D(
            padding=1,
            name="padding{}{}_branch2b".format(stage_char, block_char)
        )(y)

        y = keras.layers.Conv1D(
            filters,
            kernel_size,
            use_bias=False,
            name="res{}{}_branch2b".format(stage_char, block_char),
            **parameters
        )(y)

        y = layers.BatchNormalization(
            axis=axis,
            epsilon=1e-5,
            freeze=freeze_bn,
            name="bn{}{}_branch2b".format(stage_char, block_char)
        )(y)

        y = keras.layers.Activation(
            "relu",
            name="res{}{}_branch2b_relu".format(stage_char, block_char)
        )(y)

        y = keras.layers.Conv1D(
            filters * 4,
            1,
            use_bias=False,
            name="res{}{}_branch2c".format(stage_char, block_char),
            **parameters
        )(y)

        y = layers.BatchNormalization(
            axis=axis,
            epsilon=1e-5,
            freeze=freeze_bn,
            name="bn{}{}_branch2c".format(stage_char, block_char)
        )(y)

        if block == 0:
            shortcut = keras.layers.Conv1D(
                filters * 4,
                1,
                strides=stride,
                use_bias=False,
                name="res{}{}_branch1".format(stage_char, block_char),
                **parameters
            )(x)

            shortcut = layers.BatchNormalization(
                axis=axis,
                epsilon=1e-5,
                freeze=freeze_bn,
                name="bn{}{}_branch1".format(stage_char, block_char)
            )(shortcut)
        else:
            shortcut = x

        y = keras.layers.Add(
            name="res{}{}".format(stage_char, block_char)
        )([y, shortcut])

        y = keras.layers.Activation(
            "relu",
            name="res{}{}_relu".format(stage_char, block_char)
        )(y)

        return y

    return f
