#!/bin/bash

set -e

for f in $(ls qcif_yuv/*.yuv)
do
    ./trace_h264.sh $f 2> trace_h264/`basename ${f%.yuv}.trace`
done
