"""
convert yolo format to txt
"""
import os
import cv2

DATA_DIR = "../dataset/cam_1705"
OUT_DIR = "../dataset/cam_1705_detections_yolov4"

with open("result.txt") as in_file:
    with open("result_formatted.txt", 'w') as out_file:
        image = None
        data = in_file.read().strip().split("\n")
        for d in data:
            if d.__contains__("jpg"):
                if image is not None:
                    cv2.imwrite("{}/{}".format(OUT_DIR, img_name), image)
                img_name = d.split(":")[0][-23:]
                print(img_name)
                # open image
                image = cv2.imread("{}/{}".format(DATA_DIR, img_name))


            elif d.__contains__("layer"):
                continue

            else:
                d = d.split("\t")
                obj = d[0]
                box = d[1].split("\t")[0]
                (x, y, w, h) = int(box[9:14]), int(box[24:29]), int(box[37:42]), int(box[52:56])
                print(x, y, w, h)
                # draw these coordinates on image
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
                # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, obj, (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
