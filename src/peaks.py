import pandas as pd
import re

import scipy
import numpy as np

def find_peaks(input_df: pd.DataFrame, sample: str) -> tuple[pd.DataFrame, dict]:
    """
    Detect peaks in a selected sample trace.

    Peaks are identified using `scipy.signal.find_peaks`

    Args:
        input_df (pd.DataFrame): DataFrame containing raw traces data.
        sample (str): Name of the sample column to analyse.

    Returns:
        tuple[pd.DataFrame, dict]:
            - pd.DataFrame: Table containing peak information, including
              indices, heights, and start/center/end positions in base pairs.
            - Dictionary of peak properties returned by scipy.signal.find_peaks.
    """

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

def auto_adjust_peak_boundaries(df_input: pd.DataFrame, df_peaks: list, sample: str) -> pd.DataFrame:
    """
    Adjusts the peak start and end when overlaping peaks are detected.

    Args:
        df_input (pd.DataFrame): DataFrame containing raw traces data
        df_peaks (list): List containing detected peaks indexes
        sample (str): Name of currently procesed sample

    Returns:
        pd.DataFrame: pd.DataFrame with adjusted peak boundaries.

    Notes:
        Function finds minimum value between two neighbouring peaks and adjust the boundaries accordingly.
    """

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

def find_ref_points(input_df: pd.DataFrame) -> dict[str, dict[str, int]]:
    """
    Find construct-specific dbDNA, dbDNA dimer, and dsCircle reference positions.
    Technical replicate positions are averaged before being rounded to the nearest base pair.

    The tallest detected peak in each dbDNA trace is selected as the main reference, and
    peak within +/-10% of twice that position is optionally recorded as the dbDNA dimer.

    Sample names must follow the format `A1: 210-185 dbDNA` or `A5: 210-185 T5 (dsC)`.

    Args:
        input_df (pd.DataFrame): DataFrame containing raw trace data. 

    Returns:
        dict[str, dict[str, int]]: Mapping of construct with its reference positions.

    Raises:
        ValueError: If a reference trace cannot be parsed or contains no detectable peaks.
    """

    LOW_MARKER_BOUNDARY = 80
    HIGH_MARKER_BOUNDARY = 19500

    reference_pattern = re.compile(
        r'^[^:]+:\s+(?P<construct>\d{3}-\d{3})\s+(?P<reference>dbDNA|T5)'
    )
    reference_peaks: dict[str, dict[str, list[float]]] = {}

    for sample in input_df.columns[1:]:
        if 'dbDNA' not in sample and 'T5' not in sample:
            continue

        match = reference_pattern.search(sample)
        if match is None:
            raise ValueError(f'Could not parse reference sample name: {sample}')

        construct = match.group('construct').strip()
        reference = match.group('reference').strip()

        peak_df, _ = find_peaks(input_df, sample)
        if peak_df.empty:
            raise ValueError(f'No detectable peaks found in reference sample: {sample}')

        peaks_no_markers_mask = (
            (peak_df['peak_center'] > LOW_MARKER_BOUNDARY) &
            (peak_df['peak_center'] <= HIGH_MARKER_BOUNDARY)
            )
        peaks_no_markers = peak_df[peaks_no_markers_mask]

        main_peak_index = peaks_no_markers['peak_height'].idxmax()
        main_peak = float(peaks_no_markers.loc[main_peak_index, 'peak_center'])
        reference_peaks.setdefault(construct, {}).setdefault(reference, []).append(float(main_peak))

        # Search for dbDNA dimer peak if the current reference is dbDNA
        if reference == 'dbDNA':
            dimer_candidates = peak_df.drop(index=main_peak_index)
            dimer_candidates = dimer_candidates[
                dimer_candidates['peak_center'].between(
                    main_peak * 2 * 0.9,
                    main_peak * 2 * 1.1
                    )
                ]
            if not dimer_candidates.empty:
                dimer_peak = dimer_candidates.loc[
                    dimer_candidates['peak_height'].idxmax(),
                    'peak_center'
                    ]
                reference_peaks.setdefault(construct, {}).setdefault('2x dbDNA', []).append(float(dimer_peak))

    if not reference_peaks:
        raise ValueError('No dbDNA or dsCircle reference samples found')

    return {
        construct: {
            marker: int(round(sum(positions) / len(positions)))
            for marker, positions in markers.items()
        }
        for construct, markers in reference_peaks.items()
    }


