#!/usr/bin/env bash

python3 -m coverage  run --omit="/usr/*" -m unittest discover
python3 -m coverage html
firefox htmlcov/index.html