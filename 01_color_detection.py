from tkinter import *
from tkinter.messagebox import *
from PIL import ImageTk, Image #image display
from tkinter.filedialog import askopenfile
import cv2
import numpy as np
import pyttsx3 as pt
import pandas as pd
import argparse

# Creating argument parser to take image path from command line
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image',  help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

e = pt.init()

root = Tk()
root.title("COLOR DETECTION USING PYTHON")
HEIGHT = 600
WIDTH = 600
root.resizable(False, False)
root.geometry(f"{WIDTH}x{HEIGHT}+2+2")
root.config(background="#FFFF8F")

# Reading the image with opencv
img = cv2.imread(r"sample1.jpg")
img1 = cv2.imread(r"sample2.jpeg")

image_1 = ImageTk.PhotoImage(Image.open(r"sample1.jpg").resize((220, 150)))
image_2 = ImageTk.PhotoImage(Image.open(r"sample2.jpeg").resize((220, 150)))

font = ("Arial", 20)

Label(root, background="#FFFF8F",
      text="CLICK ON THE IMAGE TO DETECT COLOR", font=font).pack()

# declaring global variables (are used later on)
clicked = False
r = g = b = xpos = ypos = 0

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv(r'colors.csv', names=index, header=None)

# function to calculate minimum distance from all colors and get the most matching color

def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G -
                                                int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if(d <= minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# function to get x,y coordinates of mouse double click


def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


def draw_function1(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img1[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


# image = int(input("Please Select the Image!"))

def print_color_name_on_img(img):
    global clicked
    cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

    text = getColorName(r, g, b) + ', RGB(' + str(r) + \
        ',' + str(g) + ',' + str(b) + ')'

    cv2.putText(img, text, (50, 50), 2, 0.8,
                (255, 255, 255), 2, cv2.LINE_AA)

    if(r+g+b >= 600):
        cv2.putText(img, text,  (50, 50), 2, 0.8,
                    (0, 0, 0), 2, cv2.LINE_AA)

    e.say(getColorName(r, g, b))
    e.runAndWait()

    clicked = False

# if(image == 1):


def show_img_1():
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_function)

    while(1):
        cv2.imshow("image", img)
        if (clicked):
            print_color_name_on_img(img)

        # Break the loop when user hits 'esc' key
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


def show_img_2():
    cv2.namedWindow('image1')
    cv2.setMouseCallback('image1', draw_function1)

    while(1):
        cv2.imshow("image1", img1)
        if (clicked):
            print_color_name_on_img(img1)

        # Break the loop when user hits 'esc' key
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


def show_other_image():
    f_types = [
        ('image files','*.jpg'),
        ('image files','*.png'),
        ('image files','*.jpeg')
    ]
    file = askopenfile(filetypes=f_types, title="Open Image")


    def draw_function2(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            global b, g, r, xpos, ypos, clicked
            clicked = True
            xpos = x
            ypos = y
            b, g, r = _image[y, x]
            b = int(b)
            g = int(g)
            r = int(r)

    try:
        file_path = file.name
        _image = cv2.imread(file_path)

        cv2.namedWindow('Image3')
        cv2.setMouseCallback('Image3', draw_function2)
    

        while(1):
            cv2.imshow("Image3", _image)
            if (clicked):
                print_color_name_on_img(_image)

            # Break the loop when user hits 'esc' key
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    except Exception:
        showerror("WARNING","Please Select the Image")
    

def onHover(colorOnHover, colorWhenLeave, button):

    button.bind('<Enter>', func=lambda f: button.config(
        background=colorOnHover))
    button.bind('<Leave>', func=lambda g: button.config(
        background=colorWhenLeave))


Label(root, background="#FFFF8F", font=("Arial", 18),
      text="SAMPLE 1 ").place(x=10, y=130)
button1 = Button(root, background="#FFFF8F", image=image_1, command=show_img_1)
button1.place(x=140, y=70)

Label(root, background="#FFFF8F", font=("Arial", 18),
      text="SAMPLE 2 ").place(x=10, y=308)
button2 = Button(root, background="#FFFF8F", image=image_2, command=show_img_2)
button2.place(x=140, y=250)

Label(root, background="#FFFF8F", font=("Arial", 18),
      text="Want to Detect Color in Other Image ? ").place(x=10, y=440)

btn = Button(root, activebackground="#DFFF00", background="#FFFF8F",
             text="CLICK HERE TO OPEN IMAGE FROM LOCAL DISK", wraplength=100, command=show_other_image)
btn.place(x=440, y=435)

onHover("#FFF8DC", "#FFFF8F", btn)

root.mainloop()