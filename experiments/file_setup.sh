#! /bin/bash

# Create test files.
dd if=/dev/zero of=small.dat bs=6M count=1
dd if=/dev/zero of=medium.dat bs=30M count=1
dd if=/dev/zero of=large.dat bs=130M count=1