# Split Images

* This program splits images vertically using the following conditions:
  * The image is horizontal.
  * There is a blank space in the center of the image.

![Original image](/test.png)
![Left image](/test.png.0.png)
![Right image](/test.png.1.png)

## Requirements

* python3-wand

## Installation

### On Ubuntu

`
# apt update
# apt install -qy python3-wand
# cd /usr/local/lib/python3*/dist-packages
/usr/local/lib/python3.x/dist-packages# git clone https://github.com/koisnd/splitimages.git
`

## Usage

`
import splitimages

si = splitimages.SplitImages(["/tmp/foo", "/tmp/bar"])
si.split_images()
`
