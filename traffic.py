import cv2
import numpy as np
import flask
from flask import Flask, render_template, Response
import paho.mqtt.client as mqtt


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

topic_send = "george/number_of_cars"
topic_listen= "george/light"

current_active = 'A'
current_time = 0


uri = "mongodb+srv://benjamin:2is_george@cluster.iwa9w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
clientMongo = MongoClient(uri, server_api=ServerApi('1'))

try:
    clientMongo.traffic.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



def on_message(client, data, message):
    global current_active
    print ("we are in on message")
    a = f"Received:{message.payload.decode('UTF-8')} on topic {message.topic}"
    message = message.payload.decode('UTF-8')
    data = message.split(",")
    current_active = data[0]
    current_time = int(data[1].strip())


def publish(state):
        msg = f"" + state

        # add some  
        result = client.publish(topic_send, msg)
        print(state)
        # result: [0, 1]
        status = result[0]

        # save the number to mongo db database mongo , the schema is {"_id":{"$oid":"673c9b9634f053bad56c85a6"},"cars_lane_one":{"$numberInt":"423"},"cars_lane_two":{"$numberInt":"33"},"current_active":{"$numberInt":"1"}}
        # clientMongo.traffic.current.insert_one({"cars_lane_one":int(state.split(",")[0]),"cars_lane_two":int(state.split(",")[1]),"current_active":current_active})
        if status == 0:
            pass
            # print(f"Send `{msg}` to topic `{topic_send}`")
        else:
            print(f"Failed to send message to topic {topic_send}")  


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect('localhost', 1883, 120)
client.subscribe(topic_listen, qos=0)
client.on_message = on_message
client.loop_start()

# Load YOLO modelq
net = cv2.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Load COCO names for object classes
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Load the video file
video_path_first = 'video2.mp4'  # Replace with your video file path

video_path_second = 'video2.mp4'  # Replace with your video file path
cap_first = cv2.VideoCapture(video_path_first)

cap_second = cv2.VideoCapture(video_path_second)

# loop the video infinitely

ret, frame_one = cap_first.read()
ret, frame_two = cap_second.read()
car_count_second = 1
car_count_first = 1



while cap_first.isOpened() :
    car_count_second = 1
    car_count_first = 1





    if current_active =='A':
        ret, frame_one = cap_first.read()
        if not ret:
            break

        # Prepare the image
        blob = cv2.dnn.blobFromImage(frame_one, 1/255, (320, 320), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outputs = net.forward(net.getUnconnectedOutLayersNames())

        



        # Analyze results
        h, w = frame_one.shape[:2]
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.6 and class_id == 2:  # Class ID 2 corresponds to 'car' in COCO
                    box = detection[0:4] * np.array([w, h, w, h])
                    (center_x, center_y, width, height) = box.astype("int")
                    x = int(center_x - width / 2)
                    y = int(center_y - height / 2)
                    cv2.rectangle(frame_one, (x, y), (x + int(width), y + int(height)), (255, 0, 0), 2)
                    cv2.putText(frame_one, f"{classes[class_id]} {confidence:.2f}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


        
                    
        # write the program to count number of cars
        # in the video
        car_count_first = 0
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.6 and class_id == 2:  # Class ID 2 corresponds to 'car' in COCO
                    car_count_first += 1



        


        # Display the output
        # cv2.imshow('Car Detection', frame)
        if cap_first.get(cv2.CAP_PROP_POS_FRAMES) == cap_first.get(cv2.CAP_PROP_FRAME_COUNT):
            cap_first.set(cv2.CAP_PROP_POS_FRAMES, 0)



    if current_active =='B':
        ret_two, frame_two = cap_second.read()
        if not ret:
            break

        # Prepare the image
        blob = cv2.dnn.blobFromImage(frame_two, 1/255, (320, 320), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outputs = net.forward(net.getUnconnectedOutLayersNames())



        # Analyze results
        h, w = frame_two.shape[:2]
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.6 and class_id == 2:  # Class ID 2 corresponds to 'car' in COCO
                    box = detection[0:4] * np.array([w, h, w, h])
                    (center_x, center_y, width, height) = box.astype("int")
                    x = int(center_x - width / 2)
                    y = int(center_y - height / 2)
                    cv2.rectangle(frame_two, (x, y), (x + int(width), y + int(height)), (255, 0, 0), 2)
                    cv2.putText(frame_two, f"{classes[class_id]} {confidence:.2f}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


        
                    
        # write the program to count number of cars
        # in the video
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.6 and class_id == 2:  # Class ID 2 corresponds to 'car' in COCO
                    car_count_second += 1
        
        



    # combine frame and frame_two side by side

    frame_one = cv2.resize(frame_one, (640, 480))
    frame_two = cv2.resize(frame_two, (640, 480))
    
    cv2.putText(frame_two, f"Cars: {car_count_second}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    cv2.putText(frame_one, f"Cars: {car_count_first}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.putText(frame_one, "Lane A", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (24, 20, 20), 2)
    cv2.putText(frame_two, "Lane B", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (24, 20, 20), 2)


    frame_concat = np.concatenate((frame_one, frame_two), axis=1)
    cv2.imshow('Car Detection', frame_concat)


    if cap_first.get(cv2.CAP_PROP_POS_FRAMES) % 30 == 0 or cap_second.get(cv2.CAP_PROP_POS_FRAMES) % 30 == 0:
        publish(str(str(car_count_first)+","+str(car_count_second)))



    
    # Display the output
    # cv2.imshow('Car Detection', frame_two)

    if cap_second.get(cv2.CAP_PROP_POS_FRAMES) == cap_second.get(cv2.CAP_PROP_FRAME_COUNT):
        cap_second.set(cv2.CAP_PROP_POS_FRAMES, 0)


    
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
client.loop_stop()
cap_first.release()
cv2.destroyAllWindows()
