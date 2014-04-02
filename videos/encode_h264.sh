#!/bin/bash

set -e

INFILE=$1
OUTFILE=$2

x264 --input-res 176x144 -o $OUTFILE $INFILE
