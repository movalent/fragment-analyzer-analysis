import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simpson
from matplotlib.widgets import RectangleSelector, Button
import re

import peaks

def plot_trace(df_input: pd.DataFrame, peaks: pd.DataFrame, sample: str) -> None:
    """
    Plot a sample trace with detected peaks and their integration regions.


    The function visualises the raw signal, marks peak maxima, and shades
    regions corresponding to peak boundaries.

    Args:
        df_input (pd.DataFrame): DataFrame containing the raw traces data.
        peaks (pd.DataFrame): DataFrame containing the peak information.
        sample (str): Name of the sample column to plot.

    Returns:
        None
    """

    df_signal = df_input.copy()
    df_peaks = peaks.copy()


    fig, ax = plt.subplots()

    # Visualize detected peaks maximas
    ax.scatter(df_peaks['peak_center'], df_peaks['peak_height'], color='red')

    # Visualize traces
    ax.plot(df_signal['Size (bp)'], df_signal[sample], color='black', lw=1)

    # Color the graph by detected peak boundaries
    areas = []
    for idx, row in df_peaks.iterrows():
        start_idx = float(row['peak_start'])
        end_idx = float(row['peak_end'])

        x_range = df_signal[df_signal['Size (bp)'].between(start_idx, end_idx)]['Size (bp)']
        y_range = df_signal[df_signal['Size (bp)'].between(start_idx, end_idx)][sample]

        ax.fill_between(
            x_range,
            y_range,
            alpha=0.3
            )

        peak_area = int(simpson(y=list(y_range)))  # Truncating decimals are insignificant overally
        areas.append(peak_area)

    # Set the trace boundaries
    ax.set_xlim(xmin=-10, xmax=5000)
    ax.set_ylim(ymin=0, ymax = np.max(df_peaks[peaks['peak_center'] == 75]['peak_height']) + 100)

    plt.xticks(rotation=90)
    plt.show()

    # Calcualte % area
    sum_areas = sum(areas)
    area_perc = [round(x/sum_areas*100, 2) for x in areas]

    print(area_perc)

