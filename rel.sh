#!/bin/sh

#
# https://gist.github.com/audreyr/5990987
#

(
	cd godaddycli/
	python setup.py sdist
	python setup.py test
	python setup.py upload
)

