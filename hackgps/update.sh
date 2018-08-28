#!/bin/sh
mkdir -p ./hackgps/static/js
mkdir -p ./hackgps/static/css
mkdir -p ./hackgps/static/graphs
cp -a ./graphs/. hackgps/static/graphs/
find ./web/build/static/js/main\.*\.js* -exec cp {} ./hackgps/static/js/ \;
find ./web/build/static/css/main\.*\.css* -exec cp {} ./hackgps/static/css/ \;
cp -r ./web/build/static/media ./hackgps/static/
cp ./web/build/index.html ./hackgps/templates/
