import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage.util import random_noise
from skimage import feature
import skimage.io
import json

from isbntools.app import *

query = ('Za troso Lsino + >= ₁ √ = = = [√²) 2mw a= би била Gregory Zuckerman n O THE MAN WHO SOLVED THE MARKET HOW JIM SIMONS LAUNCHED THE QUANT REVOLUTION 1 ħ? 2m it (Fil at 4= d 1/1/at = at = F + √₂14₂ >= 18(1 1 {"(!) > € {{ (2, 4) = S < | دے BUSINESS')
isbn = isbn_from_words(query)

print("The ISBN of the most `spoken-about` book with this title is %s" % isbn)
print("")
print("... and the book is:")
print("")
json_obj = registry.bibformatters['json'](meta(isbn))
json_object = json.loads(json_obj)
print(json_object['title'])
print(json_object['author'][0]['name'])