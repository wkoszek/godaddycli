#!/bin/sh

# Some stuff is based on:
# https://gist.github.com/audreyr/5990987

if [ "x$1" = "x-t" ]; then
	MODE="test"
else
	MODE=""
fi

echo "# Will build and register to PyPi: $MODE"

(
	cd godaddycli/
	python setup.py register -r pypi${MODE}
	python setup.py sdist upload -r pypi${MODE}
)
