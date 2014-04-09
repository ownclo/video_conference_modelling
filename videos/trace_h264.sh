#!/bin/bash

set -e

INFILE=$1

x264 --input-res 176x144 \
    --min-keyint 10000 \
    --verbose --bframes 0 --qp 5 --psnr \
    -o /dev/null $INFILE
