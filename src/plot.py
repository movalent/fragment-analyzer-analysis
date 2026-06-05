# fig, ax = plt.subplots()

# ax.plot(df_raw['Size (bp)'], df_raw[sample], color='black', lw=1)
# ax.scatter(peaks_df['peak_center'], peaks_df['peak_height'], color='red')


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


# ax.set_xlim(xmin=-500, xmax=23000)
# ax.set_ylim(ymin=0, ymax = np.max(peaks_df[peaks_df['peak_center'] == 75]['peak_height']))
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
