#!/bin/bash

# Add project root to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the crews
python crews/run_all_crews.py 