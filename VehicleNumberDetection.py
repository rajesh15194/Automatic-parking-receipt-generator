import cv2
import random
import os
import numpy as np
import matplotlib.pyplot as plt
print(cv2.__version__)

image = cv2.imread("C:/Users/rajes/Desktop/car.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def plot_images(img1, img2, title1="", title2=""):
    fig = plt.figure(figsize=[15,15])
    ax1 = fig.add_subplot(121)
    ax1.imshow(img1, cmap="gray")
    ax1.set(xticks=[], yticks=[], title=title1)
    ax2 = fig.add_subplot(122)
    ax2.imshow(img2, cmap="gray")
    ax2.set(xticks=[], yticks=[], title=title2)

plot_images(image, gray)
blur = cv2.bilateralFilter(gray, 11,90, 90)
plot_images(gray, blur)
edges = cv2.Canny(blur, 30, 200)
plot_images(blur, edges)
cnts, new = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
image_copy = image.copy()
_ = cv2.drawContours(image_copy, cnts, -1, (255,0,255),2)
plot_images(image, image_copy)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
image_copy = image.copy()
_ = cv2.drawContours(image_copy, cnts, -1, (255,0,255),2)
plot_images(image, image_copy)
plate = None
for c in cnts:
    perimeter = cv2.arcLength(c, True)
    edges_count = cv2.approxPolyDP(c, 0.02 * perimeter, True)
    if len(edges_count) == 4:
        x,y,w,h = cv2.boundingRect(c)
        plate = image[y:y+h, x:x+w]
        break

cv2.imwrite("plate.png", plate)
plot_images(image, plate)

import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
Vehicle_Number = pytesseract.image_to_string(plate, lang="eng")
print(Vehicle_Number)

from datetime import datetime
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

from reportlab.pdfgen import canvas
c = canvas.Canvas("receipt1.pdf",pagesize=(200,250),bottomup=0)
# Logo Section
# Setting th origin to (10,40)
c.translate(10,40)
# Inverting the scale for getting mirror Image of logo
c.scale(1,-1)
# Inserting Logo into the Canvas at required position
c.drawImage("https://st.depositphotos.com/1431107/2001/v/450/depositphotos_20012645-stock-illustration-car-parking-sign-vector-illustration.jpg",0,0,width=40,height=40)
# Title Section
# Again Inverting Scale For strings insertion
c.scale(1,-1)
# Again Setting the origin back to (0,0) of top-left
c.translate(-10,-40)
# Setting the font for Name title of company
c.setFont("Helvetica-Bold",10)
# Inserting the name of the company
c.drawCentredString(125,20,"XYZ PARKING LIMITED")
# For under lining the title
c.line(70,22,180,22)
# Changing the font size for Specifying Address
c.setFont("Helvetica-Bold",5)
c.drawCentredString(125,30,"Address Line 1")
c.drawCentredString(125,35,"Address Line 2")
c.line(5,45,195,45)
# Document Information
# Changing the font for Document title
c.setFont("Courier-Bold",8)
c.drawCentredString(100,55,"PARKING RECEIPT")
c.line(5,63,195,63)
c.setFont("Times-Bold",5)
c.drawRightString(90,80,"VEHICLE TYPE :")
c.drawRightString(150,80,"FOUR WHEELER")
c.drawRightString(90,90,"VEHICLE NUMBER :")
c.drawRightString(150,90, Vehicle_Number )
c.drawRightString(90,100,"DATE AND TIME :")
c.drawRightString(150,100, dt_string)
c.drawRightString(90,110,"PARKING CHARGES :")
c.drawRightString(130,110," Rs.50 /-")
c.line(5,130,195,130)
c.drawCentredString(100,140,"THANK YOU AND DRIVE SAFELY !")
c.line(5,150,195,150)
# End the Page and Start with new
c.showPage()
# Saving the PDF
c.save()

