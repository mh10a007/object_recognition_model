import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

model = load_model('object_recognition_model.h5')

img_path = "image.png"
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

pred = model.predict(img_array)
class_names = ["headphones", "keyboard", "mouse", "phone","book","laptop","pen","water_bottle"]
print("Predicted Object: ", class_names[np.argmax(pred)])
