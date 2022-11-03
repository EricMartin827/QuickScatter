import os
import sys

unit_test_dir = os.path.dirname(__file__)
root_dir = os.path.join(unit_test_dir, '..')
sys.path.append(root_dir)

from utils.UpperBounds import (BuffonCoin, JointBuffonCoin)


def test_buffon_coin():

    height, width, marker_size, beta = 500, 500, 5, 0.5
    N_actual = BuffonCoin(height, width, marker_size, beta)()
    N_expected = 1465

    assert N_actual == N_expected

def test_joint_buffon_coin():
    height, width, marker_size, beta = 500, 500, 5, 0.5
    N_actual = JointBuffonCoin(height, width, marker_size, beta)()
    N_expected = 17

    assert N_actual == N_expected
