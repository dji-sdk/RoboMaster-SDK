mkdir _build_tmp
cd _build_tmp
cmake ../src
make -j4
cd ..
rm -rf _build_tmp
