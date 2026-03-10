import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

class HeartSoundClassifier:
    def __init__(self):
        self.model = tf.keras.models.load_model('new_model/finalheartAICNN.keras')
        self.class_labels = ['Abnormal', 'Murmur', 'Normal']
    def preprocess_image(self, img_path):
        img = image.load_img(img_path, target_size=(240, 240))  # resize to match model input size
        img_array = image.img_to_array(img)  # convert to array
        img_array = np.expand_dims(img_array, axis=0)  # add batch dimension
        img_array /= 255.0  # rescale pixel values to [0, 1]
        return img_array

    def predict_image(self, img_path):
        img_array = self.preprocess_image(img_path)
        prediction = self.model.predict(img_array)
        predicted_class = self.class_labels[np.argmax(prediction)]
        confidence = np.max(prediction) * 100
        return predicted_class, confidence

    
    # classifier = HeartSoundClassifier(model_path, class_labels)
    
    # img_path = 'train/normal/84894_PV_spectrogram.png'  # replace with your image path
    # predicted_class, confidence = classifier.predict_image(img_path)
    
    # print(f"Predicted class: {predicted_class}")
    # print(f"Confidence: {confidence:.2f}")