import tensorflow as tf
import keras
import numpy as np
from os.path import join

from PIL import Image
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

# from util import cocoTrain, cocoVal
# Common pathnames
from util import train_img_dir_wrapper, val_img_dir_wrapper, \
                 train_mask_dir_wrapper, val_mask_dir_wrapper

from keras.preprocessing.image import ImageDataGenerator

tmp = "../tmp"

def test_img_and_mask_datagen():
    datagen_args = dict(
        rotation_range = 20,
        width_shift_range = 0.1,
        height_shift_range = 0.1,
        zoom_range = 0.1,
        horizontal_flip = True
    )

    image_datagen = ImageDataGenerator(**datagen_args)
    mask_datagen  = ImageDataGenerator(**datagen_args)

    seed = 191
    # Also use a batch_size = 128 in real code. shuffle=True by default
    val_image_generator = image_datagen.flow_from_directory(
        val_img_dir_wrapper,
        #"../data/person_wrapper",
        class_mode=None,
        seed=seed,
        shuffle=True,
        batch_size=128,
        color_mode='rgb',
        target_size=(224,224))
    val_mask_generator  = mask_datagen.flow_from_directory(
        val_mask_dir_wrapper,
        #"../data/mask_wrapper",
        class_mode=None,
        seed=seed,
        shuffle=True,
        batch_size=128,
        color_mode = 'grayscale',
        target_size = (224,224))

    # This will yield (x images, y mask labels) upon iteration
    val_generator = zip(val_image_generator, val_mask_generator)

    print("val_generator is: %s" % str(val_generator))

    for x, y in val_generator:
        print("Info about x:")
        print(x.shape)

        print("Info about y:")
        print(y.shape)
        
        print("Taking some out of this batch, and storing their images.")
        arbitrary_nums  = [120]
        for arbitrary in arbitrary_nums:
            x_arr = x[arbitrary]
            y_arr = y[arbitrary][:,:,0] # remove the last dim
            

            # casting to uint8 is necessary for displaying photos.
            # For the machine learning, don't need to do anything.
            x_arr_int = x_arr.astype(np.uint8)
            y_arr_int = y_arr.astype(np.uint8)
            xdiff = np.sum(x_arr - x_arr_int)
            ydiff = np.sum(y_arr - y_arr_int)
            print("xdiff: %f, ydiff: %f" % (xdiff, ydiff))
            #x_img = Image.fromarray(x, mode='RGB')
            #y_img = Image.fromarray(np.uint8(y * 255), mode='L')
            difference_array = x_arr - x_arr_int
            np.save(join(tmp, "diff.npy"), difference_array)

            print("Saving the image and mask in ../tmp.")
            #x_img.save(join(tmp, "dataflow_x.png"), 'PNG')
            #y_img.save(join(tmp, 'dataflow_y.png'), 'PNG')
            plt.imshow(x_arr)
            plt.savefig(join(tmp, "dataflow_%d_x.png" % arbitrary))
            plt.imshow(y_arr)
            plt.savefig(join(tmp, "dataflow_%d_y.png" % arbitrary))
            plt.imshow(x_arr_int)
            plt.savefig(join(tmp, "dataflow_%d_x_INT.png" % arbitrary))
            plt.imshow(y_arr_int)
            plt.savefig(join(tmp, "dataflow_%d_y_INT.png" % arbitrary))
        break

if __name__ == "__main__":
    test_img_and_mask_datagen()


