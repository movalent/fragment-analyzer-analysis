import pandas as pd

# from scipy.signal import find_peaks, peak_widths
import scipy

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
        'peak_end':     df['Size (bp)'].iloc[properties['right_bases']].values
        })

    # Keep only peaks that are within the ladder range, e.g. 75 - 20 000 bp
    peak_df = peak_df[(peak_df['peak_center'] > 74) & (peak_df['peak_center'] < 20001)]

    return peak_df, properties

def find_valleys(df_input, df_peaks, sample):
    valleys = []

    y_signal = df_input[sample].values
    x_size = df_input['Size (bp)'].values

    # Find valleys between peaks
    for i in range(len(df_peaks) - 1):
        left = df_peaks['peak_end'].iloc[i]
        right = df_peaks['peak_start'].iloc[i + 1]

        left_idx = np.searchsorted(x_size, left)
        right_idx = np.searchsorted(x_size, right)

        if right_idx <= left_idx:
            valley_index = left_idx
        else:
            segment = y_signal[left_idx : right_idx]
            valley_relative = np.argmin(segment)
            valley_index = left_idx + valley_relative


        valleys.append(valley_index)

    valleys = np.array(valleys)

    # Define new peak boundaries
    starts_corr = []
    ends_corr = []
    peaks_idx = df_peaks['peak_index'].values

    for i in range(len(peaks_idx)):
        if i == 0:
            start = df_peaks['peak_start'].iloc[i]  # keep original
        else:
            start = x_size[valleys[i - 1]]  # valley before

        if i == len(peaks_idx) - 1:
            end = df_peaks['peak_end'].iloc[i]
        else:
            end = x_size[valleys[i]]

        starts_corr.append(start)
        ends_corr.append(end)

    result = pd.DataFrame({
        'peak_index':       peaks_idx,
        'peak_height':      df_peaks['peak_height'].values,
        'peak_start_corr':  starts_corr,
        'peak_center_corr': x_size[peaks_idx],
        'peak_end_corr':    ends_corr
        })

    return result, valleys
