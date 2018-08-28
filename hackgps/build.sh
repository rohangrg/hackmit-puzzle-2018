#!/bin/sh
cd web
npm run build
npm run build-css
cd ..
./clean.sh
./update.sh