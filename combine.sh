#!/bin/sh

[ "$1" = "" ] && exit 1
[ -f "$1" ] && exit 1

project_dir=$(pwd)
temp_dir=$(mktemp -d)
cp berad.py "${temp_dir}/__main__.py"
cp m3u.py audio.py browser.py "${temp_dir}/"

cd "$temp_dir" || exit 1
zip -r "${project_dir}/$1.zip" *

cd "$project_dir" || exit 1
echo '#!/usr/bin/env python3' | cat - "$1".zip > "$1".py
chmod a+x "$1".py
rm "$1".zip
