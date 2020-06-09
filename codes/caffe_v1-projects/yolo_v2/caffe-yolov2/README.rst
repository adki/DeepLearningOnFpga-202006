|Python27|

.. |Python27| image:: https://img.shields.io/badge/python-2.7-blue.svg
    :target: https://www.python.org/

==========
Caffe-YOLO
==========

Introduction
============

This is a set of tools to convert models from 
`Darknet <http://pjreddie.com/darknet/yolov1/>`_ to 
`Caffe <https://github.com/BVLC/caffe>`_, and in
particular to convert the YOLO networks for object detection. For more details,
see the paper:

    *"You Only Look Once: Unified, Real-Time Object Detection"*
    [`Redmon2015 <https://arxiv.org/abs/1506.02640>`_]


Usage
=====

The repository includes a tool to convert the Darknet configuration file ``.cfg``
to the ``.prototxt`` definition in Caffe, a tool to convert the weight
file ``.weights`` to ``.caffemodel`` in Caffe and a detection demo to test the 
converted networks.

Convert the configuration file with:

.. code:: bash

    python create_yolo_prototxt.py tiny-yolo.cfg yolo_tiny

By default, only the *deploy* prototxt is generate. If the ``--train`` option is
passed, the *train_val* version of the prototxt file is generated; however, the
file lacks the information about input annotations, training loss and it's meant
as a form of partial automation of a manually defined training.

The YOLO weights are available on the `YOLO <https://pjreddie.com/darknet/yolo/>`_
and `YOLO v1 <http://pjreddie.com/darknet/yolov1/>`_
websites.
See the instructions there on how to download the weight files.
To convert them to Caffe, use:

.. code:: bash

    python create_yolo_caffemodel.py yolo_tiny_deploy.prototxt tiny-yolo.weights \
           yolo_tiny.caffemodel

If the number of weights is not compatible with the given prototxt, an error is
returned.

Test the results on one of the images in the repository with:

.. code:: bash

    python yolo_detect.py yolo_tiny_deploy.prototxt yolo_tiny.caffemodel images/dog.jpg

By default, the presets for the *CoCo* networks are used. To use the `Pascal VOC`
preset pass ``--mode voc`` option in order to use the correct set of class labels.
Classification is also supported for the `Darknet` networks: use ``--mode darknet``
to enable it.


Limitations
^^^^^^^^^^^

The process only supports a limited number of layers and options. The *detection*
layer in YOLO is not implemented and parsing of the network output is left to
the caller application.

The most recent ``yolo`` and ``yolo-coco`` models in Darknet v1 use the *Local
Convolution* layer (convolutions without weight sharing) which is not supported
by the official Caffe repository. There is partial support to the version in
`caffe-mt <https://github.com/knsong/caffe-mt>`_ by passing ``--loclayer`` to 
``create_yolo_prototxt.py`` but the implementation is still buggy.

The shortcut connections introduced in the Darknet v2 YOLO models are also not
supported.


Model files
===========

Two models converted from YOLO v2 are available in the ``prototxt`` directory:

* **YOLO tiny** (CoCo): converted from ``tiny-yolo.cfg``,
  `caffemodel <https://drive.google.com/open?id=0Bx7QZuu7oVBbNEt5YmUzRGNXZlk>`__.

* **YOLO tiny VOC**: converted from ``tiny-yolo-voc.cfg``,
  `caffemodel <https://drive.google.com/open?id=0Bx7QZuu7oVBbSEdpaDBGMVFIVk0>`__.

* **Darknet** (Imagenet 1k): converted from ``darknet.cfg``,
  `caffemodel <https://drive.google.com/open?id=0Bx7QZuu7oVBbU19ZdU5neFl0T1k>`__.

* **Tiny Darknet** (Imagenet 1k): converted from ``tiny.cfg``,
  `caffemodel <https://drive.google.com/open?id=0Bx7QZuu7oVBbRUxyRk9NOFRueGM>`_


Legacy models
^^^^^^^^^^^^^

Three converted models from YOLO v1 are available in the ``prototxt/v1`` directory:

* **YOLO tiny**: converted from ``yolov1/tiny-yolo.cfg``, 
  `caffemodel <https://drive.google.com/file/d/0Bx7QZuu7oVBbLVktdDJEQ3FZTEk/view?usp=sharing>`__.

* **YOLO small**: converted from ``yolov1/yolo-small.cfg``,
  `caffemodel <https://drive.google.com/file/d/0Bx7QZuu7oVBbVVJaVzh2WV9CR28/view?usp=sharing>`__.

* **YOLO CoCo tiny**: converted from ``yolov1/tiny-coco.cfg``,
  `caffemodel <https://drive.google.com/file/d/0Bx7QZuu7oVBbcWRpVG9NNl9EanM/view?usp=sharing>`__.

The models originally converted by *xingwangsfu* (https://github.com/xingwangsfu/caffe-yolo)
are available in the directory ``prototxt/legacy``. The converted weights can
be downloaded here:

* **YOLO**: https://drive.google.com/file/d/0Bzy9LxvTYIgKMXdqS29HWGNLdGM/view?usp=sharing

* **YOLO small**: https://drive.google.com/file/d/0Bzy9LxvTYIgKa3ZHbnZPLUo0eWs/view?usp=sharing

* **YOLO tiny**: https://drive.google.com/file/d/0Bzy9LxvTYIgKNFEzOEdaZ3U0Nms/view?usp=sharing


Requirements
============

   * `Caffe <http://caffe.berkeleyvision.org>`__ with ``pycaffe`` support

   * OpenCV 2 with python interfaces (``python-opencv`` in Ubuntu)


License
=======
 
The code is released under the YOLO license.
