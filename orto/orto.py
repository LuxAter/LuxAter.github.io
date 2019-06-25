#!/usr/bin/env python3

import jinja2
import os
import sys
import json
import yaml
import markdown
import datetime
import shutil
import re
import subprocess
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from pprint import pprint

import orto.video

MARKDOWN_EXTENSIONS = [
    'admonition', 'pymdownx.arithmatex', 'pymdownx.extra',
    'pymdownx.highlight', 'pymdownx.inlinehilite'
]

CONFIG = {
    'FFMPEG': bool(shutil.which('ffmpeg')),
    'PYGMENTS': bool(shutil.which('pygmentize')),
    'IMAGEMAGICK': bool(shutil.which('convert')),
    'TRANSCRIBE': False
}


def get_file_meta(path):
    meta = {'type': path.split('.')[-1], 'path': path}
    if path.endswith('.md'):
        with open(path, 'r') as markdown_file:
            lines = [x.strip('\n') for x in markdown_file.readlines()]
        if lines[0] == '---':
            lines = lines[1:[i for i, v in enumerate(lines) if v == '---'][1]]
            meta = {**meta, **yaml.load('\n'.join(lines), Loader=yaml.Loader)}
    return meta


def get_tree_data(path):
    objs = os.listdir(path)
    data = {
        'path': path[5:],
        'files': {
            x: get_file_meta(os.path.join(path, x))
            for x in objs if os.path.isfile(os.path.join(path, x))
        },
        'dirs': {
            x: get_tree_data(os.path.join(path, x))
            for x in objs if os.path.isdir(os.path.join(path, x))
        }
    }
    if os.path.exists(os.path.join(path, 'config.yaml')):
        with open(os.path.join(path, 'config.yaml'), 'r') as config_file:
            data['config'] = yaml.load(config_file, Loader=yaml.Loader)
    return data


def copy_video(src, dest):
    print("\033[96mCopying Video From {}\033[0m".format(src))
    if not CONFIG['TRANSCRIBE']:
        dest_dir = os.path.join(dest, src.split('/')[-1])
        shutil.copyfile(src, dest_dir)
        return
    dest_dir = os.path.join(dest, '.'.join(src.split('/')[-1].split('.')[:-1]))
    subprocess.run([
        'ffmpeg', '-y', '-i', src, '-vcodec', 'libx264', '-pix_fmt', 'yuv420p',
        dest_dir + '.mp4'
    ],
                   capture_output=True)
    subprocess.run([
        'ffmpeg', '-y', '-i', src, '-c:v', 'libvpx', '-crf', '10', '-b:v',
        '1M', '-c:a', 'libvorbis', dest_dir + '.webm'
    ],
                   capture_output=True)


def copy_image(src, dest):
    print("\033[96mCopying Image From {}\033[0m".format(src))
    dest_dir = os.path.join(dest, src.split('/')[-1])
    shutil.copyfile(src, dest_dir)


def copy_misc(src, dest):
    print("\033[96mCopying Resource From {}\033[0m".format(src))
    dest_dir = os.path.join(dest, src.split('/')[-1])
    shutil.copyfile(src, dest_dir)


def copy_resource(data, dest_dir):
    if data['type'] in ('mp4', 'webm'):
        copy_video(data['path'], dest_dir)
    elif data['type'] in ('png', 'jpeg'):
        copy_image(data['path'], dest_dir)
    else:
        copy_misc(data['path'], dest_dir)


def gen_file(data, dest_dir):
    if data['type'] in ('md'):
        pass
    else:
        copy_resource(data, dest_dir)


def gen_tree(data, base_path='./docs'):
    dir_path = base_path + data['path']
    if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    for _, subdir in data['dirs'].items():
        gen_tree(subdir, base_path)
    for _, file in data['files'].items():
        gen_file(file, dir_path)


def generate(full_gen=False):
    data = get_tree_data('./src/')
    gen_tree(data)
    pprint(data)


def main():
    generate()


if __name__ == "__main__":
    main()
