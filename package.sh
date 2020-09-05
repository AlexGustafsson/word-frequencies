#!/usr/bin/env bash

# Swedish
python3 -m scripts.processing.download -l sv
python3 -m scripts.processing.clean -l sv
python3 -m scripts.processing.compile -l sv
python3 -m scripts.processing.count -l sv
python3 -m scripts.processing.ngram -l sv -n 3
python3 -m scripts.processing.ngram -l sv -n 2

# The compiled source is not included due to potential licensing issues

tar -czf frequency-data.tgz $(find frequency-data/compiled -type f -not -iname "compiled.txt")
zip frequency-data.zip $(find frequency-data/compiled -type f -not -iname "compiled.txt")
