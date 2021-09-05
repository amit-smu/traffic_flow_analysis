import cv2
import numpy as np
import os
import time

if __name__ == "__main__":
    YOLO_DIR = "./yolov3"
    DATA_DIR = "../dataset"
    CAM_ID = "1705"
    THRESHOLD = 0.3
    CONFIDENCE = 0.5
    CONFIG_PATH = "{}/{}".format(YOLO_DIR, "yolov3.cfg")
    WEIGHTS_PATH = "{}/{}".format(YOLO_DIR, "yolov3.weights")
    OUTPUT_DIR = "{}/cam_{}_detections".format(DATA_DIR, CAM_ID)
    HIGHWAY_OBJECTS = ['person', 'bicycle', 'car', 'motorbike', 'bus', 'truck']
    OUTPUT_FILE = "detections.txt"

    with open("{}/{}".format(YOLO_DIR, "coco.names"), 'r') as in_file:
        LABELS = in_file.read().strip().split("\n")
    print(LABELS)

    out_file = open("{}/{}".format(DATA_DIR, OUTPUT_FILE), 'a')
    out_file.write("image, cam_id, detected_objects\n")

    print("Loading Yolo.. \n")
    net = cv2.dnn.readNetFromDarknet(CONFIG_PATH, WEIGHTS_PATH)

    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    file_names = os.listdir("{}/cam_{}".format(DATA_DIR, CAM_ID))
    for img_name in file_names:
        print(img_name)
        # img_name = "2021-08-08-11-00-00.jpg"
        image = cv2.imread("{}/cam_{}/{}".format(DATA_DIR, CAM_ID, img_name))
        # image = cv2.imread("temp.jpg")
        (H, W) = image.shape[:2]

        # construct a blob from the input image and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes and
        # associated probabilities
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln)
        end = time.time()
        # show timing information on YOLO
        print("[INFO] YOLO took {:.6f} seconds".format(end - start))

        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > CONFIDENCE:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping bounding
        # boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE,
                                THRESHOLD)

        # ensure at least one detection exists
        total_objects = 0
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                h_obj = LABELS[classIDs[i]]
                if h_obj not in HIGHWAY_OBJECTS:
                    continue

                total_objects += 1
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                # draw a bounding box rectangle and label on the image
                # color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)
        # show the output image
        cv2.imwrite("{}/{}".format(OUTPUT_DIR, img_name), image)
        out_file.write("{}, {}, {}\n".format(img_name, CAM_ID, total_objects))
        out_file.flush()
        # cv2.waitKey(-1)

    # close file
    out_file.close()
