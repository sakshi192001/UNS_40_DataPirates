from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers, callbacks
import warnings
import pickle
warnings.filterwarnings("ignore")

IMAGE_SIZE = [224, 224]

train_path = '/content/drive/MyDrive/Unscript/diag-train'
valid_path = '/content/drive/MyDrive/Unscript/diag-test'

vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

for layer in vgg.layers:
    layer.trainable = False

folders = glob('/content/drive/MyDrive/Unscript/diag-train/*')

x = Flatten()(vgg.output)
prediction = Dense(7, activation='softmax')(x)

model = Model(inputs=vgg.input, outputs=prediction)
model.summary()

model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('/content/drive/MyDrive/Unscript/diag-train',
                                                 target_size = (224, 224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory('/content/drive/MyDrive/Unscript/diag-test',
                                            target_size = (224, 224),
                                            batch_size = 32,
                                            class_mode = 'categorical')                                                 

from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
r = model.fit_generator(
  training_set,
  validation_data=test_set,
  epochs=10,
  #callbacks=[early_stopping],
  steps_per_epoch=len(training_set),
  validation_steps=len(test_set)
)

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
image1 = load_img('/content/drive/MyDrive/Unscript/diag-test/Melasma_Test/melasma(9).JPG', target_size=(224, 224))
image1 = img_to_array(image1)
# reshape data for the model
print(image1.shape)
image1 = image1.reshape((1, image1.shape[0], image1.shape[1], image1.shape[2]))
print(image1.shape)
# prepare the image for the VGG model
image1 = preprocess_input(image1)
yhat = model.predict(image1, verbose=0)[0]
print(yhat)
print(yhat.max())

obj_name=''
if yhat[0] == yhat.max():
  obj_name = 'acne scars'
elif yhat[1] == yhat.max():
  obj_name = 'alopecia areata'
elif yhat[2] == yhat.max():
  obj_name = 'melasma'
elif yhat[3] == yhat.max():
  obj_name = 'vitiligo'
elif yhat[4] == yhat.max():
  obj_name = 'warts'
elif yhat[5] == yhat.max():
  obj_name = 'acanthosis nigricans'
elif yhat[6] == yhat.max():
  obj_name = 'acne'    

print(obj_name)