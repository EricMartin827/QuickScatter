#!/usr/bin/env python

"""

This module contains all the sampling methods used to generate useful
scatter plots.

"""

import os
import sys
import numpy as np


class SamplingBase(object):
    
    def __init__(self, sample_rate: float):
        self.sample_rate = sample_rate


class UniformRandom(SamplingBase):

    def __call__(self, data):
        N = data.shape[0]
        num_samples = round(N * self.sampling_rate)
        return data[np.random.permutation(N)[:num_samples]]
