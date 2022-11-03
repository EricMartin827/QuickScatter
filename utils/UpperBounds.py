#!/usr/bin/env python

"""

This module constains upper bound estimate calculations for various sampling
methodologies.

"""

import os
import sys
import numpy as np

class UpperBoundBase(object):

    def __init__(self, height, width, marker_radius):
        self.height = height
        self.width = width
        self.marker_radius = marker_radius


class BuffonCoin(UpperBoundBase):

    def __init__(self, height, width, marker_radius, beta):
        super().__init__(height=height, width=width, marker_radius=marker_radius)
        self.beta = beta

    def __call__(self):
        H, W, R, beta = self.height, self.width, self.marker_radius, self.beta
        return np.divide(
            ((H - 2*R) * (W - 2*R)) - (beta * H * W),
            np.pi * R**2
        ).astype(int)

class JointBuffonCoin(UpperBoundBase):

    def __init__(self, height, width, marker_radius, beta):
        super().__init__(height=height, width=width, marker_radius=marker_radius)
        self.beta = beta

    def __call__(self):
        H, W, R, beta = self.height, self.width, self.marker_radius, self.beta

        total_area = H * W
        freespace = (H - 2*R) * (W - 2*R)
        marker_area = np.pi * (R**2)

        score, threshold = 0.0, np.log(1 - beta)

        N = BuffonCoin(H, W, R, beta)()

        for n in range(1, N):
            prob = (freespace - ((n - 1) * marker_area)) / total_area
            score += np.log(prob)
            if score <= threshold:
                return n

        return N

