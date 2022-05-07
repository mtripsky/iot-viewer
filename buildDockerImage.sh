#!/bin/bash
VERSION="0.1.0"
ARCH1="arm32v7"
ARCH2="arm64"
APP="iot-viewer"

docker buildx build -f ./Dockerfile-$ARCH1 -t $APP-$ARCH1:$VERSION . --load
docker tag $APP-$ARCH1:$VERSION mtripsky/$APP-$ARCH1:$VERSION
docker push mtripsky/$APP-$ARCH1:$VERSION

docker buildx build -f ./Dockerfile-$ARCH2 -t $APP-$ARCH2:$VERSION . --load
docker tag $APP-$ARCH2:$VERSION mtripsky/$APP-$ARCH2:$VERSION
docker push mtripsky/$APP-$ARCH2:$VERSION