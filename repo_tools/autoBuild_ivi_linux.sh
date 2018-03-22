#!/bin/bash

echo "auto build ivi_linux"

########################################
# Download ivi_linux source code
########################################
# ivi_linux
myrepo init -u https://github.com/sky8336/manifest.git
myrepo sync -j4

#############################
# Build the ivi_linux project
#############################
