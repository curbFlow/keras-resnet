# -*- coding: utf-8 -*-

"""
keras_resnet.models
~~~~~~~~~~~~~~~~~~~

This module implements popular residual models.
"""

from ._2d import (
    ResNet2D,
    ResNet2D18,
    ResNet2D34,
    ResNet2D50,
    ResNet2D101,
    ResNet2D152,
    ResNet2D200
)


from ._feature_pyramid_2d import (
    FPN2D,
    FPN2D18,
    FPN2D34,
    FPN2D50,
    FPN2D101,
    FPN2D152,
    FPN2D200
)


# for backwards compatibility reasons
ResNet = ResNet2D
ResNet18 = ResNet2D18
ResNet34 = ResNet2D34
ResNet50 = ResNet2D50
ResNet101 = ResNet2D101
ResNet152 = ResNet2D152
ResNet200 = ResNet2D200
