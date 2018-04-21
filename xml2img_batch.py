#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
将xml记录的标记转换为二进制模版图像

'''


import os, sys
import cv2
import numpy as np
import copy
import xml.etree.ElementTree as ET


width, height, x, y, a, b, angle = 0,0,0,0,0,0,0


def generate_mask(xml_path, img_path, save_path, test):
    tree = ET.parse(xml_path)
        
    # 解析xml文件并遍历相应的节点，根据标签名称伏予相应的值
    
    for elem in tree.iter():
        #print elem.tag, elem.attrib, elem.text
        if elem.tag == "width":
            width = int(elem.text)
        elif elem.tag == "height":
            height = int(elem.text)
        elif elem.tag == "x":
            x = int(elem.text)
        elif elem.tag == "y":
            y = int(elem.text)
        elif elem.tag == "a":
            a = int(elem.text)
        elif elem.tag == "b":
            b = int(elem.text)
        elif elem.tag == "angle":
            angle = int(elem.text)
        
    print(width, height, x, y, a, b, angle)
    
    mask_image = np.zeros((height,width), np.uint8)
    pts = cv2.ellipse2Poly((x,y), (a,b), angle, 0, 360, 15)
    cv2.fillConvexPoly(mask_image, pts, (255,255))
    ret,thresh = cv2.threshold(mask_image, 127, 255, cv2.THRESH_BINARY)
    print test 
    if test:
        img_ori = cv2.imread(img_path)
        img_masked = cv2.bitwise_and(img_ori, img_ori, mask = thresh)    
        cv2.imshow("image", img_ori)
        cv2.imshow("mask", thresh)
        cv2.imshow("img_masked",img_masked)
        cv2.waitKey()
        cv2.destroyAllWindows()
     
    
    else:
        cv2.imwrite(save_path,thresh)
   


if __name__ == "__main__":
    test = False
    # chang to your path of images here
    base_dir = ""
    annotation_dir = os.path.join(base_dir, "Annotations")
    image_dir = os.path.join(base_dir, "origin_images")
    save_dir = os.path.join(base_dir,"Annotations_image")

    for root, dirs, files in os.walk(annotation_dir):
        for xml_file in files:
            #print xml_file
            
            image_file = xml_file.split(".")[0] + ".jpg"
            mask_file = xml_file.split(".")[0] +"_mask.jpg"
            #print xml_file, image_file, mask_file

            xml_path = os.path.join(annotation_dir,xml_file)
            image_path = os.path.join(image_dir,image_file)
            save_path = os.path.join(save_dir, mask_file)
            print xml_path, image_path, save_path

            generate_mask(xml_path, image_path, save_path, test)            


