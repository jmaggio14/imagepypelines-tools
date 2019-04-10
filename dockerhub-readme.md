# imagepypelines-tools

This repository contains two docker images which provide a full
development environment for those doing image processing, computer
vision, or machine learning development in python.

It includes:
 * [ImagePypelines](https://www.imagepypelines.org) (obviously :p)
 * Opencv (an optimized build)
 * tensorflow
 * keras
 * Pillow
 * sklearn
 * the usual suspects (scipy, numpy, etc)

This repository is an accessory to the open source image and data processing
library [ImagePypelines](https://www.imagepypelines.org)

Quick Setup
===========

*note that GPU usage requires separate installation of Nvidia-Docker*

We provide a convenient python wrapper to easily and quickly, download, launch
and update these images

**Standard**

``` {.console}
pip install imagepypelines-tools
imagepypelines shell
```

**GPU Accelerated (limited to Linux hosts with Nvidia-Docker)**

``` {.console}
pip install imagepypelines-tools
imagepypelines shell --gpu
```

Latest
======

### Base (no GPU)

[latest](https://github.com/jmaggio14/imagepypelines-tools/blob/3c6dcd7178afa4d4ef3e5c8d497dc58815689374/imagepypelines_tools/dockerfiles/imagepypelines-base.Dockerfile),
[base-0.4.1-alpha](https://github.com/jmaggio14/imagepypelines-tools/blob/3c6dcd7178afa4d4ef3e5c8d497dc58815689374/imagepypelines_tools/dockerfiles/imagepypelines-base.Dockerfile)

### GPU

[latest-gpu](https://github.com/jmaggio14/imagepypelines-tools/blob/3c6dcd7178afa4d4ef3e5c8d497dc58815689374/imagepypelines_tools/dockerfiles/imagepypelines-gpu.Dockerfile),
[gpu-0.4.1-alpha](https://github.com/jmaggio14/imagepypelines-tools/blob/3c6dcd7178afa4d4ef3e5c8d497dc58815689374/imagepypelines_tools/dockerfiles/imagepypelines-gpu.Dockerfile)

Older Releases
--------------

[gpu-0.4.0-alpha](https://github.com/jmaggio14/imagepypelines-tools/blob/5a351d31a39b1d0af294ea5d968d9385e1ac23ce/imagepypelines_tools/dockerfiles/imagepypelines-gpu.Dockerfile),
[base-0.4.0-alpha](https://github.com/jmaggio14/imagepypelines-tools/blob/5a351d31a39b1d0af294ea5d968d9385e1ac23ce/imagepypelines_tools/dockerfiles/imagepypelines-base.Dockerfile)

[gpu-0.3.3-alpha](https://github.com/jmaggio14/imagepypelines-tools/blob/90b028647411e443d7c1b31b8a829e648826dec4/dockerfiles/imagepypelines-gpu.Dockerfile),
[base-0.3.3-alpha](https://github.com/jmaggio14/imagepypelines-tools/blob/90b028647411e443d7c1b31b8a829e648826dec4/dockerfiles/imagepypelines-base.Dockerfile)
