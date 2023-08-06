from tkinter.messagebox import showinfo
from imageai.Detection import ObjectDetection
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import ImageTk, Image as img
import pyttsx3
from tkinter import *
import time
from tkinter.filedialog import askopenfile
import threading


detection = ""

root = Tk()
root.title("OBJECT DETECTION USING PYTHON")
root.resizable(False,False)
HEIGHT = 600
WIDTH = 900
root.geometry(f"{WIDTH}x{HEIGHT}+5+120")


font = ("Arial",30)

Label(root,background= "#FFFF8F",text="OBJECT DETECTION IN PYTHON",font=font).pack()
image_1 = ImageTk.PhotoImage(img.open(r"sample1.jpg").resize((220, 150)))
image_2 = ImageTk.PhotoImage(img.open(r"sample2.jpeg ").resize((220, 150)))



detector = ObjectDetection()

e = pyttsx3.init()

model_path = r"YONO\yolo.h5"
input_path = ""
       

def set_img_1():
    global input_path
    input_path = r"sample1.jpg"
    d = detect()
    d.start()

def set_img_2():
    global input_path
    input_path = f"sample2.jpeg"
    # detect(input_path)
    d = detect()
    d.start()


def perform_detection_on_img_frm_local_disk():
    f_type = (
        ("image files","*.jpg"),
        ("image files","*.jpeg"),
        ("image files","*.png")
    )
    file = askopenfile(filetypes=f_type,title="Open PNG,JPEG or JPG file")
    file_path = file.name

    global input_path
    input_path = file_path

    # detect(input_path)
    d = detect()
    d.start()


output_path = r"OUTPUT/sample.jpg"

img_path = input_path


detector.setModelTypeAsYOLOv3()
detector.setModelPath(model_path)
detector.loadModel()




class print_detect_details_in_screen(threading.Thread):
    def run(self):
        def plot_input():
            img = mpimg.imread(input_path)
            # imgplot = plt.imshow(img)
            plt.title('Input Image')
            plt.show()


        def plot_output():
            img2 = mpimg.imread(output_path)
            imgplot2 = plt.imshow(img2)
            plt.title('Output Image')
            plt.show()


        objects = []      

        for eachItem in detection:
            if not eachItem['name'] in objects:
                objects.append(eachItem['name'])

        if(len(objects)):
            # plot_input()   
            plot_output() 
            sub_root = Tk()
            sub_root.geometry("500x540")
            sub_root.title("Detected Details")
            sub_root.resizable(False,False)

            Label(sub_root,text = "Objects with its percentage probability").place(x = 2,y = 2)

            f1 = Frame(sub_root)
            f1.place(relx=0.01,rely=0.04)


            list_of_objects_wth_percentage_probaility = Listbox(f1,width=27)

            s_b_1 = Scrollbar(f1)
            s_b_1.pack(side = RIGHT,fill=Y)
            j = 1

            for eachItem in detection:
                print(eachItem["name"] , " : ", eachItem["percentage_probability"])
                text = str(eachItem["name"]) + " : " + str(eachItem["percentage_probability"])
                list_of_objects_wth_percentage_probaility.insert(j,text)
                j+= 1

            list_of_objects_wth_percentage_probaility.pack()
            list_of_objects_wth_percentage_probaility.config(yscrollcommand=s_b_1.set)

            s_b_1.config(command=list_of_objects_wth_percentage_probaility.yview)
            Label(sub_root,text = "The Detected Objects are follows").place(relx=0.5,y = 2)

           
            f2 = Frame(sub_root)
            f2.place(relx=0.51,rely=0.04)


            s_b_2 = Scrollbar(f2)
            s_b_2.pack(side=RIGHT,fill = Y)

            list_of_objects = Listbox(f2,yscrollcommand=s_b_2.set,width=25)

            i = 1
            for object in objects:
                list_of_objects.insert(i , object)
                i += 1

            list_of_objects.pack()

            s_b_2.config(command=list_of_objects.yview)


            Label(sub_root,text = f"Total Objects in an Image are {len(detection)}").place(rely=0.45,relx=0.01)

            total_numbers = [0 for i in objects]

            for item in detection:
                index = objects.index(item['name'])
                total_numbers[index]+=1

            f3 = Frame(sub_root)
            f3.place(rely=0.5,relx=0.01)

            s_b_3= Scrollbar(f3)
            s_b_3.pack(side = RIGHT,fill=Y)

            counted_objects = Listbox(f3,yscrollcommand=s_b_3.set,width=40)
            counted_objects.pack()


            l = 1
            for i in range(len(objects)):
                counted_objects.insert(l,f"Total Number of \"{objects[i]}\" is {total_numbers[i]}")
                l += 1

            counted_objects.pack()
            s_b_3.config(command=counted_objects.yview)

            def speak():
                e.say("The Detected Objects are")
                e.runAndWait()

                for object in objects:
                    e.say(object)
                    e.runAndWait()


                e.say(f"Total Objects in an Image are {len(detection)}")
                e.runAndWait()


                for i in range(len(objects)):
                    e.say(f"Total Number of {objects[i]} is {total_numbers[i]}")
                    e.runAndWait()

                # e.say("Objects with its percentage probability")
                # e.runAndWait()

                # for eachItem in detection:
                #     text = str(eachItem["name"]) + " : " + str(eachItem["percentage_probability"])
                #     e.say(text)
                #     e.runAndWait()



            t = threading.Thread(target=speak)
            t.start()

            

            sub_root.mainloop()

        else:
            plot_input()
            e.say("No Any Objects Detected From the Image")
            e.runAndWait()
            showinfo("MASSAGE","No Any Objects Detected From the Image")

            plot_output()






class detect(threading.Thread):
    def run(self):
        global detection
        try:
            detection = detector.detectObjectsFromImage(input_image=input_path,output_image_path=output_path)
        except Exception:
            print("\nWrong Name/Path of Input Image or Input Image Not Found.Please Enter proper name with full path\n")
            e.say("Wrong Name/Path of Input Image or Input Image Not Found.Please Enter proper name with full path")
            e.runAndWait()
            exit(1)

        # print_detect_details_in_screen(detection)
        print_detail = print_detect_details_in_screen()
        print_detail.start()


font = ("Helvetica",18)

Label(root,text="SAMPLE 1",font=font, background= "#FFFF8F").place(x = 35,y = 140)
Button(root,image=image_1,command=set_img_1).place(x = 165,y = 80)
 
Label(root,text="SAMPLE 2",font=font, background= "#FFFF8F").place(x = 450,y = 140)
Button(root,image=image_2,command=set_img_2).place(x =580,y = 80)


font = ("Helvetica",15)
Label(root,text="CLICK BUTTON TO DETECT OBJECT IN IMAGE FROM LOCAL IMAGE",font=font, background= "#FFFF8F").place(x = 100,y = 260)

btn  = Button(root,text="DETECT OBJECT FROM IMAGE FROM THE LOCAL DISK",wraplength=130,command=perform_detection_on_img_frm_local_disk, background= "#FFFF8F")
btn.place(y = 295,x = 353)

root.config(background= "#FFFF8F")

root.mainloop()