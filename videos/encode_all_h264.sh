#!/bin/bash

set -e

for f in $(ls qcif_yuv/*.yuv)
do
    ./encode_h264.sh $f mp4_h264/`basename ${f%.yuv}.mp4`
done
