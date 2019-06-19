#!/usr/bin/env python3

import jinja2
import os
import json
import yaml
import markdown
import datetime
import shutil
import re

from pprint import pprint

MARKDOWN_EXTENSIONS = [
    'admonition', 'pymdownx.arithmatex', 'pymdownx.extra', 'pymdownx.highlight',
    'pymdownx.inlinehilite'
]


def gen_tabs(block):
    if block.strip().startswith('<p><img'):
        block = block[4:-5].split('\n')
        return '<div class="carousel">{}</div>'.format('\n'.join([
            '<a class="carousel-item" href="#{}!">{}</a>'.format(i, img.replace('class="responsive-img"', ''))
            for i, img in enumerate(block)
        ]))
    else:
        block = [(x.strip()[3:] if x.strip().startswith('<p>') else
                  (x.strip()[:-4] if x.strip().endswith('</p>') else x.strip()))
                 for x in block.split('</p>\n<p>')]
        data = {
            v.split('\n')[0].strip():
            '<p>{}</p>'.format('\n'.join(v.split('\n')[1:])) for v in block
        }
        tabs = [
            '<li class="tab col s3"><a href="#{}" class="blue-text">{}</a></li>'
            .format(x.lower(), x) for x in data.keys()
        ]
        divs = [
            '<div id="{}" class="col s12">{}</div>'.format(k.lower(), v)
            for k, v in data.items()
        ]
        return '<div class="row container"><div class="col s12"><ul class="tabs">{}</ul></div>{}</div>'.format(
            '\n'.join(tabs), '\n'.join(divs))


def apply_classes(html):
    html = html.replace('<img ', '<img class="responsive-img" ')
    if '<p>%%%</p>' in html:
        matches = re.findall('<p>%%%</p>(.*?)<p>%%%</p>', html, flags=re.DOTALL)
        for match in matches:
            html = re.sub('<p>%%%</p>(.*?)<p>%%%</p>',
                          'TAB_BLOCK_DATA',
                          html,
                          count=1,
                          flags=re.DOTALL)
            html = html.replace('TAB_BLOCK_DATA', gen_tabs(match))
    html = re.sub(
        '<img ( *alt="([^"]*)")? *src="([^\.]*)\.mp4"( *title="([^"]*)")? */>',
        '<video class="responsive-video" controls \g<2>><source src="/\g<3>.mp4" type="video/mp4"><source src="/\g<3>.webm" type="video/webm">Your browser does not support MP4 video.</video>',
        html)
    html = html.replace('<p>', '<p class="flow-text">')
    return html


def load_markdown(src, base, tab=None):
    data = {
        'path': src,
        'tab': 'p:' + src.split('/')[-1].strip('.md') if tab is None else tab,
        'type': 'page',
        **base
    }
    with open(src, 'r') as src_file:
        source = [x.strip('\n') for x in src_file.readlines()]
    if source[0] == '---':
        prefix = source[1:[i for i, v in enumerate(source) if v == '---'][1]]
        data = {**data, **yaml.load('\n'.join(prefix), Loader=yaml.SafeLoader)}
        source = source[[i for i, v in enumerate(source) if v == '---'][1] + 1:]
    source = '\n'.join(source)
    data['body'] = apply_classes(
        markdown.markdown(source, extensions=MARKDOWN_EXTENSIONS))
    data['preface'] = apply_classes(
        markdown.markdown(source.strip().split('\n\n')[0].strip(),
                          extensions=MARKDOWN_EXTENSIONS))
    if 'date' not in data:
        data['date'] = datetime.date.fromtimestamp(os.path.getmtime(src))
    if 'badges' not in data:
        data['badges'] = ['github', 'github-size']
    if 'title' not in data:
        data['title'] = src.split('/')[-1].strip(".md").title()
    return data


def load_dir(src, base):
    data = {
        'path': src,
        'tab': 'g:' + src.split('/')[-1].strip('/'),
        'type': 'dir',
        **base
    }
    data['entrySource'] = os.listdir(src)
    data['entries'] = []
    for path in data['entrySource']:
        data['entries'].append(
            load_markdown(src + '/' + path, base, data['tab']))
    return data


def load_data():
    data = {}
    with open('./config.json', 'r') as config:
        data = json.load(config)
    pages = sorted(os.listdir('./src/'))
    data['tabs'] = [
        'p:' + x[:-3] if x.endswith('.md') else 'g:' + x for x in pages
    ]
    base = dict(data)
    data['pages'] = {}
    for page in pages:
        if os.path.isdir('./src/' + page):
            data['pages'][page] = load_dir('./src/' + page, base)
        else:
            data['pages'][page.strip('.md')] = load_markdown(
                './src/' + page, base)
    return data


def render_page(env, data):
    template_src = "base.jinja2"
    if 'template' in data and os.path.isfile('./templates/{}'.format(
            data['template'])):
        template_src = data['template']
    template = env.get_template(template_src)
    with open("docs/{}.html".format(data['tab'][2:]), "w") as file:
        file.write(template.render(data))


def render_group_index(env, data):
    template_src = "group.jinja2"
    template = env.get_template(template_src)
    if not os.path.exists('docs/{}'.format(data['tab'][2:])):
        os.mkdir('docs/{}'.format(data['tab'][2:]))
    with open("docs/{}/index.html".format(data['tab'][2:]), "w") as file:
        file.write(template.render(data))


def render_group_page(env, data):
    template_src = "base.jinja2" if not os.path.isfile(
        'templates/{}.jinja2'.format(data['tab'][2:])) else '{}.jinja2'.format(
            data['tab'][2:])
    if 'template' in data and os.path.isfile('./templates/{}'.format(
            data['template'])):
        template_src = data['template']
    template = env.get_template(template_src)
    with open("docs/{}/{}.html".format(data['tab'][2:], data['title'].lower()),
              "w") as file:
        file.write(template.render(data))


def render_group(env, data):
    has_index = True if [
        x for x in data['entries'] if x['path'].endswith('index')
    ] else False
    render_group_index(env, data)
    for entry in data['entries']:
        render_group_page(env, entry)


def main():
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates/'),
                             lstrip_blocks=True,
                             trim_blocks=True)
    data = load_data()
    if not os.path.exists('docs'):
        os.mkdir('docs')
    if os.path.exists('img'):
        if os.path.exists('docs/img'):
            shutil.rmtree('docs/img')
        shutil.copytree('img', 'docs/img')
    if os.path.exists('css'):
        if os.path.exists('docs/css'):
            shutil.rmtree('docs/css')
        shutil.copytree('css', 'docs/css')
    if os.path.exists('js'):
        if os.path.exists('docs/js'):
            shutil.rmtree('docs/js')
        shutil.copytree('js', 'docs/js')
    for page in data['pages']:
        if data['pages'][page]['path'].endswith('.md'):
            render_page(env, data['pages'][page])
        else:
            render_group(env, data['pages'][page])


if __name__ == "__main__":
    main()
