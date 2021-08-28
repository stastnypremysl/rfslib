#!/bin/bash

venv=$(mktemp -d)
main_repo=$(dirname $0)/..

pip install virtualenv
virtualenv $venv
trap "rm -rf $venv" EXIT

source $venv/bin/activate

pip install -U pip
pip install -r $main_repo/requirements.txt
pip install $main_repo

(
  cd $main_repo/docs
  make latexpdf
)

(
  readme=$main_repo/docs/_build/README.md
  cat >$readme << EOF

# rfslib documentation
This is automatically generated documentation of [rfslib](https://git.profinit.eu/rfs/rfslib).
## rfslib developer documentation
The developer documentation is in file [rfslib-dev-doc.pdf](./rfslib-dev-doc.pdf).

EOF

)


