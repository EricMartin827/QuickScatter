#!/usr/bin/env python

"""

This module is a library of functions to abstract the data preparation phase
from the data anaylysis phase for the baseball dataset. Functions where
generated from Initial Baseball Data Exploration Jupyter Notebook.

"""
################################################################################
############################# Python System Imports ############################
################################################################################

import os
import sys
import numpy as np
import pandas as pd
import plotly.offline as py
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go

################################################################################
############################## Constnt Variables ###############################
################################################################################

"""
All Pitch Types Present in the Baseball Dataset.
"""
PITCH_TYPES = [
    'Four Seam Fastball',
    'Slider',
    'Two Seam Fastball',
    'Changeup',
    'Sinker',
    'Curveball',
    'Cutter',
    'Knuckle Curve',
    'Splitter',
    'Knuckleball',
    'Eephus',
    'Pitch Out',
    'Pitch Out',
    'Screwball',
    'Unidentified',
    'Fastball',
    'Intentional Ball'
]

"""
All Possible Resutls From a Given Pitch in the Baseball Dataset.
"""
CODE_TYPES = [
    'Ball',
    'Ball In Dirt',
    'Swinging Strike',
    'Called Strike',
    'Foul',
    'Foul Tip',
    'Foul Bunt',
    'Intentional Ball',
    'Blocked',
    'Missed Bunt',
    'Pitch Out',
    'Swinging Pitch Out',
    'Foul Pitch Out',
    'In Play Out(s)',
    'In Play No Out',
    'In Play Runs'
]

################################################################################
############################### Hidden Functions ###############################
################################################################################

def construct_data_paths(data_dir: str):

    if len(data_dir) == 0:
        raise ValueError(str.format("Empty Data Directory Specified."))
    elif not os.path.exists(data_dir):
        raise ValueError(str.format("Input Directory {} Does Not Exist!", data_dir))

    paths = dict(
        games=os.path.join(data_dir, "games.csv"),
        players=os.path.join(data_dir, "player_names.csv"),
        pitches=os.path.join(data_dir, "pitches.csv"),
        atbats=os.path.join(data_dir, "atbats.csv")
    )

    for path in paths.values():
        if not os.path.exists(path):
            raise ValueError(str.format("Failed To Locate {}!", path))

    return paths


def construct_data_frame(paths: dict):

    games   = pd.read_csv(paths['games'])

    players = pd.read_csv(paths['players'])
    players.rename(columns={'id': 'batter_id'}, inplace=True) ### Rename

    pitches = pd.read_csv(paths['pitches'])
    pitches['ab_id'] = pitches['ab_id'].astype(int) ### Convert

    atbats = pd.read_csv(paths['atbats'])

    ### Project At Bats Onto Pitches Via At Bat ID
    p_b = pd.merge(pitches, atbats,
                   how='left', left_on='ab_id', right_on='ab_id')

    ### Project Games Onto Target Via Game ID
    p_b_g = pd.merge(p_b, games,
                     how='left', left_on='g_id', right_on='g_id')

    ### Project Player Onto Target Via Their Batter Id For Final Dataframe
    df = pd.merge(p_b_g, players,
                  how='left', left_on='batter_id', right_on='batter_id')

    ### Merge Batter First And Last Names for Ease of Access
    ### names is a tuple(first_name, last_name)
    df['batters_name'] = df[['first_name', 'last_name']].apply(
        lambda names: " ".join(names), axis=1)
    df.drop(['first_name', 'last_name'], axis=1, inplace=True)

    ### Now Project Pitchers Onto All the Pitches Dataframe
    players.rename(columns={'batter_id': 'pitcher_id'}, inplace=True)
    df = pd.merge(df, players,
                  how='left', left_on='pitcher_id', right_on='pitcher_id')

    df['pitcher_name'] = df[['first_name', 'last_name']].apply(
        lambda names: " ".join(names), axis=1)
    df.drop(['first_name', 'last_name'], axis=1, inplace=True)

    return df

