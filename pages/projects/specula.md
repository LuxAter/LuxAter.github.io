---
path: "/projects/specula"
date: "2020-03-04"
title: "Specula"
github: "https://github.com/LuxAter/Specula"
tags: [c++,graphics]
featuredImage: specula1.png
---

This ray tracer implements the basis of a ray tracing rendering engine in C++.
It is possible to render still images, or sequences of images. Multi threading
has also been implemented allowing for significantly faster render times.

[[warn]]
| A complete overhaul of the Specula rendering engine is currently in progress.
| This rewrite is focused on implementing path tracing into the renderer, and
| implementing PBR techniques.

The ability to create multiple object of *sphere*, *triangle*, *plane*,
*circle*, or *mesh* types is currently available. Where a mesh is any
collection of triangles specified by an ``.stl`` file. Thus allowing for the
import of any arbitrary model. Using these five different supported objects,
there is the possibility for the construction of all three dimensional models.

The implementation of different materials is such that the reflectively of the
material, the specular index, and the diffuse and specular colors can be
determined. Using these settings it is possible to demonstrate most opaque
materials.

There are three formats of lights implemented in the system. *Distant* lights
are lights that cast parallel rays across the entire space. They are useful for
simulations of sunlight, or large sources of light that are very far away.
*Point* lights approximate point sources. *Area* lights represent a light
source from a rectangle. This is useful for most light sources, as very few
sources of light are actual point sources, and can be better represented by
this area light source. Every light can have have a specified intensity and
color. And area light sources can specify the number of samples for calculating
the lighting. Higher number of samples improves the quality of soft shadows
produced in the final image.

The entire process is self enclosed, as the process of compilation also
compiles and links ``libpng`` in order to output ``png`` files.

The multi threading is optimized by scattering the pixels that each thread
renders, so that no single thread is solely rendering a simple set of pixels.
This proves a significantly faster rendering time. Thus allowing for the
rendering of significantly more complex systems.
