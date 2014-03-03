#!/bin/sh

HERE=`pwd`;
cd ..;
export PYTHONPATH=`pwd`:$PYTHONPATH;
cd $HERE;