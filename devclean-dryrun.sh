#!/bin/bash

# Dry-run mode to estimate deletions and sizes
python3 ./devclean.py \
  --log ./out.txt \
  --path "." \
  --silent \
  --show-size \
  --dry-run
