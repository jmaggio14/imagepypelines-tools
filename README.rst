======================
imagepypelines-tools
======================

.. _ImagePypelines: `https://github.com/jmaggio14/imagepypelines`

This repository contains two docker images which provide a full development
environment for those doing image processing, computer vision, or machine
learning development in python.

It includes:
    - imagepypelines (obviously :p)
    - Opencv (an optimized build)
    - tensorflow
    - keras
    - Pillow
    - sklearn
    - the usual suspects (scipy, numpy, etc)



This repository is an accessory to the open source image and data ImagePypelines_


*note that GPU usage requires separate installation of Nvidia-Docker*

These images are built to work in tandem with the pip package imagepypelines-tools.
To enter this docker environment simply:

.. code-block:: console

    pip install imagepypelines
    imagepypelines shell


--------------------
imagepypelines shell
--------------------

Standard

.. code-block:: console

    pip install imagepypelines-tools
    imagepypelines shell

GPU Accelerated (limited to Linux hosts with Nvidia-Docker)

.. code-block:: console

    pip install imagepypelines-tools
    imagepypelines shell --gpu
