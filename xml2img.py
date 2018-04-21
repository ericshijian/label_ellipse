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



xml_file = "test.xml"
tree = ET.parse(xml_file)


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
    
# print(width, height, x, y, a, b, angle)

mask_image = np.zeros((height,width), np.uint8)
pts = cv2.ellipse2Poly((x,y), (a,b), angle, 0, 360, 15)
cv2.fillConvexPoly(mask_image, pts, (255,255))
ret,thresh = cv2.threshold(mask_image, 127, 255, cv2.THRESH_BINARY)  
img_file = "test.jpg"
img_ori = cv2.imread(img_file)

img_masked = cv2.bitwise_and(img_ori, img_ori, mask = thresh)

print thresh.shape

cv2.imshow("image", img_ori)
cv2.imshow("mask", thresh)
cv2.imshow("img_masked",img_masked)
cv2.imwrite("test_mask.jpg",thresh)
cv2.waitKey()
cv2.destroyAllWindows()

