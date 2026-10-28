#!/bin/sh
# Build libyaml as a static library, so that the extension module links it in and the wheels
# do not depend on a system libyaml.
#
# Usage: build-libyaml.sh <archive> <prefix>
set -eu

archive=$1
prefix=$2

build_dir=$(mktemp -d)
tar -xzf "$archive" -C "$build_dir" --strip-components=1
cd "$build_dir"
./configure --prefix="$prefix" --disable-shared --enable-static --with-pic
make -j4
make install
