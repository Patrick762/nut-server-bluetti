#!/bin/sh

# Execute unittests inside docker
sudo docker build --progress=plain -t nut-server-bluetti-tests -f Dockerfile.test .
