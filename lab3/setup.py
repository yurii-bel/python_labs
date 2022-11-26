import glob
import shutil
import os


src_dir = 'input/images/'
dst_dir = 'input'
types = ['*.jpg', '*.png', '*.jpeg']


def move_images_in_dir(dir_name):
    files_grabbed = []

    for type in types:
        files_grabbed.extend(glob.glob(os.path.join(src_dir, dir_name, type)))

    for file in files_grabbed:
        dst_file = f'{dst_dir}/{dir_name}-{file.split("/")[-1]}'
        shutil.copy(file, dst_file)


if __name__ == '__main__':
    dir_names = os.listdir(src_dir)

    for dir_name in dir_names:
        move_images_in_dir(dir_name)