def update_baseball_codes(df):

    ### Update Pitch Type To Verbose Description
    pitch_type_map = dict({
        'FF': 'Four Seam Fastball',
        'SL': 'Slider',
        'FT': 'Two Seam Fastball',
        'CH': 'Changeup',
        'SI': 'Sinker',
        'CU': 'Curveball',
        'FC': 'Cutter',
        'KC': 'Knuckle Curve',
        'FS': 'Splitter',
        'KN': 'Knuckleball',
        'EP': 'Eephus',
        'FO': 'Pitch Out',
        'PO': 'Pitch Out',
        'SC': 'Screwball',
        'UN': 'Unidentified',
        'FA': 'Fastball',
        'IN': 'Intentional Ball'
    })
    df['pitch_type'] = df['pitch_type'].map(pitch_type_map)

    ### Update Batting Result Code To Verbose Desription
    code_type_map = dict({
        'B':  'Ball',
        '*B': 'Ball In Dirt',
        'S':  'Swinging Strike',
        'C':  'Called Strike',
        'F':  'Foul',
        'T':  'Foul Tip',
        'L':  'Foul Bunt',
        'I':  'Intentional Ball',
        'W':  'Blocked',
        'M':  'Missed Bunt',
        'P':  'Pitch Out',
        'Q':  'Swinging Pitch Out',
        'R':  'Foul Pitch Out',
        'X':  'In Play Out(s)',
        'D':  'In Play No Out',
        'E':  'In Play Runs'
    })
    df['code'] = df['code'].map(code_type_map)


################################################################################
############################### Public Functions ###############################
################################################################################


def get_pitch_locations(df, code_type=None):
    if code_type is None:
        raise ValueError("get_pitch_location() -> Failed To Specify Code Type")
    pos_x = df.px[df.code == code_type]
    pos_z = df.pz[df.code == code_type]
    return pd.DataFrame(data=dict(x=pos_x, y=pos_z))


def scatter_trace(df, name, color, marker_size):
    return go.Scatter(
        x=df.x,
        y=df.y,
        name=name,
        mode='markers',
        marker=dict(
            size=marker_size,
            color=color,
            line=dict(width=2, color=color)
        )
    )


def build_sample_slider_figure(df, name, sample_rates, color, marker_size):
    figure = go.Figure()
    for rate in sample_rates:
        indices = np.random.choice(len(df), int(rate*len(df)), replace=False)
        trace = go.Scatter(x=df.x.iloc[indices], y=df.y.iloc[indices],
                           visible=False, name=name, mode='markers',
                           marker=dict(
                               size=marker_size,
                               color=color,
                               line=dict(width=2, color=color)))
        figure.add_trace(trace)

    steps = []
    for i in range(len(figure.data)):
        step = dict(
            method='update',
            args=[
                dict(visible=[False]*len(figure.data)),
                dict(title='Sample Rate {}'.format(sample_rates[i]))
            ])
        step['args'][0]['visible'][i] = True ### Make This i Slice of Data Visible
        steps.append(step)

    sliders = [
        dict(
            active=10,
            currentvalue={'prefix': 'Sample Rate {}'.format(sample_rates[i])},
            pad={'t':50},
            steps=steps
        )
    ]

    return figure, sliders


def generate_sampled_pitch_view(df, name, sample_rates, color, marker_size):
    figure = go.Figure()
    for rate in sample_rates:
        indices = np.random.choice(len(df), int(rate*len(df)), replace=False)
        trace = go.Scatter(x=df.x.iloc[indices], y=df.y.iloc[indices],
                           visible=False, name=name, mode='markers',
                           marker=dict(
                               size=marker_size,
                               color=color,
                               line=dict(width=2, color=color)))
        figure.add_trace(trace)

    ### Make First Data Set Visble On Initial Render
    figure.data[0].visible = True

    steps = []
    for i in range(len(figure.data)):
        step = dict(
            method='update',
            args=[
                dict(visible=[False]*len(figure.data)),
                dict(title='Sample Rate {}'.format(sample_rates[i]))
            ])
        step['args'][0]['visible'][i] = True ### Make This i Slice of Data Visible
        steps.append(step)

    slider_descriptions = [
        dict(
            active=10,
            currentvalue={'prefix': 'Sample Rate'},
            pad={'t':50},
            steps=steps
        )
    ]

    #######################################################
    ### Return Tuple so that caller can invoke ...
    ### figure.update_layout(sliders=slider_descriptions)
    #######################################################
    return figure, slider_descriptions

def load_baseball_df(data_dir: str):
    paths = construct_data_paths(data_dir)
    df = construct_data_frame(paths)
    update_baseball_codes(df)
    return df


################################################################################
############################# Local Testing ####################################
################################################################################

def test_loading():
    df = load_baseball_df("./../data/")
    print("Total Number Of Pictches For 4 Seasons: {}".format(len(df)))

if __name__ == "__main__":
    test_loading()
