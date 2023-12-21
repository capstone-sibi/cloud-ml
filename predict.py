from keras.models import load_model
import cv2
import numpy as np
from PIL import Image

def get_prediction(video_path, model_path, weights_path):
    classes = ['aku', 'kamu', 'maaf', 'semangat', 'senang', 'terimakasih']

    cap = cv2.VideoCapture(video_path)
    model = load_model(model_path)
    model.load_weights(weights_path)
    # Check if the video file is opened successfully
    if not cap.isOpened():
        print("Error opening video file")
        exit()

    sequence_to_predict = []

    frame_count = 0
    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # Break the loop if we have reached the end of the video
        if not ret:
            break

        # Process the frame (you can perform operations on the frame here)
        if frame_count % 5 == 0:
            frame.resize((84, 112))
            pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img_array = np.array(pil_image)
            sequence_to_predict.append(img_array)

        frame_count += 1
        if len(sequence_to_predict) == 7:
            break

    sequence_to_predict = np.array(sequence_to_predict)
    expanded_array = np.expand_dims(sequence_to_predict, axis=0)
    predictions = model.predict(expanded_array)

    final_prediction = np.argmax(predictions[0])
    final_prediction_label = classes[final_prediction]
    print(predictions[0])
    print(final_prediction_label)
    return final_prediction_label