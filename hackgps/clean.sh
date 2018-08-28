#!/bin/sh
rm -rf ./hackgps/static/graphs/
find ./hackgps/static/js/main.*.js* -exec rm {} \;
find ./hackgps/static/css/main.*.css* -exec rm {} \;
rm -rf ./hackgps/static/media
rm ./hackgps/templates/index.html