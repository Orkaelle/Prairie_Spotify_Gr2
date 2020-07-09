#############################################
# Object detection - YOLO - OpenCV
# Author : Arun Ponnusamy   (July 16, 2018)
# Website : http://www.arunponnusamy.com
############################################
import matplotlib.image as mpimg
import wget
import cv2
import argparse
import numpy as np
import os

YOLO_FOLDER = os.getcwd() + os.sep + "yolo" 
TEMPORARY_FOLDER =  os.getcwd() + os.sep + "yolo" +  os.sep + "tmp"
TEMPORARY_FILE_IN =  TEMPORARY_FOLDER +  os.sep + "cover.jpg"
TEMPORARY_FILE_OUT =  TEMPORARY_FOLDER +  os.sep + "cover-transformed.jpg"
YOLO_TXT =  YOLO_FOLDER +  os.sep + "yolo.txt"
YOLO_WEIGHTS =  YOLO_FOLDER +  os.sep + "yolov3.weights"
YOLO_CFG =  YOLO_FOLDER +  os.sep + "yolo.cfg"

def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, label , color, confidence, x, y, x_plus_w, y_plus_h):
    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    print("{}  -> {:.2f}".format(label, confidence))

def cleanup_files():
    #clean up imgs
    if os.path.exists(TEMPORARY_FILE_IN):
        os.remove(TEMPORARY_FILE_IN)
    if os.path.exists(TEMPORARY_FILE_OUT):
        os.remove(TEMPORARY_FILE_OUT)

def cover_analysis(url):
   
    #get cover from web
    wget.download(url, TEMPORARY_FILE_IN)
    image = mpimg.imread(TEMPORARY_FILE_IN)

    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    with open(YOLO_TXT, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    net = cv2.dnn.readNet(YOLO_WEIGHTS, YOLO_CFG)

    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    results = []
    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        object_id=class_ids[i]
        draw_prediction(image, str(classes[object_id]), colors[object_id], confidences[i], round(x), round(y), round(x+w), round(y+h))
        results.append([classes[object_id], int(confidences[i]*100)])

    cv2.imwrite(TEMPORARY_FILE_OUT, image)

    return results

