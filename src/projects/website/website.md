---
title: Personal Website
url: https://github.com/LuxAter/LuxAter.github.io
---

This personal website, is generated using a static site generator that I have
developed. The static site generator is written in python, and uses yaml files
for the configuration, and markdown files for all of the content.

The basic file structure can be seen in the repository for this website. In
general, in the root directory, there is the templates, which define the look
for each of the webpages. and the generator script. All of the other content is
located in the `src/` directory.

Each file or folder in the ``src/`` directory will create a new tab in the
navigation bar. Then if it is a directory, it will automatically generate a
page containing cards for each subdirectory or file. Each card will contain the
first paragraph of the content for that file. This structure is recursive, so
any level of subdirectories can be created, and the generated website will
generate the neccesary index files to brows all of the files.

The markdown is rendered using the python package ``markdown``, and uses
``jinja2`` files for the html templates. The rendering can handle most markdown
components, and can also render mathmatical formuala using mathjax.

When generating the static site, the generator script will make use of
``ffmpeg`` if it is available, to convert any images and video files into
multiple different file formats, to improve the compatability across multiple
devices. This along with the Materialize css framework that is used allows the
website to be easily viewed any any device that is used.

