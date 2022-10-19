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
from google.cloud import vision
from numpy import asarray

def get_cropped_images(image, points):
    '''
    Takes a spine line drawn image and
    returns a list of opencv images splitted
    from the drawn lines
    '''
    image = image.copy()
    #print(image)
    #print('*****')
    y_max, _, _ = image.shape
    last_x1 = 0
    last_x2 = 0
    y1 = 0
    y2 = y_max
    cropped_images = []

    for point in points:
        (x1,x2) = point
        x1 = int(x1)
        x2 = int(x2)

        crop_points = np.array([[last_x1, 0],
                                [last_x2,y_max],
                                [x2, y2],
                                [x1, y1]])
        #print(crop_points)

        # Crop the bounding rect
        rect = cv2.boundingRect(crop_points)
        x, y, w, h = rect
        cropped = image[y: y + h, x: x + w].copy()

        # make mask
        crop_points = crop_points - crop_points.min(axis=0)
        mask = np.zeros(cropped.shape[:2], np.uint8)
        cv2.drawContours(mask, [crop_points], -1, (255, 255, 255), -1, cv2.LINE_AA)

        # do bit-op
        dst = cv2.bitwise_and(cropped, cropped, mask=mask)
        cropped_images.append(dst)

        last_x1 = x1
        last_x2 = x2

    return cropped_images

def detect_document(path):
    """Detects document features in an image."""
    from google.cloud import vision
    import io
    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_file("key/service_key.json")
    client = vision.ImageAnnotatorClient(credentials=credentials)



    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = str(response.full_text_annotation.text)
    texts = texts.replace('\n',' ')
    

    # for text in texts:
    #     print('\n"{}"'.format(text.description))

    #     vertices = (['({},{})'.format(vertex.x, vertex.y)
    #                 for vertex in text.bounding_poly.vertices])

    #     print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return texts