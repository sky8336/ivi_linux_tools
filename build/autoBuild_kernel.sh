#!/bin/bash

export ARCH=arm
export CROSS_COMPILE=/opt/arm-cross-compile/arm-none-linux-gnueabi-2014-05/bin/arm-none-linux-gnueabi-

SHELL_DIR=$(cd $(dirname ${0});pwd)
cd ${SHELL_DIR}

CPU_NUM=$(grep processor /proc/cpuinfo | awk '{field=$NF};END{print field+1}')
KERN_NAME="linux-4.8.5@xj"
TFTP_DIR=/tftp/
DTB_PATH=arch/${ARCH}/boot/dts/exynos4412-origen.dtb
DTS_PATH=arch/${ARCH}/boot/dts/exynos4412-origen.dts
ZIMAGE_PATH=arch/${ARCH}/boot/zImage

if [ "" == "$1" ];then
	make menuconfig

	#make exynos_defconfig
	make zImage -j${CPU_NUM}
	mkimage -A ${ARCH} -O linux -T kernel -C none -a 0x41000000
	-e 0x41000040 -n ${KERN_NAME} -d ${ZIMAGE_PATH} uImage
	make dtbs -j${CPU_NUM}
	cp uImage ${DTB_PATH} ${DTS_PATH} ${TFTP_DIR}
elif [ "man" == "$1" ];then
	make mandocs
	make installmandocs
else
	make "$1"
fi
