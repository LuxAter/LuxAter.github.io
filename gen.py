#!/usr/bin/env python3

import jinja2
import os
import yaml
import markdown
import datetime
import shutil
import subprocess
import sys
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import orto.video
import orto.tab

MARKDOWN_EXTENSIONS = [
    'admonition', 'pymdownx.arithmatex', 'pymdownx.extra',
    'pymdownx.highlight', 'pymdownx.inlinehilite', 'orto.video', 'orto.tab'
]

CONFIG = {
    'FFMPEG': bool(shutil.which('ffmpeg')),
    'PYGMENTS': bool(shutil.which('pygmentize')),
    'IMAGEMAGICK': bool(shutil.which('convert')),
    'TRANSCRIBE': False
}


def tree_has_markdown(data):
    for file in data['files']:
        if file.endswith('.md') and file[:-3] != data['path'].split('/')[-1]:
            return True
    return any(
        [tree_has_markdown(data['dirs'][dirs]) for dirs in data['dirs']])


def get_file_meta(path, config, base):
    meta = {'type': path.split('.')[-1], 'path': path, **config}
    if path.endswith('.md'):
        with open(path, 'r') as markdown_file:
            lines = [x.strip('\n') for x in markdown_file.readlines()]
        if lines and lines[0] == '---':
            lines = lines[1:[i for i, v in enumerate(lines) if v == '---'][1]]
            meta = {**meta, **yaml.load('\n'.join(lines), Loader=yaml.Loader)}
    if 'img' in meta and not meta['img'].startswith('/'):
        meta['img'] = '/' + '/'.join(
            path.lstrip(base).split('/')[:-1]) + '/' + meta['img']
    if 'title' not in meta:
        meta['title'] = '.'.join(path.split('/')[-1].split('.')[:-1]).title()
    if 'date' not in meta:
        meta['date'] = datetime.date.fromtimestamp(os.path.getmtime(path))
    if 'tags' not in meta and 'url' in meta:
        meta['tags'] = {}
        meta['tags'][
            'https://img.shields.io/badge/Github-{}-blue.svg?style=for-the-badge&logo=github'
            .format(meta['title'])] = meta['url']
    if 'tab' not in meta:
        for seg in path.split('/'):
            if seg.title() in meta['tabs'].keys():
                meta['tab'] = seg.title()
                break
            elif seg.endswith(
                    '.md') and seg[:-3].title() in meta['tabs'].keys():
                meta['tab'] = seg[:-3].title()
                break
    return meta


def get_tree_data(path, config, base):
    objs = os.listdir(path)
    data = {
        'path': path[5:],
        'files': {
            x: get_file_meta(os.path.join(path, x), config, base)
            for x in objs if os.path.isfile(os.path.join(path, x))
        },
        'dirs': {
            x: get_tree_data(os.path.join(path, x), config, base)
            for x in objs if os.path.isdir(os.path.join(path, x))
        },
        **config
    }
    if os.path.exists(os.path.join(path, 'config.yaml')):
        with open(os.path.join(path, 'config.yaml'), 'r') as config_file:
            data = {**data, **yaml.load(config_file, Loader=yaml.Loader)}
    return data


def gen_config():
    config = {}
    if os.path.exists('orto.yaml'):
        with open('orto.yaml', 'r') as config_file:
            config = yaml.load(config_file, Loader=yaml.Loader)
    config['tabs'] = {}
    for file in os.listdir('./src'):
        if file.lower() in ('index.md', 'config.yaml'):
            continue
        if file.endswith('.md'):
            config['tabs'][file[:-3].title()] = file[:-3] + '.html'
        else:
            config['tabs'][
                file.title()] = file + '/' if file + '.md' not in os.listdir(
                    './src/' + file) else file + '/' + file + '.html'
    return config


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


def copy_resource(data, dest_dir, base_name):
    if data['type'] in ('mp4', 'webm'):
        copy_video(data['path'], os.path.join(base_name, dest_dir))
    elif data['type'] in ('png', 'jpeg'):
        copy_image(data['path'], os.path.join(base_name, dest_dir))
    else:
        copy_misc(data['path'], os.path.join(base_name, dest_dir))


