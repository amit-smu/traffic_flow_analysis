"""
convert yolo format to txt
"""
import os
import cv2

BASE_DIR = "../dataset"
CAM_ID = 1705
IN_IMG_DIR = "{}/cam_{}".format(BASE_DIR, CAM_ID)
OUT_IMG_DIR = "{}/cam_{}_detections_yolov3".format(BASE_DIR, CAM_ID)
DETECTIONS_FILE = "{}/traffic_cam_{}/result.txt".format(BASE_DIR, CAM_ID)
FINAL_OUTPUT_FILE = "{}/traffic_cam_{}/traffic_data.txt".format(BASE_DIR, CAM_ID)
HIGHWAY_VEHICLES = ["car", "motorbike", "bus", "truck", "bicycle", "person"]

with open(DETECTIONS_FILE) as in_file:
    with open(FINAL_OUTPUT_FILE, 'w') as out_file:
        out_file.write("timestamp,cam_id,vehicle_count\n")
        image = None
        data = in_file.read().strip().split("\n")
        obj_count = 0
        for d in data:
            if d.__contains__("jpg"):
                if image is not None:
                    cv2.imwrite("{}/{}".format(OUT_IMG_DIR, img_name), image)
                    out_file.write("{},{},{}\n".format(img_name[:-4], CAM_ID, obj_count))
                    out_file.flush()
                    obj_count = 0
                img_name = d.split("jpg")[0][-20:] + "jpg"
                print(img_name)
                # open image
                image = cv2.imread("{}/{}".format(IN_IMG_DIR, img_name))

            else:
                d = d.split(", ")
                obj = d[0]
                vehicle = obj.split(":")[0]
                if vehicle not in HIGHWAY_VEHICLES:
                    continue
                x, y, w, h = d[1].split(" ")
                x = max(0, int(x))
                y = max(0, int(y))
                w = int(w)
                h = int(h)

                # draw these coordinates on image
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
                # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, obj, (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
                obj_count += 1
