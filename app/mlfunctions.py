import os
from datetime import date, datetime

import face_recognition as fr
import cv2
from django.http import HttpResponse
import pickle
import numpy as np
from django.shortcuts import redirect, get_object_or_404

from .models import StudentClass, Student


def capture_face(request, img_name):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            print("pressed capture")
            img_name = "images/{}.jpg".format(img_name)
            cv2.imwrite(img_name, frame)
            cv2.destroyAllWindows()
            break
    train()
    return redirect("/")


def train():
    path = 'images'  # images folder name
    images = []  # list of images
    classNames = []  # list of image names
    myList = os.listdir(path)  # getting the list of items in a path
    print(myList)
    for cl in myList:
        currentImg = cv2.imread(f'{path}/{cl}')  # reading images using cv2
        images.append(currentImg)
        # extract class names without extension
        classNames.append(os.path.splitext(cl)[0])
    all_encodings = findEncodings(images)
    dumpPickleAss(all_encodings, classNames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert color to rgb
        en = fr.face_encodings(img)
        print(en)
        encode=en[0]
        encodeList.append(encode)
    return encodeList


def dumpPickleAss(all_encodings, imageClassNames):
    dict_pickle = {'face_encodings': all_encodings, 'image_class_names': imageClassNames}
    pickle_file = open('trainedpickle', 'ab')
    pickle.dump(dict_pickle, pickle_file)
    pickle_file.close()


def loadPickle():
    pickle_file = open('trainedpickle', 'rb')
    dict_pickle = pickle.load(pickle_file)
    return dict_pickle


def detect_cont(request):
    dict_pickled = loadPickle()
    encodeListKnown = dict_pickled['face_encodings']
    classNames = dict_pickled['image_class_names']
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25,
                          0.25)  # reducing and resizing to 1/4th the image for faster operations
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurrentFrame = fr.face_locations(imgS)  # all faces in a frame
        encodesCurrentFrame = fr.face_encodings(imgS, facesCurrentFrame)
        for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
            matches = fr.compare_faces(encodeListKnown, encodeFace)
            faceDistance = fr.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDistance)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                print(name)

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # multiplying to rescale the image we done previous
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255),
                            2)  # the numericals are color,thickness,dimension to  be present in image
                res = get_student_details(name)
                if res:
                    write_data(res.regno, res.name, res.stclass)
                    print('wrote')

        cv2.imshow('Webcam', img)  # webcam feed
        k = cv2.waitKey(1)  # second argument to prevent warning

        if k % 256 == 27:
            cv2.destroyAllWindows()
            print("pressed end")

            break
    return redirect('/')


def make_directories(stclassName):
    main_root = "/attendance_list"

    inside_root = (os.getcwd().replace('\\', '/') + main_root)

    dated_path = inside_root + '/' + str(date.today())

    if not os.path.isdir(dated_path):
        os.mkdir(dated_path)
    if not os.path.isfile(str(dated_path) + '/{}.csv'.format(stclassName)):
        print('goes')
        fp = open(str(dated_path) + '/{}.csv'.format(stclassName), 'w')
        fp.writelines('Register No.,Name,Time')
        fp.close()
    fp = open(str(dated_path) + '/{}.csv'.format(stclassName), 'r+')
    return fp
    # fp.close()


def return_csv(stclassName):
    return make_directories(stclassName)


def write_data(reg_no, name, stclassName):
    filep = return_csv(stclassName)
    myDataList = filep.readlines()
    regList = []
    for line in myDataList:
        entry = line.split(',')
        regList.append(entry[0])
    if reg_no not in regList:
        now = datetime.now()
        dtString = now.strftime('%H:%M:%S')
        filep.writelines(f'\n{reg_no},{name},{dtString}')
        filep.close()


def get_student_details(reg_no):
    obj = Student.objects.get(regno=str(reg_no))
    return obj


def get_directories():
    main_root = "/attendance_list"

    inside_root = (os.getcwd().replace('\\', '/') + main_root)
    return os.listdir(inside_root)


def get_csvs_by_date(date_input):
    main_root = "/attendance_list"

    inside_root = (os.getcwd().replace('\\', '/') + main_root + '/' + date_input)
    return {"files": os.listdir(inside_root), "path": date_input}


def get_csv_data(stclassName, date_input):
    main_root = "/attendance_list"

    inside_root = (os.getcwd().replace('\\', '/') + main_root + '/' + date_input)
    fileop = open(inside_root + '/' + stclassName, "r+")
    myDataList = fileop.readlines()
    List = []
    counts = 1
    for line in myDataList:
        if counts == 1:
            counts = counts + 1
            continue
        entry = line.split(',')
        List.append(entry)
    return List
