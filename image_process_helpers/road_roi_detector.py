import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from cv2 import cv2


# img_median = cv2.imread(str(median_path), cv2.IMREAD_GRAYSCALE)
# frame_size = img_median.shape
# image = np.zeros(frame_size)

def width_and_heights_to_points(df):
    df = df.copy()[['x', 'y', 'w', 'h', 'label']]
    df.loc[:, 'x2'] = df.x + df.w
    df.loc[:, 'y2'] = df.y + df.h
    return df


def lay_rects_on_image(imgae, df, filled=True):
    img = imgae.copy()
    for i, row in df.iterrows():
        try:
            pt1 = (int(row.x), int(row.y))
            pt2 = (int(row.x2), int(row.y2))
        except ValueError:
            continue  # cannot convert float NaN to integer
        if filled:
            img = cv2.rectangle(img, pt1, pt2, 1, cv2.FILLED)
        else:
            img = cv2.rectangle(img, pt1, pt2, 1, thickness=3)
    img = img.astype(np.uint8)
    return img


def group_boundary_detections(df, field_name, quantile, edge_type):
    series = df[field_name]

    q_value = series.quantile(quantile)
    idxs = series < q_value if quantile < 0.5 else series > q_value
    selected_boxes = df[idxs]
    ret = selected_boxes.agg({'x': 'min', 'y': 'min', 'x2': 'max', 'y2': 'max'})
    ret['edge_type'] = edge_type
    return ret


def get_rois(df_detections, quantile=0.95):
    df = width_and_heights_to_points(df_detections)
    left_most = group_boundary_detections(df, 'x', 1 - quantile, 'left')  # df.loc[df.x.idxmin()]#
    top_most = group_boundary_detections(df, 'y', 1 - quantile, 'top')  # df.loc[df.y.idxmin()]
    right_most = group_boundary_detections(df, 'x', quantile, 'right')  # df.loc[df.x.idxmax()]
    bottom_most = group_boundary_detections(df, 'y', quantile, 'bottom')  # df.loc[df.y.idxmax()]

    df_extremes = pd.DataFrame([left_most,
                                top_most,
                                right_most,
                                bottom_most])

    return df_extremes


def main():
    median_path = 'C:/Users/avitu/Documents/GitHub/Traffic/experimental/median.jpg'
    path = 'C:/Users/avitu/Documents/GitHub/Traffic/experimental/detections.prqt'

    img_median = cv2.imread(str(median_path), cv2.IMREAD_GRAYSCALE)
    frame_size = img_median.shape
    image = np.zeros(frame_size)

    data_set = pq.ParquetDataset(str(path))
    pdf = data_set.read()
    df_detections = pdf.to_pandas()[['x', 'y', 'w', 'h', 'label']]

    # The ROIs
    df_extremes = get_rois(df_detections)

    img_near_edge = lay_rects_on_image(image, df_extremes)

    masked_median = cv2.bitwise_or(img_median, img_median, mask=img_near_edge)
    marked_median = lay_rects_on_image(img_median, df_extremes,
                                       filled=False)  # marked_median = plot_rects(img_median, df_edges, filled=False)

    # Show side by side
    stacked = np.hstack((masked_median, marked_median))  # stacking images side-by-side
    aspect = stacked.shape[1] / stacked.shape[0]
    # h = 8
    # w = h * aspect
    # plt.figure(figsize=(w, h))

    plt.imshow(stacked, cmap='gray', interpolation='nearest')
    plt.show(block=True)


if __name__ == '__main__':
    main()
