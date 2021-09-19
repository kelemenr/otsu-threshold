import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import sys


def otsu(gray):
    n = 256
    hist, bin_edges = np.histogram(gray, bins=n)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0

    w1 = np.cumsum(hist)
    w2 = np.cumsum(hist[::-1])[::-1]

    mu1 = np.cumsum(hist * bin_centers) / w1
    mu2 = (np.cumsum((hist * bin_centers)[::-1]) / w2[::-1])[::-1]

    sigma_total = w1[:-1] * w2[1:] * (mu1[:-1] - mu2[1:]) ** 2

    max_val_index = np.argmax(sigma_total)
    t = bin_centers[:-1][max_val_index]

    return t


def main():
    try:
        path = sys.argv[1]
    except:
        raise SystemExit(f"Usage: {sys.argv[0]} <image_path>")

    file_name = os.path.basename(path)
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    threshold = otsu(image)
    print('The threshold for ', file_name, ' is: ', threshold)

    mask = image > threshold
    final_image = np.zeros(image.shape)
    final_image[mask] = 255

    final_image = final_image.astype(np.uint8)
    cv2.imwrite('output/thresholded_' + file_name, final_image)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_figheight(5)
    fig.set_figwidth(10)

    ax1.imshow(image, cmap='gray')
    ax1.set_title('Original Image', fontsize=16)

    ax2.imshow(final_image, cmap='gray')
    ax2.set_title('Otsu Thresholded Image', fontsize=16)
    plt.show()


if __name__ == "__main__":
    main()
