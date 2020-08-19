from keras.preprocessing.image import load_img, img_to_array
from helper import create_top_model, class_labels, target_size
import numpy as np
from keras import applications
import operator
import matplotlib.pyplot as plt
import argparse

img_path = 'img_2810.jpg'

# prepare image for classification using keras utility functions
image = load_img(img_path, target_size=target_size)

image_arr = img_to_array(image) # convert from PIL Image to NumPy array
image_arr /= 255

# to be able to pass it through the network and use batches, we want it with shape (1, 224, 224, 3)
image_arr = np.expand_dims(image_arr, axis=0)
# print(image.shape)

# build the VGG16 network  
model = applications.VGG16(include_top=False, weights='imagenet')  

# get the bottleneck prediction from the pre-trained VGG16 model  
bottleneck_features = model.predict(image_arr) 

# build top model  
model = create_top_model("softmax", bottleneck_features.shape[1:])

model.load_weights("res/top_model_weights.h5")

predicted = model.predict(bottleneck_features)
decoded_predictions = dict(zip(class_labels, predicted[0]))
decoded_predictions = sorted(decoded_predictions.items(), key=operator.itemgetter(1), reverse=True)

print()
count = 1
for key, value in decoded_predictions[:5]:
    print("{}. {}: {:8f}%".format(count, key, value*100))
    count += 1

# print image
plt.imshow(image)
plt.axis('off')
plt.show()