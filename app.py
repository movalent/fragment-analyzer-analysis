# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths
from scipy.integrate import simpson
from pathlib import Path

# Load data
file_name = r'Data/2026 03 04 15H 52M Electropherogram.csv'
file_path = Path.cwd() / file_name
df = pd.read_csv(file_path)

sample_names = list(df.columns[1:])

print('=================== Traces ===================\n')
for index, sample in enumerate(sample_names):
    print(f'{index}: {sample}')
    
print()

sample = int(input('=================== Select the sample: ===================\n'))
print()
sample = sample_names[sample]

df_filtered = df[['Size (bp)', sample]]
# Remove the lower and upper marker
df_filtered = df_filtered[(df_filtered['Size (bp)'] > 90) & (df_filtered['Size (bp)'] < 19100)]

# Find peaks
peaks, properties = find_peaks(df_filtered[sample],
                               height=20, 
                               prominence=5)


df_peaks = df_filtered.iloc[peaks]

print(df_peaks)

print('=================== Peaks properties ===================\n')
for key, value in properties.items():
    print(key, value)

# Peak area
peak_width_results = peak_widths(df_filtered[sample], peaks, rel_height=0.99)
widths = peak_width_results[0]
peak_start = peak_width_results[2]
peak_end = peak_width_results[3]
print(peak_width_results)


fig, ax = plt.subplots()

ax.plot(df_filtered['Size (bp)'], df_filtered[sample], color='black', lw=1)
ax.scatter(df_peaks['Size (bp)'], df_peaks[sample], color='red')


# integration
areas = []
for i in range(len(peaks)):
    start_idx = int(peak_start[i])
    end_idx = int(peak_end[i])
    
    peak_area = int(simpson(df_filtered[sample].iloc[start_idx:end_idx]))
    
    areas.append(peak_area)
    
    ax.fill_between(df_filtered['Size (bp)'].iloc[start_idx:end_idx],
                   df_filtered[sample].iloc[start_idx:end_idx],
                   alpha=0.3
                   )
    
print('=================== Areas ===================\n')
print(areas)

sum_areas = sum(areas)

area_perc = [round(x/sum_areas*100, 2) for x in areas]
print(area_perc)

# When you document this project, mention that you chose Simpson's Rule specifically for higher integration accuracy on curvilinear signal data. This shows you aren't just copy-pasting code, but thinking about the underlying mathematics of the analytical chemistry you are automating.


# ax.set_xlim(xmin=0, xmax=20000)
ax.set_ylim(ymin=0, ymax = 3000)
# ax.set_xscale('log')
# ax.set_yscale('log')



plt.show()