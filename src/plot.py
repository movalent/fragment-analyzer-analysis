import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simpson

def plot_trace(df_input: pd.DataFrame, peaks: pd.DataFrame, sample: str) -> None:

    df_signal = df_input.copy()
    df_peaks = peaks.copy()
    # print('=================== Data ===================\n', df_signal)
    # print('=================== Peaks ===================\n', df_peaks)

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
    ax.set_xlim(xmin=-10, xmax=23000)
    ax.set_ylim(ymin=0, ymax = np.max(df_peaks[peaks['peak_center'] == 75]['peak_height']) + 100)

    plt.xticks(rotation=90)
    plt.show()

    # Calcualte % area
    sum_areas = sum(areas)
    area_perc = [round(x/sum_areas*100, 2) for x in areas]
    print(area_perc)

# peaks_main = pd.DataFrame({
#     'peak_id': df_peaks.index,
#     'start': df_filtered.iloc[properties['left_bases']]['Size (bp)'].values,
#     'center': df_peaks['Size (bp)'],
#     'end': df_filtered.iloc[properties['right_bases']]['Size (bp)'].values
#     })

# peaks_main = pd.DataFrame({
#     'start': start_bp,
#     'center': center_bp,
#     'end': end_bp
#     })

# # peaks_main = peaks_main.astype({
# #     "start": float,
# #     "end": float,
# #     "center": float
# # })

# # editor = PeakEditor(df_filtered['Size (bp)'], df_filtered[sample], peaks_main)
# # editor.show()
