# ETM FCC extractor

## The python script for Alfa Romeo Giorgio Head Unit firmwares

It's capable to extract Alfa Rome Guilia/Stelvio firmwares gen1 to gen3. Yet it will not work with gen3_my20 since the content is encrypted there.

Usage:

main.py firmware_folder_path

The firmware is expected to be a folder where ETM_FFC.xml and bin file is situated.

The result is the folder called "out". It will contain the individual pieces of the firmware which are stored in swfl subdirectories. 