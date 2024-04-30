#!/usr/bin/python3

import argparse
import splitimages

ap = argparse.ArgumentParser()
ap.add_argument("target_dirs", nargs='*', default=[])
pa = ap.parse_args()

si = splitimages.SplitImages(pa.target_dirs)
si.split_images()
