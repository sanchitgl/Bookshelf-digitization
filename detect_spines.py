import numpy as np
from skimage.transform import hough_line, hough_line_peaks
from skimage.feature import canny
from skimage.draw import line
from skimage import data
import skimage.io
import matplotlib.pyplot as plt
from matplotlib import cm
import cv2
from PIL import Image
from io import BytesIO
from scipy import ndimage as ndi
from skimage.util import random_noise
from skimage import feature



def spine_detect(img_path):
    og_image = skimage.io.imread(fname=img_path)
    image = skimage.io.imread(fname=img_path, as_gray=True)
    #skimage.io.imshow(image)

    #image = skimage.io.imread(fname=img_path,  as_gray=True)
    image = ndi.gaussian_filter(image, 2)
    #image = random_noise(image, mode='speckle', mean=0.1)

    # Compute the Canny filter for two values of sigma
    edges = feature.canny(image,sigma =1.5,low_threshold=0.03, high_threshold=0.06)

    # display results
    # fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(8, 3))

    # ax[0].imshow(image, cmap='gray')
    # ax[0].set_title('noisy image', fontsize=20)

    # ax[1].imshow(edges, cmap='gray')
    # ax[1].set_title(r'Canny filter, $\sigma=1$', fontsize=20)

    # ax[2].imshow(edges2, cmap='gray')
    # ax[2].set_title(r'Canny filter, $\sigma=3$', fontsize=20)

    # for a in ax:
    #     a.axis('off')

    # Classic straight-line Hough transform
    # Set a precision of 0.5 degree.
    tested_angles = np.linspace(-np.pi/18, np.pi/18, 180, endpoint=False)
    h, theta, d = hough_line(edges, theta=tested_angles)

    # Generating figure 1
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    ax = axes.ravel()

    ax[0].imshow(edges, cmap=cm.gray)
    ax[0].set_title('Input image')
    ax[0].set_axis_off()

    angle_step = 0.5 * np.diff(theta).mean()
    d_step = 0.5 * np.diff(d).mean()
    bounds = [np.rad2deg(theta[0] - angle_step),
            np.rad2deg(theta[-1] + angle_step),
            d[-1] + d_step, d[0] - d_step]
    # ax[1].imshow(np.log(1 + h), extent=bounds, cmap=cm.gray, aspect=1 / 1.5)
    # ax[1].set_title('Hough transform')
    # ax[1].set_xlabel('Angles (degrees)')
    # ax[1].set_ylabel('Distance (pixels)')
    # ax[1].axis('image')

    ax[1].imshow(og_image)
    ax[1].set_ylim((image.shape[0], 0))
    ax[1].set_axis_off()
    #ax[1].set_title('Detected lines')

    points = []
    for _, angle, dist in zip(*hough_line_peaks(h, theta, d, min_distance = int(image.shape[1]/30))):
        (x0, y0) = dist * np.array([np.cos(angle), np.sin(angle)])
        #print(x0)
        #print(y0)
        x1 = x0+(image.shape[0]/(np.tan(angle + np.pi/2)))
        #print(x1)
        #print('######')
        point = (x0,x1)
        points.append(point)

        #im = im.crop( (0, 0, 360, 222) ) # previously, image was 826 pixels wide, cropping to 825 pixels wide
        #im.save('card.png') # saves the image
        #y1 = (np.tan(angle + np.pi/2))*x1 + y0
        #cv2.line(og_image,(x0,y0),(x1,y1),(0,0,255),2)
        ax[1].axline((x0, y0), slope=np.tan(angle + np.pi/2), lw = 3.0)
    #     ax[2].plot((0, image.shape[1]), (y0, y1), '-r')
    # ax[2].set_xlim((0, image.shape[1]))
    # ax[2].set_ylim((image.shape[0], 0))
    # ax[2].set_axis_off()
    # ax[2].set_title('Detected lines')
    extent = ax[1].get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig('images_run/houghline.png', bbox_inches=extent)
    extent_2 = ax[0].get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig('images_run/canny_edge.png', bbox_inches=extent_2)
    #plt.tight_layout()
    #cv2.imwrite('houghlines3.jpg',img)
    #plt.show()
    last_point = (image.shape[1],image.shape[1])
    points.append(last_point)
    points.sort(key=lambda y: y[0])
    return og_image, points


#spine_detect('books.jpg')
# spine_detect('books_2.jpg')
# spine_detect('img.jpeg')
# spine_detect('spines.jpg')