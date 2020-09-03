#!/usr/bin/env bash

tar -czf word-frequencies.tgz data
zip word-frequencies.zip $(find data)