def interactive_peak_boundary_adjustment(
        df_input: pd.DataFrame,
        df_peaks: pd.DataFrame,
        sample: str,
        ref_points: dict[str, dict[str, int]] | None = None
        ) -> pd.DataFrame:

    """
    Interactively adjust peak boundaries for a selected trace.
    - click inside peak boundary activates it, clicking and dragging moves the boundary
    - click outside peak boundary triggers rectangular zooming
    - right click 
    - pressing `a` accepts the changes and closes the editor
    - pressing `d` deletes active peak

    Args:
        df_input (pd.DataFrame): DataFrame containing the raw traces data.
        df_peaks (pd.DataFrame): DataFrame containing the peaks location information.
        sample (str): Name of the sample column to plot.
        ref_points (dict[str, dict[str, int]] | None): Optional reference points for dbDNA and dsCircle.
        
    Returns:
        pd.DataFrame: Updated DataFrame with adjusted peak boundaries.
    """

    LOW_MARKER_BOUNDARY = 80
    HIGH_MARKER_BOUNDARY = 19500

    # Zoom control buttons
    def zoom_to_5kb(event=None) -> None:
        ax.set_xlim(0, 5000)
        fig.canvas.draw_idle()

    def reset_zoom(event=None) -> None:
        ax.set_xlim(initial_xlim)
        ax.set_ylim(initial_ylim)
        fig.canvas.draw_idle()

    def zoom_with_scroll(event) -> None:
        if event.inaxes is not ax or event.xdata is None or event.ydata is None:
            return

        scale = 0.8 if event.button == 'up' else 1.25
        current_xlim = ax.get_xlim()
        current_ylim = ax.get_ylim()

        x_left = event.xdata - (event.xdata - current_xlim[0]) * scale
        x_right = event.xdata + (current_xlim[1] - event.xdata) * scale
        y_bottom = event.ydata - (event.ydata - current_ylim[0]) * scale
        y_top = event.ydata + (current_ylim[1] - event.ydata) * scale

        ax.set_xlim(x_left, x_right)
        ax.set_ylim(y_bottom, y_top)
        fig.canvas.draw_idle()

    df_signal = df_input.copy()
    adjusted_peaks = df_peaks.copy().reset_index(drop=True)

    adjusted_peaks['peak_start'] = adjusted_peaks['peak_start'].astype(float)
    adjusted_peaks['peak_end'] = adjusted_peaks['peak_end'].astype(float)

    x_values = df_signal['Size (bp)'].astype(float)
    y_values = df_signal[sample].astype(float)

    fig, ax = plt.subplots()

    fig.subplots_adjust(bottom=0.16) # Place for buttons

    ax.plot(x_values, y_values, color='black', lw=1)
    ax.set_xlabel('Size (bp)')
    ax.set_ylabel('Signal intensity')

    peaks_no_markers_mask = (
        (adjusted_peaks['peak_center'] > LOW_MARKER_BOUNDARY) &
        (adjusted_peaks['peak_center'] <= HIGH_MARKER_BOUNDARY)
        )
    peaks_no_markers = adjusted_peaks[peaks_no_markers_mask]

    # Visual aid for detected peaks
    ax.scatter(
        peaks_no_markers['peak_center'],
        peaks_no_markers['peak_height'],
        color='black',
        zorder=3
        )

    ax.set_xlim(0, HIGH_MARKER_BOUNDARY + 1000)
    ax.set_ylim(0, 10000)

    initial_xlim = ax.get_xlim()  # Default values for reset button
    initial_ylim = ax.get_ylim()

    if ref_points is not None:
        sample_match = re.match(r'^[^:]+:\s+(?P<construct>\d{3}-\d{3})\s+', sample)

        if sample_match is not None:
            construct = sample_match.group('construct').strip()

            if construct in ref_points:                

                # TODO: refactor reference names, so they are not hard coded in plot.py and peaks.py
                line_settings = {
                    'dbDNA': {'color': 'red', 'linestyle': '--'},
                    '2x dbDNA': {'color': 'darkred', 'linestyle': '--'},
                    'T5': {'color': 'blue', 'linestyle': '--'}
                }

                for marker, settings in line_settings.items():
                    if marker not in ref_points[construct]:
                        continue

                    position = ref_points[construct][marker]

                    ax.axvline(
                        position,
                        color=settings['color'],
                        ls=settings['linestyle'],
                        alpha=0.3
                    )

                    ax.annotate(
                        marker,
                        xy=(position, 0.98),
                        xycoords=('data', 'axes fraction'),
                        xytext=(2, 0),
                        textcoords='offset points',
                        color=settings['color'],
                        ha='left',
                        va='top'
                        )

    # Button positioning
    reset_axis = fig.add_axes([0.42, 0.03, 0.13, 0.06])
    zoom_axis = fig.add_axes([0.56, 0.03, 0.13, 0.06])

    # Butoon creation
    reset_button = Button(reset_axis, 'Reset zoom')
    zoom_button = Button(zoom_axis, '5kb zoom')

    # Button actions
    reset_button.on_clicked(reset_zoom)
    zoom_button.on_clicked(zoom_to_5kb)

    fig.canvas.mpl_connect('scroll_event', zoom_with_scroll)

    table_content = []
    for row_no, (_, row) in enumerate(adjusted_peaks.iterrows()):

        table_content.append(
            [
                str(row_no + 1),
                f'{round(row['peak_center'], 0)}',
                row['peak_percentage']
            ]
            )

    if table_content:
        ax.table(
            cellText=table_content,
            colLabels=['Peak', 'Size (bp)', 'Area (%)'],
            cellLoc='center',
            loc='upper right',
            bbox=[0.72, 0.72, 0.28, 0.28],

        )

    # redraw()

    plt.show()