def gen_markdown(env, data, dest_dir, base_name):
    print("\033[96mGenerating Page {}\033[0m".format(
        data['path'].split('/')[-1]))
    with open(data['path'], 'r') as markdown_file:
        lines = [x.strip('\n') for x in markdown_file.readlines()]
    if lines and lines[0] == '---':
        lines = lines[[i for i, v in enumerate(lines) if v == '---'][1] + 1:]
    lines = markdown.markdown('\n'.join(lines), extensions=MARKDOWN_EXTENSIONS)
    data['dirname'] = dest_dir.lstrip('.')
    data['filename'] = data['path'].split('/')[-1].strip('.md') + '.html'
    body_template = jinja2.Environment(
        loader=jinja2.BaseLoader).from_string(lines)
    lines = body_template.render(data)
    if data['path'].split('/')[-2].lower() == data['path'].split(
            '/')[-1][:-3].lower():
        dest = os.path.join(base_name, dest_dir) + '.html'
    else:
        dest = os.path.join(base_name, dest_dir,
                            data['path'].split('/')[-1].strip('.md') + '.html')
    data['dest'] = dest
    template_src = None
    if 'template' in data and os.path.isfile('./templates/{}'.format(
            data['template'])):
        template_src = data['template']
    elif os.path.isfile('./templates/{}.jinja2'.format(data['dirname'])):
        template_src = data['dirname'] + '.jinja2'
    elif any([
            os.path.isfile('./templates/{}.jinja2'.format(x))
            for x in data['dirname'].split('/')
    ]):
        vals = [
            os.path.isfile('./templates/{}.jinja2'.format(x))
            for x in data['dirname'].split('/')
        ]
        template_src = data['dirname'].split('/')[vals.index(True)] + '.jinja2'
    else:
        template_src = 'base.jinja2'
    template = env.get_template(template_src)
    file_data = {**data, 'body': lines.replace('<p>', '<p class="flow-text">')}
    with open(dest, 'w') as output_file:
        output_file.write(template.render(file_data))


def gen_markdown_str(data, dest_dir):
    with open(data['path'], 'r') as markdown_file:
        lines = [x.strip('\n') for x in markdown_file.readlines()]
    if lines and lines[0] == '---':
        lines = lines[[i for i, v in enumerate(lines) if v == '---'][1] + 1:]
    preface = markdown.markdown('\n'.join(lines).split('\n\n')[0],
                                extensions=MARKDOWN_EXTENSIONS).replace(
                                    '<p>', '<p class="flow-text">')
    data['dirname'] = dest_dir.lstrip('.')
    data['filename'] = data['path'].split('/')[-1].strip('.md') + '.html'
    body_template = jinja2.Environment(
        loader=jinja2.BaseLoader).from_string(preface)
    preface = body_template.render(data)
    return preface


def gen_file(env, data, dest_dir, base_name):
    if data['type'] in ('md'):
        gen_markdown(env, data, dest_dir, base_name)
    else:
        copy_resource(data, dest_dir, base_name)


def gen_tree_index(env, data, dest_dir, base_name):
    template = env.get_template('group.jinja2')
    dest = os.path.join(base_name, dest_dir, 'index.html')
    indexed = [
        {
            'title': k,
            **v
        } for k, v in data['files'].items()
        if k.rstrip('.md') != data['path'].split('/')[-1] and 'index' in v
    ]
    dated = [
        {
            'title': k,
            **v
        } for k, v in data['files'].items()
        if k.rstrip('.md') != data['path'].split('/')[-1] and 'index' not in v
    ]
    dated += [{
        'title': k,
        'subdir': True,
        **v['files'][k + '.md']
    } for k, v in data['dirs'].items() if k + '.md' in v['files']]
    data['dest'] = dest
    data['entries'] = sorted(indexed, key=lambda x: x['index'],
                             reverse=False) + sorted(
                                 dated, key=lambda x: x['date'], reverse=True)
    for entry in data['entries']:
        entry['preface'] = gen_markdown_str(entry, dest_dir)
    with open(dest, 'w') as output_file:
        output_file.write(template.render(data))


def gen_tree(env, data, base_path='.', base_name='./docs'):
    dir_path = base_path + data['path']
    if dir_path == './':
        dir_path = ''
    if not os.path.exists(os.path.join(base_name,
                                       dir_path)) or not os.path.isdir(
                                           os.path.join(base_name, dir_path)):
        os.mkdir(os.path.join(base_name, dir_path))
    if 'root' not in data and tree_has_markdown(data) and (any([
            file not in (data['path'].split('/')[-1] + ".md")
            for file in data['files']
    ]) or len(data['files'].keys()) == 0) and 'index.md' not in data['files']:
        gen_tree_index(env, data, dir_path, base_name)
    for _, subdir in data['dirs'].items():
        gen_tree(env, subdir, base_path, base_name)
    for _, file in data['files'].items():
        gen_file(env, file, dir_path, base_name)


def generate(full_gen=False):
    config = gen_config()
    data = get_tree_data('./src/', config, './src')
    data['root'] = True
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates/'),
                             lstrip_blocks=True,
                             trim_blocks=True)
    gen_tree(env, data)
    dirs = [
        f for f in os.listdir('./templates')
        if os.path.isdir(os.path.join('./templates/', f))
    ]
    for d in dirs:
        if os.path.isdir(os.path.join('./docs', d)):
            shutil.rmtree(os.path.join('./docs', d))
        shutil.copytree(os.path.join('./templates/', d),
                        os.path.join('./docs', d))
    if os.path.isdir('./favicon/'):
        for f in os.listdir('./favicon'):
            shutil.copyfile(os.path.join('./favicon', f),
                            os.path.join('./docs', os.path.basename(f)))


class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        generate(False)


def main():
    watcher = False
    full = False
    if 'full' in sys.argv or 'all' in sys.argv:
        full = True
    if 'serve' not in sys.argv:
        generate(full)
    else:
        observer = Observer()
        observer.schedule(MyHandler(), 'src/', recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


if __name__ == "__main__":
    main()
