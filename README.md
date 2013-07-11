DeMagicEye
==========

Reverse's magic eye images into depth maps. 


Installation
============

How to install SimpleCV on Ubuntu

    sudo apt-get install ipython python-opencv python-scipy python-numpy python-pygame python-setuptools python-pip 
    sudo pip install https://github.com/sightmachine/SimpleCV/zipball/develop


Usage
=====

To create a depth map from an autostereogram, simply pass it as an argument the DeMagicEye.py script, along with a file name stub for output

    python DeMagicEye.py autostereograms/face.gif face_output

You will see the output images generated in the working directory

