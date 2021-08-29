import matplotlib.pyplot as plt
import numpy as np
import csv

from CSIKit.util.csitools import get_CSI
from CSIKit.util.filters import bandpass, hampel, running_mean
from CSIKit.reader import get_reader

# DEFAULT_PATH = "../results/room_10_20210803-094215/output_0_20210803-094215/output.pcap"
DEFAULT_PATH = "output.pcap"


if __name__ == "__main__":
    path: str=DEFAULT_PATH
    reader = get_reader(path)
    csi_data = reader.read_file(path)
    print (len(csi_data.frames))
    finalEntry, no_frames, no_subcarriers = get_CSI(csi_data, squeeze_output=True)
    print(len(finalEntry[0]))
    total_length = finalEntry.size
    print(total_length)
    print (len(csi_data.timestamps))
    # print (csi_data.timestamps)
    print (finalEntry)
    print (finalEntry[5])


    with open('pcapdata.csv', 'w') as csvfile:
        fieldnames = ['Timestamp', 'finalEntry']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in csi_data.timestamps:
            timer = i - csi_data.timestamps[0]
            #1627975155.109669-1627972936.190185                #!!!
            writer.writerow({'Timestamp': timer})

        for j ,frame in enumerate(finalEntry):
            # print(finalEntry[j])
            writer.writerow({'finalEntry': finalEntry[j]})




# class BatchGraph:

#     def __init__(self, path: str = DEFAULT_PATH):
#         reader = get_reader(path)
#         self.csi_data = reader.read_file(path)

#         self.full_path = path

#     def prepostfilter(self):

#         csi_trace = self.csi_data.frames

#         finalEntry, no_frames, _ = get_CSI(self.csi_data)

#         if len(finalEntry.shape) == 4:
#             # >1 antenna stream.
#             # Loading the first for ease.
#             finalEntry = finalEntry[:, :, 0, 0]
#         finalEntry = np.transpose(finalEntry)

#         finalEntry = finalEntry[10]

#         hampelData = hampel(finalEntry, 10)
#         smoothedData = running_mean(hampelData.copy(), 10)

#         y = finalEntry
#         y2 = hampelData
#         y3 = smoothedData

#         x = list([x.timestamp for x in csi_trace])

#         if sum(x) == 0:
#             x = np.arange(0, no_frames, 1)

#         plt.plot(x, y, label="Raw")
#         plt.plot(x, y2, label="Hampel")
#         plt.plot(x, y3, "r", label="Hampel + Running Mean")

#         plt.xlabel("Time (s)")
#         plt.ylabel("Amplitude (dBm)")
#         plt.legend(loc="upper right")

#         plt.show()

#     def plotAllSubcarriers(self):

#         finalEntry, no_frames, _ = get_CSI(self.csi_data)
#         if len(finalEntry.shape) == 4:
#             # >1 antenna stream.
#             # Loading the first for ease.
#             finalEntry = finalEntry[:, :, 0, 0]
#         finalEntry = np.transpose(finalEntry)

#         for x in finalEntry:
#             plt.plot(np.arange(no_frames) / 20, x)

#         plt.xlabel("Time (s)")
#         plt.ylabel("Amplitude (dBm)")
#         plt.legend(loc="upper right")

#         plt.show()

#     def heatmap(self, metric='amplitude', plot_show=True, axs=None, plt_row=None, plt_col=None):

#         csi_trace = self.csi_data.frames
#         finalEntry, no_frames, no_subcarriers = get_CSI(self.csi_data, metric=metric, squeeze_output=True)

#         if len(finalEntry.shape) == 4:
#             # >1 antenna stream.
#             # Loading the first for ease.
#             finalEntry = finalEntry[:, :, 0, 0]

#         # from CSIKit.filters.wavelets.dwt import denoise
#         # finalEntry = denoise(finalEntry)

#         # Transpose to get subcarriers * amplitude.
#         finalEntry = np.transpose(finalEntry)
#         #finalEntry[finalEntry == 0] = -np.inf
#         #finalEntry = np.diff(np.diff(finalEntry, axis=0), axis=1)
#         if np.any(np.iscomplex(finalEntry)):
#             print('Complex Values, Reducing to abs values')
#             finalEntry = np.abs(finalEntry)
#         x_label = "Time (s)"
#         try:
#             x = self.csi_data.timestamps

#             x = [timestamp - x[0] for timestamp in x]
#             #1627975155.109669-1627972936.190185                #!!!
#             print(x[0])  # len of x
#             print("len of x: ", len(x))  # represent the time in ms
#             print("last value: ", x[len(x)-1])  # represent the time in ms

#         except AttributeError as e:
#             # No timestamp in frame. Likely an IWL entry.
#             # Will be moving timestamps to CSIData to account for this.
#             x = [0]

#         if sum(x) == 0:
#             # Some files have invalid timestamp_low values which means we can't plot based on timestamps.
#             # Instead we'll just plot by frame count.

#             xlim = no_frames

#             x_label = "Frame No."
#         else:
#             xlim = max(x)

#         limits = [0, xlim, 1, no_subcarriers]
#         # limits = [0, xlim, -64, 63]

#         # TODO Add options for filtering.
#         # for x in range(no_subcarriers):
#         #     hampelData = hampel(finalEntry[x], 5, 3)
#         #     runningMeanData = running_mean(hampelData, 20)
#         #     # smoothedData = dynamic_detrend(runningMeanData, 5, 3, 1.2, 10)
#         #     # doubleHampel = hampel(smoothedData, 10, 3)

#         #     finalEntry[x] = bandpass(9, 1, 2, Fs, runningMeanData)
#         #     # for i in range(0, 140):
#         #     #     finalEntry[x][i] = 0

#         if axs is not None:
#             ax = axs[plt_row, plt_col]
#         else:
#             _, ax = plt.subplots()

#         im = ax.imshow(finalEntry, cmap="jet", extent=limits, aspect="auto")

#         cbar = ax.figure.colorbar(im, ax=ax)
#         if metric == 'amplitude':
#             cbar.ax.set_ylabel("Amplitude (dBm)")
#         elif metric == 'phase':
#             cbar.ax.set_ylabel("Phase (Rad)")

#         ax.set_xlabel(x_label)
#         ax.set_ylabel("Subcarrier Index")
#         ax.set_title(str(plt_col))

#         #plt.xlabel(x_label)
#         #plt.ylabel("Subcarrier Index")
#         #plt.title(self.full_path.replace('/', '_').replace('results', '').replace('output', '') + ' ' + metric)

#         if plot_show:
#             plt.show()


# if __name__ == "__main__":
#     bg = BatchGraph()
#     bg.heatmap()