import paths, file_utils, preprocess_data, peaks, plot

def main() -> None:

    # Resolve paths
    dir_paths = paths.resolve_paths()

    # Load data
    raw_data = file_utils.load_data(dir_paths)

    selected_sample = preprocess_data.select_sample(raw_data)
    data_no_ladder = preprocess_data.remove_ladder_well(raw_data)

    # Detect peaks
    peaks_df, properties = peaks.find_peaks(data_no_ladder, selected_sample)

    # Refine the peaks
    peaks_corr = peaks.adjust_peak_boundaries(data_no_ladder, peaks_df, selected_sample)

    # Visualize the traces
    plot.plot_trace(data_no_ladder, peaks_corr, selected_sample)

    # Confirm dbDNA, dsCircle, product position
    ref_peaks = peaks.find_ref_points(data_no_ladder)

    file_utils.save_adjusted_peaks(dir_paths, selected_sample, peaks_corr)

    # Manually adjust the peak boundaries

    # Calculate the peak percentages

    # Generate the graphs

    # Generate the peak summary tables

if __name__ == '__main__':
    main()
