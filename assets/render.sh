#!/bin/bash

mkdir -p ./png

for f in ./svg/*.xml
do
  convert -background none -trim  -density 800 -resize 800x800 $f png/$(basename $f .xml).png
done


