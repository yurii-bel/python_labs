import glob
import os
import cv2
from multiprocessing import Pool, cpu_count
from functools import partial
from timeit import default_timer as timer


INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
TYPES = ['*.jpg', '*.png', '*.jpeg']

face_cascade = cv2.CascadeClassifier(
    'haarcascade_frontalface_default.xml'
)


def get_img_paths():
    paths = []

    for file_type in TYPES:
        paths.extend(glob.glob(os.path.join(INPUT_DIR, file_type)))

    return paths


def replace_img_type_to_jpg(img_path):
    replace_types = ['.png', '.jpeg']

    img_name = img_path.split('/')[-1]
    for type in replace_types:
        img_name = img_name.replace(type, '.jpg')

    return img_name


def face_recognition(img_path):
    img = cv2.imread(img_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.2)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite(os.path.join(
        OUTPUT_DIR,
        replace_img_type_to_jpg(img_path)
        ),
        img
    )


def face_recognition_all(img_paths, n_processes):
    start = timer()
    with Pool(n_processes) as p:
        p.map(partial(face_recognition), img_paths)

    print(f'Took {timer() - start} seconds with {n_processes=}')


def test_all_cpus():
    max_processes = cpu_count()+1
    for n_processes in range(1, max_processes):
        face_recognition_all(img_paths, n_processes)


if __name__ == '__main__':
    img_paths = get_img_paths()
    # test_all_cpus()  # Best result with 3 processes

    n_processes = 3
    face_recognition_all(img_paths, n_processes)
