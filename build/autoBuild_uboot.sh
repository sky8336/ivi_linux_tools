#!/bin/bash

# copy this script into ivi_linux root dir, then run it
cd bootloader/u-boot
make O=../../out/s32v234evb/bootloader/u-boot s32v234evb_defconfig
make O=../../out/s32v234evb/bootloader/u-boot -j4
