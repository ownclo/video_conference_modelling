#!/bin/bash

set -e

INFILE=$1

x264 --input-res 176x144 \
    --verbose --bframes 0 --qp 5 --psnr \
    -o /dev/null $INFILE
