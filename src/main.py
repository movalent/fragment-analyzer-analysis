import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths
from scipy.integrate import simpson
from pathlib import Path

import paths, file_utils, preprocess_data, peaks, plot

# from peak_adjustment import PeakEditor

# peaks_df_corr, valleys = find_valleys(df_raw, peaks_df, sample)

# print(peaks_df_corr)

# df_peaks = df_filtered.iloc[peaks]


# print('=================== Peaks properties ===================\n')
# for key, value in properties.items():
#     print(key, value)

# # Peak area
# peak_width_results = peak_widths(df_filtered[sample], peaks, rel_height=0.99)
# widths = peak_width_results[0]
# peak_start = peak_width_results[2]
# peak_end = peak_width_results[3]


def main() -> None:

    # Resolve paths
    dir_paths = paths.resolve_paths()

    # Load data
    raw_data = file_utils.load_data(dir_paths)

    selected_sample = preprocess_data.select_sample(raw_data)

    # Detect peaks
    peaks_df, properties = peaks.find_peaks(raw_data, selected_sample)

    print(peaks_df, properties)

    # Refine the peaks

    # Visualize the traces

    # Confirm dbDNA, dsCircle, product position

    # Adjust the peak boundaries

    # Calculate the peak percentages

    # Genera the graphs

    # Generate the peak summary tables



if __name__ == '__main__':
    main()

