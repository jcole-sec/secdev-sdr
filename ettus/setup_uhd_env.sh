#!/bin/bash
# UHD Environment Setup Script
# Run this before using UHD utilities to ensure proper image directory

export UHD_IMAGES_DIR=/usr/share/uhd/4.9.0/images

echo "UHD environment configured:"
echo "UHD_IMAGES_DIR = $UHD_IMAGES_DIR"
echo ""
echo "Available USRP devices:"
uhd_find_devices