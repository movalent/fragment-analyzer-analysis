# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths
from scipy.integrate import simpson
from pathlib import Path

from peak_adjustment import PeakEditor


def load_data():
    file_name = r'../../input/2026 03 04 15H 52M Electropherogram.csv'
    file_path = Path.cwd() / file_name
    return pd.read_csv(file_path)


def select_sample(df):
    sample_names = list(df.columns[1:])
    
    print('=================== Traces ===================\n')
    for index, sample in enumerate(sample_names, start=1):
        print(f'{index}: {sample}')
        
    print()
    print('Select the sample: ')
    
    sample_idx = int(input('> ')) - 1
    return sample_names[sample_idx]


def find_peaks_(df, sample):
    peaks, properties = find_peaks(df[sample],
                                   height=20, 
                                   prominence=10
                                   )
        
    peak_df = pd.DataFrame(
        {'peak_index':  peaks,
        'peak_height':  df[sample].iloc[peaks],
        'peak_start':   df['Size (bp)'].iloc[properties['left_bases']].values,
        'peak_center':  df['Size (bp)'].iloc[peaks],
        'peak_end':     df['Size (bp)'].iloc[properties['right_bases']].values
        })
        
    return peak_df, properties
    
def find_valleys(df_input, df_peaks, sample):
    valleys = []
    peaks_idx = df_peaks['peak_index'].values

    for i in range(len(peaks_idx) - 1):
        left = peaks_idx[i]
        right = peaks_idx[i + 1]
        
        # Find valley in original signal
        segment = df_input[sample].iloc[left:right].values        
        valley_relative = np.argmin(segment)
        
        valley_index = left + valley_relative
        
        valleys.append(valley_index)
        
    valleys = np.array(valleys)

    # Define new peak boundaries
    starts = np.concatenate(([0], valleys))
    ends = np.concatenate((valleys, [len(df_input) - 1]))
    
    result = pd.DataFrame({
        'peak_index':       df_peaks['peak_index'].values,
        'peak_height':      df_peaks['peak_height'].values,
        'peak_start_corr':  df_input['Size (bp)'].iloc[starts].values,
        'peak_center_corr': df_input['Size (bp)'].iloc[peaks_idx].values,
        'peak_end_corr':    df_input['Size (bp)'].iloc[ends].values
        })
    
    return result, valleys
    

  
df_raw = load_data()
sample = select_sample(df_raw)

peaks_df, properties = find_peaks_(df_raw, sample)

print(peaks_df)

peaks_df_corr, valleys = find_valleys(df_raw, peaks_df, sample)

print(peaks_df_corr)

# df_peaks = df_filtered.iloc[peaks]


# print('=================== Peaks properties ===================\n')
# for key, value in properties.items():
#     print(key, value)

# # Peak area
# peak_width_results = peak_widths(df_filtered[sample], peaks, rel_height=0.99)
# widths = peak_width_results[0]
# peak_start = peak_width_results[2]
# peak_end = peak_width_results[3]

# fig, ax = plt.subplots()

# ax.plot(df_filtered['Size (bp)'], df_filtered[sample], color='black', lw=1)
# ax.scatter(df_peaks['Size (bp)'], df_peaks[sample], color='red')


# # integration
# areas = []
# for i in range(len(peaks)):
#     start_idx = int(peak_start[i])
#     end_idx = int(peak_end[i])
    
#     peak_area = int(simpson(df_filtered[sample].iloc[start_idx:end_idx]))
    
#     areas.append(peak_area)
    
#     ax.fill_between(df_filtered['Size (bp)'].iloc[start_idx:end_idx],
#                    df_filtered[sample].iloc[start_idx:end_idx],
#                    alpha=0.3
#                    )
    
# # print('=================== Areas ===================\n')
# # print(areas)

# # sum_areas = sum(areas)

# # area_perc = [round(x/sum_areas*100, 2) for x in areas]
# # print(area_perc)

# # # When you document this project, mention that you chose Simpson's Rule specifically for higher integration accuracy on curvilinear signal data. This shows you aren't just copy-pasting code, but thinking about the underlying mathematics of the analytical chemistry you are automating.


# ax.set_xlim(xmin=0, xmax=20000)
# ax.set_ylim(ymin=0, ymax = 1500)
# # ax.set_xscale('log')
# # ax.set_yscale('log')

# plt.xticks(rotation=90)

# peaks_main = pd.DataFrame({
#     'peak_id': df_peaks.index,
#     'start': df_filtered.iloc[properties['left_bases']]['Size (bp)'].values,
#     'center': df_peaks['Size (bp)'],
#     'end': df_filtered.iloc[properties['right_bases']]['Size (bp)'].values
#     })

# # print(peaks_main)

# peaks_main = pd.DataFrame({
#     'start': start_bp,
#     'center': center_bp,
#     'end': end_bp
#     })

# # print(peaks_main)

# # peaks_main = peaks_main.astype({
# #     "start": float,
# #     "end": float,
# #     "center": float
# # })

# # editor = PeakEditor(df_filtered['Size (bp)'], df_filtered[sample], peaks_main)
# # editor.show()


# plt.show()

