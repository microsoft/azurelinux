#!/bin/bash

# output = tensorboard-$TB_VERSION.tar.gz
# Tensorboard version to use
TB_VERSION="2.16.2"

docker build --build-arg TB_VERSION=$TB_VERSION -t tensorboard .

CONTAINER_ID=$(docker run -d tensorboard)

docker cp $CONTAINER_ID:/root/tensorboard-$TB_VERSION.tar.gz $PWD

docker stop $CONTAINER_ID
docker rm $CONTAINER_ID
