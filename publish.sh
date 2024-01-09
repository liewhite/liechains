#!/bin/bash

rm -rf dist liechains.egg-info
python setup.py sdist && twine upload --skip-existing dist/*