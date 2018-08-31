import os
import zipfile

import cv2 as cv
import dlib

from config import identity_annot_filename, image_folder
from utils import ensure_folder

predictor_path = 'models/shape_predictor_68_face_landmarks.dat.bz2'

# Load all the models we need: a detector to find the faces, a shape predictor
# to find face landmarks so we can precisely localize the face
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)


def ensure_dlib_model():
    if not os.path.isfile(predictor_path):
        import urllib.request
        urllib.request.urlretrieve("http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2",
                                   filename="models/shape_predictor_68_face_landmarks.dat.bz2")


def extract(folder):
    filename = '{}.zip'.format(folder)
    print('Extracting {}...'.format(filename))
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall('data')


def check_one_image(line):
    line = line.strip()
    if len(line) > 0:
        tokens = line.split(' ')
        image_name = tokens[0].strip()
        filename = os.path.join(image_folder, image_name)
        img = cv.imread(filename)
        dets = detector(img, 1)

        num_faces = len(dets)
        if num_faces == 0:
            print("Sorry, there were no faces found in '{}'".format(filename))
            exit()

        # Find the 5 face landmarks we need to do the alignment.
        faces = dlib.full_object_detections()
        for detection in dets:
            faces.append(sp(img, detection))

        window = dlib.image_window()

        # Get the aligned face images
        # Optionally:
        # images = dlib.get_face_chips(img, faces, size=160, padding=0.25)
        images = dlib.get_face_chips(img, faces, size=320)
        for image in images:
            window.set_image(image)
            dlib.hit_enter_to_continue()

        # It is also possible to get a single chip
        image = dlib.get_face_chip(img, faces[0])
        window.set_image(image)
        dlib.hit_enter_to_continue()

        # try:
        #     resized = cv.resize(original, (img_size, img_size), cv.INTER_CUBIC)
        # except cv.error as err:
        #     print(filename)
        #     print('image_name={} original.shape={}'.format(image_name, original.shape))
        #     print('image_name={} resized.shape={}'.format(image_name, resized.shape))


def check_image():
    with open(identity_annot_filename, 'r') as file:
        lines = file.readlines()
    check_one_image(lines[0])

    # pool = Pool(24)
    # for _ in tqdm(pool.imap_unordered(check_one_image, lines), total=len(lines)):
    #    pass
    # pool.close()
    # pool.join()


if __name__ == '__main__':
    # parameters
    ensure_folder('data')
    ensure_folder('models')
    ensure_dlib_model()

    if not os.path.isdir(image_folder):
        extract(image_folder)

    check_image()
