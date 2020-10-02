======================
imagepypelines-tools
======================

.. _ImagePypelines: `https://www.imagepypelines.org`

This repository is an accessory to the open source image and data processing
library  ImagePypelines_ and is automatically installed alongside

imagepypelines-tools can setup an interactive dashboard with which you can view
and manage your pipelines.The dashboard can be run locally or via a
containerized docker image


Install
=========
.. code-block:: shell

    pip install imagepypelines


.. 0.3.3
.. _base-0.3.3-alpha: `https://github.com/jmaggio14/imagepypelines-tools/blob/90b028647411e443d7c1b31b8a829e648826dec4/dockerfiles/imagepypelines-base.Dockerfile`
.. _gpu-0.3.3-alpha: ``https://github.com/jmaggio14/imagepypelines-tools/blob/90b028647411e443d7c1b31b8a829e648826dec4/dockerfiles/imagepypelines-gpu.Dockerfile``
    pip install imagepypelines-tools
    imagepypelines shell --gpu


Building the UI
=============

To build the ui:

1. Install NodeJS 12.X.X
2. `cd ip-client && npm i && ng build:prod`
