import numpy as np
import cv2

# ----- Constants

faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('Cascades/haarcascade_eye.xml')
smileCascade = cv2.CascadeClassifier('Cascades/haarcascade_smile.xml')

# ----- Utility

def unzip(ts):
    fs, ss = [], []
    for fst, snd in ts:
        fs.append(fst)
        ss.append(snd)
    return fs, ss

# ----- Input

def gen_frames(source=0, w=640, h=480):
    ''' Generates a stream of images from source mentioned '''
    cap = cv2.VideoCapture(0)
    cap.set(3, w) # set Width
    cap.set(4, h) # set Height
    while True:
        ret, img = cap.read()
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        yield img
    cap.release()

def gray_image(img):
    ''' Series of transformations to perform on an image '''
    img = cv2.flip(img, -1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

# ----- Face Cascades

def get_faces(img):
    faces = faceCascade.detectMultiScale(
        img,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30)
    )
    return faces

def get_rois(img, gray, f):
    x, y, w, h = f
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]

    return roi_gray, roi_color

# ----- Eye Cascades

def get_eyes(roi_gray):
    eyes = eyeCascade.detectMultiScale(
        roi_gray,
        scaleFactor=1.5,
        minNeighbors=5,
        minSize=(5, 5),
    )
    return eyes

# ----- Smile Cascades

def get_smile(roi_gray):
    smile = smileCascade.detectMultiScale(
        roi_gray,
        scaleFactor=1.5,
        minNeighbors=5,
        minSize=(5, 5),
    )
    return smile

# ----- Main

if __name__ == '__main__':
    for img in gen_frames():
        gray = gray_image(img)

        faces = get_faces(gray)
        for x, y, w, h in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        mroi = map(lambda f: get_rois(img, gray, f), faces)
        roi_grays, roi_colors = unzip(mroi)

        smiles = map(get_smile, roi_grays)
        for x, y, w, h in smiles:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        eyes = map(get_eyes, roi_grays)
        for x, y, w, h in eyes:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('video', img)
