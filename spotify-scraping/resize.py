import matplotlib
import os
from os import listdir
import matplotlib.pyplot as plt
import skimage.color
from skimage import io, color
from skimage.transform import rescale, resize
from skimage.util import img_as_ubyte
from timeit import default_timer as timer
import numpy as np


input_dir = "insert input directory here"
output_dir = "insert output directory here"

imagesProcessed = 0
start = timer()

image_list = sorted(os.listdir(input_dir))

resume_index = 13575

for image_name in image_list:

    if imagesProcessed == 0 or imagesProcessed <= resume_index:
        imagesProcessed += 1
        continue

    img_dir = input_dir + "/" + image_name
    image = io.imread(img_dir)
    image = resize(image, (512, 512))

    # convert to RGB if grayscale
    if image.ndim == 2:
        image = skimage.color.gray2rgb(image)

    image = img_as_ubyte(image)
    io.imsave(output_dir+"/"+image_name+".png", image)
    imagesProcessed += 1
    if imagesProcessed % 100 == 0:
        print("Num images processed = " + str(imagesProcessed))
        end = timer()
        time = end - start
        print("timer: " + str(time))
        start = end




