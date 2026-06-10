import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths
from pathlib import Path

import paths, file_utils, preprocess_data, peaks, plot

# from peak_adjustment import PeakEditor

def main() -> None:

    # Resolve paths
    dir_paths = paths.resolve_paths()

    # Load data
    raw_data = file_utils.load_data(dir_paths)

    selected_sample = preprocess_data.select_sample(raw_data)

    # Detect peaks
    peaks_df, properties = peaks.find_peaks(raw_data, selected_sample)
    # print('====== Raw peaks\n', peaks_df)

    # Refine the peaks
    peaks_corr = peaks.adjust_peak_boundaries(raw_data, peaks_df, selected_sample)
    # print('====== Corrected peaks\n', peaks_corr)

    # Visualize the traces
    plot.plot_trace(raw_data, peaks_corr, selected_sample)

    # Confirm dbDNA, dsCircle, product position

    # Manually adjust the peak boundaries

    # Calculate the peak percentages

    # Generate the graphs

    # Generate the peak summary tables



if __name__ == '__main__':
    main()

