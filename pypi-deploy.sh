python -m build
tar -xf dist/evdev3_utilities-0.1.0.tar.gz
cat evdev3_utilities-0.1.0/PKG-INFO | grep License
twine upload dist/*