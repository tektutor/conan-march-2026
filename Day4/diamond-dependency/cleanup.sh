#/bin/bash

rm -rf build CMakeUserPresets.json
cd libA
rm -rf build CMakeUserPresets.json
cd ../libB
rm -rf build CMakeUserPresets.json
cd ../logger/v1
rm -rf build CMakeUserPresets.json
cd ../v2
rm -rf build CMakeUserPresets.json
cd ../..


