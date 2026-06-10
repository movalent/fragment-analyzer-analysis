import pandas as pd

import scipy
import numpy as np

def find_peaks(input_df: pd.DataFrame, sample: str) -> tuple[pd.DataFrame, dict]:

    df = input_df.copy()

    peaks, properties = scipy.signal.find_peaks(
        df[sample],
        height=100,
        prominence=10
        )

    peak_df = pd.DataFrame(
        {'peak_index':  peaks,
        'peak_height':  df[sample].iloc[peaks],
        'peak_start':   df['Size (bp)'].iloc[properties['left_bases']].values,
        'peak_center':  df['Size (bp)'].iloc[peaks],
        'peak_end':     df['Size (bp)'].iloc[properties['right_bases']].values,
        'peak_start_idx': properties['left_bases'],
        'peak_end_idx':   properties['right_bases']
        })

    return peak_df, properties

def adjust_peak_boundaries(df_input, df_peaks, sample):

    df_p = df_peaks.copy()

    # Remove lower and upper markers from data
    y_signal = df_input[sample]

    # Find valleys between peaks
    for i in range(len(df_p) - 1):
        curr_peak_end = df_p['peak_end'].iloc[i]
        next_peak_start = df_p['peak_start'].iloc[i + 1]

        curr_peak_centre = df_p['peak_index'].iloc[i]
        next_peak_centre = df_p['peak_index'].iloc[i + 1]

        curr_peak_idx = df_p.iloc[i]['peak_index']
        next_peak_idx = df_p.iloc[i + 1]['peak_index']

        if curr_peak_end > next_peak_start:

            segment = y_signal.iloc[curr_peak_centre : next_peak_centre + 1]  # +1 to account for not inclusive slicing index

            valley_idx = np.argmin(segment) + curr_peak_centre  # valley is an offset from the 1st peak

            df_p.at[curr_peak_idx, 'peak_end_idx'] = valley_idx
            df_p.at[next_peak_idx, 'peak_start_idx'] = valley_idx

            df_p.at[curr_peak_idx, 'peak_end'] = df_input.iloc[valley_idx]['Size (bp)']
            df_p.at[next_peak_idx, 'peak_start'] = df_input.iloc[valley_idx]['Size (bp)']

    return df_p


