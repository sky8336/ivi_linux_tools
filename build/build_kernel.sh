#!/bin/bash

KERNEL=kernel/linux
kernel_out=../../out/s32v234evb/kernel/linux

# Generate default configs:
cd $KERNEL
make O=$kernel_out defconfig
make O=$kernel_out -j$(nproc)
