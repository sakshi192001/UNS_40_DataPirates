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
import joblib
warnings.filterwarnings("ignore")

IMAGE_SIZE = [224, 224]

train_path = 'C:/Users/Isha Patel/OneDrive/Desktop/PROJECTS/Evathon/evathon/train-20220123T025302Z-001/train'
valid_path = 'C:/Users/Isha Patel/OneDrive/Desktop/PROJECTS/Evathon/evathon/test/test'


vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

for layer in vgg.layers:
    layer.trainable = False

folders = glob('C:/Users/Isha Patel/OneDrive/Desktop/PROJECTS/Evathon/evathon/train-20220123T025302Z-001/train/*')

x = Flatten()(vgg.output)
prediction = Dense(2, activation='softmax')(x)

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

training_set = train_datagen.flow_from_directory('C:/Users/Isha Patel/OneDrive/Desktop/PROJECTS/Evathon/evathon/train-20220123T025302Z-001/train',
                                                 target_size = (224, 224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory('C:/Users/Isha Patel/OneDrive/Desktop/PROJECTS/Evathon/evathon/test/test',
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

model12=model.save('model2.h5')




