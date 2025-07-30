#!/bin/bash

# Actual cleanup with confirmation disabled
python3 ./devclean.py \
  --log ./out.txt \
  --path "." \
  --silent \
  --show-size \
  --force
