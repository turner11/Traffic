import numpy as np
from cv2 import cv2
import matplotlib.pyplot as plt

erosion_size = 0
max_elem = 2
max_kernel_size = 21
title_trackbar_element_type = 'Element:\n 0: Rect \n 1: Cross \n 2: Ellipse'
title_trackbar_kernel_size = 'Kernel size:\n 2n +1'
title_erosion_window = 'Erosion Demo'
title_dilatation_window = 'Dilation Demo'


def demo_erosion_dilatation(img, iterations):
    src = img / 255  # np.max(img)

    # src = 1 - src
    # src = cv2.GaussianBlur(src, (25, 25), 0)

    def erosion(val):
        erosion_size = cv2.getTrackbarPos(title_trackbar_kernel_size, title_erosion_window)
        erosion_type = 0
        val_type = cv2.getTrackbarPos(title_trackbar_element_type, title_erosion_window)
        if val_type == 0:
            erosion_type = cv2.MORPH_RECT
        elif val_type == 1:
            erosion_type = cv2.MORPH_CROSS
        elif val_type == 2:
            erosion_type = cv2.MORPH_ELLIPSE
        element = cv2.getStructuringElement(erosion_type, (2 * erosion_size + 1, 2 * erosion_size + 1),
                                            (erosion_size, erosion_size))
        erosion_dst = cv2.erode(src, element, iterations=iterations)
        cv2.imshow(title_erosion_window, erosion_dst)

    def dilatation(val):
        dilatation_size = cv2.getTrackbarPos(title_trackbar_kernel_size, title_dilatation_window)
        dilatation_type = 0
        val_type = cv2.getTrackbarPos(title_trackbar_element_type, title_dilatation_window)
        if val_type == 0:
            dilatation_type = cv2.MORPH_RECT
        elif val_type == 1:
            dilatation_type = cv2.MORPH_CROSS
        elif val_type == 2:
            dilatation_type = cv2.MORPH_ELLIPSE
        element = cv2.getStructuringElement(dilatation_type, (2 * dilatation_size + 1, 2 * dilatation_size + 1),
                                            (dilatation_size, dilatation_size))
        dilatation_dst = cv2.dilate(src, element, iterations=iterations)
        cv2.imshow(title_dilatation_window, dilatation_dst)

    cv2.namedWindow(title_erosion_window)
    cv2.createTrackbar(title_trackbar_element_type, title_erosion_window, 0, max_elem, erosion)
    cv2.createTrackbar(title_trackbar_kernel_size, title_erosion_window, 0, max_kernel_size, erosion)
    cv2.namedWindow(title_dilatation_window)
    cv2.createTrackbar(title_trackbar_element_type, title_dilatation_window, 0, max_elem, dilatation)
    cv2.createTrackbar(title_trackbar_kernel_size, title_dilatation_window, 0, max_kernel_size, dilatation)
    erosion(0)
    dilatation(0)
    cv2.waitKey()


def demo_thersholding(img, threshold=None, show=True, thresh_type=cv2.THRESH_BINARY_INV):
    plt.figure(654)

    hist, bins = np.histogram(img.ravel(), 256, [0, 256])

    threshold = threshold if threshold is not None else bins[hist.argmax()]
    # threshold = threshold if threshold is not None else np.median(img)
    # aimg = cv2.cvtColor(img/255, cv2.COLOR_BGR2GRAY)  # or convert
    equ = cv2.equalizeHist(img.astype(np.uint8))

    threshold, equ_threshed = cv2.threshold(equ, threshold, equ.max(), thresh_type)

    if show:
        # Show histogram
        cdf = hist.cumsum()
        cdf_normalized = cdf * hist.max() / cdf.max()
        plt.plot(cdf_normalized, color='b')
        plt.hist(img.flatten(), 256, [0, 256], color='r')
        plt.xlim([0, 256])
        plt.legend(('cdf', 'histogram'), loc='upper left')
        plt.show()

        # Compare images
        res = np.hstack((img, equ.astype(np.float)))  # stacking images side-by-side
        threshold, ret = cv2.threshold(res, threshold, res.max(), thresh_type)
        ret = ret / 255.
        cv2.imshow('try...', ret)
        cv2.waitKey(0)
    return equ_threshed


def main():
    median = cv2.imread(r'median.jpg', cv2.IMREAD_GRAYSCALE)
    src = median

    hist, bins = np.histogram(src.ravel(), 256, [0, 256])
    threshold = bins[hist.argmax()] * 1.1
    th = demo_thersholding(src, threshold=threshold)

    # cv2.imshow('threshed',th)

    erosion_size = 5
    erosion_type = cv2.MORPH_ELLIPSE
    element = cv2.getStructuringElement(erosion_type, (2 * erosion_size + 1, 2 * erosion_size + 1),
                                        (erosion_size, erosion_size))
    erosion_dst = cv2.erode(th, element, iterations=1)
    cv2.imshow('erosion', erosion_dst)

    dialation_dst = cv2.dilate(erosion_dst, element, iterations=2)
    cv2.imshow('dialation', dialation_dst)
    # =====================================================================
    mask = cv2.inRange(median, 0, threshold*1.3)
    result = cv2.bitwise_and(median, median, mask=mask)
    result2 = cv2.bitwise_and(median, mask, mask=mask)

    dialation_size = 2
    erosion_size = 1

    def a(img, dialation_size, erosion_size, dialation_iter=2, erosion_iter=1):
        mask = cv2.inRange(img, 0, threshold * 1.3)
        def get_element(size, type=cv2.MORPH_ELLIPSE):
            ksize = (2 * size + 1, 2 * size + 1)
            anchor = (size, size)
            element = cv2.getStructuringElement(type, ksize=ksize ,anchor=anchor)
            return element

        dialation_element, erose_element= [get_element(size) for size in [dialation_size, erosion_size]]
        dialated_mask = cv2.dilate(mask, dialation_element, iterations=dialation_iter)

        dialate_and_erosed = cv2.erode(dialated_mask, erose_element, iterations=erosion_iter)
        erosed_mask = cv2.erode(mask, erose_element, iterations=erosion_iter)

        items = [img,
                 mask,
                 # result,
                 # result2,
                 dialated_mask,
                 dialate_and_erosed,
                 # erosed_mask,
                 ]
        cols = 2
        rows = (len(items)+1) // cols
        plt.subplot(rows, cols, 1)
        for i, img in enumerate(items, start=1):
            plt.subplot(rows, cols, i)
            plt.imshow(img, cmap="gray")
        plt.show()

    a(median, dialation_size=2, erosion_size=2, dialation_iter=2, erosion_iter=4)
    blure_size = 45
    blured = cv2.GaussianBlur(median, (blure_size , blure_size), 0)
    a(blured, dialation_size=2, erosion_size=2, dialation_iter=2, erosion_iter=4)
    blure_size = 7
    blured = cv2.medianBlur(median, blure_size)
    a(blured, dialation_size=3, erosion_size=2, dialation_iter=2, erosion_iter=4)

    cv2.waitKey(0)
    str(th)


if __name__ == '__main__':
    main()
