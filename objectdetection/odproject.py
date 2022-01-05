import os
from tkinter import *
import cv2
import numpy as np
import tkfilebrowser
from PIL import Image
from PIL import ImageTk
from gtts import gTTS
from playsound import playsound
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def select_image():
    global panelA, panelB
    path = tkfilebrowser.askopenfilename()
    # path = tkFileDialog.askopenfilename()

    if len(path) > 0:
        # load the image from disk, convert it to grayscale, and detect
        # edges in it

        net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
        classes = []
        with open("coco.names", "r") as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))

        # Loading image
        img1 = cv2.imread(path)
        img1 = cv2.resize(img1, None, fx=0.4, fy=0.4)
        img = cv2.imread(path)
        img = cv2.resize(img, None, fx=0.4, fy=0.4)
        # img1 = img
        height, width, channels = img.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        print(indexes)
        font = cv2.FONT_HERSHEY_PLAIN
        voice = ''
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                voice += label + " "
                print(label)
                color = colors[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 2, color, 2)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img1 = Image.fromarray(img1)
        # ...and then to ImageTk format
        img = img.resize((400, 400))
        img1 = img1.resize((400, 400))
        img = ImageTk.PhotoImage(img)
        img1 = ImageTk.PhotoImage(img1)

        if panelA is None or panelB is None:
            # the first panel will store our original image
            panelA = Label(image=img1)
            panelA.image = img1
            panelA.pack(side="left", padx=10, pady=10)
            # while the second panel will store the edge map
            panelB = Label(image=img)
            panelB.image = img
            panelB.pack(side="right", padx=10, pady=10)
            # otherwise, update the image panels
        else:
            # update the pannels
            panelA.configure(image=img1)
            panelB.configure(image=img)
            panelA.image = img1
            panelB.image = img
        language = 'en'
        myobj = gTTS(text=voice, lang=language, slow=True)
        myobj.save("new3.mp3")
        #os.system("mpq321 new2.mp3")
        playsound("new3.mp3")
        email = 'elenasalvatore0130@gmail.com'  # Your email
        password = 'elenasalvatore123'  # Your email account password
        send_to_email = 'dhruvihl369@gmail.com'  # Who you are sending the message to
        subject = 'object detection'
        message = voice  # The message in the email
      #  file_location = 'D:\\cardboard, garbage bags and containers\\data\\images\\frame270.jpg'
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = send_to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        # Setup the attachment
        #filename = os.path.basename(file_location)
        #attachment = open(file_location, "rb")
        #part = MIMEBase('application', 'octet-stream')
        #part.set_payload(attachment.read())
        #encoders.encode_base64(part)
        #part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        # Attach the attachment to the MIMEMultipart object
        #msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, send_to_email, text)
        server.quit()
        # cv2.imshow("Image", img)
        # cv2.imwrite("D:\objectdetection\imgnew4.jpg", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        '''gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 100)
        # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # convert the images to PIL format...
        image = Image.fromarray(image)
        edged = Image.fromarray(edged)
        # ...and then to ImageTk format
        image = ImageTk.PhotoImage(image)
        edged = ImageTk.PhotoImage(edged)
        # if the panels are None, initialize them
        if panelA is None or panelB is None:
            # the first panel will store our original image
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)
            # while the second panel will store the edge map
            panelB = Label(image=edged)
            panelB.image = edged
            panelB.pack(side="right", padx=10, pady=10)
        # otherwise, update the image panels
        else:
            # update the pannels
            panelA.configure(image=image)
            panelB.configure(image=edged)
            panelA.image = image
            panelB.image = edged

'''


# initialize the window toolkit along with the two image panels
root = Tk()
panelA = None
panelB = None
root.minsize(300, 300)
# create a button, then when pressed, will trigger  a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
Label(root, text='Detect the objects', font=('Verdana', 15)).pack(side=TOP, pady=10)
btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
# kick off the GUI
root.mainloop()
