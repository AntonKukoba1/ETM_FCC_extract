import os
import sys
from pathlib import Path
import xml.etree.cElementTree as ET


def main():
    if len(sys.argv) < 2:
        print("Too few arguments")
        print("Usage: main.py firmware_folder_path\n")
        print("As result you're gonna get out folder with the extracted content in the same dir as firmware folder")
        return

    folder_path = sys.argv[1]
    xml_file = os.path.join(folder_path, "ETM_FFC.xml")
    try:
        tree = ET.ElementTree(file=xml_file)
        root = tree.getroot()

        for item in root.iterfind('./MM-FFC//'):
            if item.tag == "FLASH":
                bin_file_path = os.path.join(folder_path, item.attrib['ID'] + ".bin")
                break

        with open(bin_file_path, "rb") as bin_file:
            for item in root.iterfind('./MM-FFC/FLASH//'):
                if item.tag == "DATABLOCK":
                    datablock_name = item.attrib['ID']

                    for binary_segment in item.iterfind('./BINARY-SEGMENTS//'):
                        filename = ""
                        data_start = -1
                        data_end = -1
                        for binary_segment_item in binary_segment.iterfind('.//'):
                            if binary_segment_item.tag == "SHORT-NAME":
                                filename = binary_segment_item.text
                            elif binary_segment_item.tag == "SOURCE-START-ADDRESS":
                                data_start = int(binary_segment_item.text, 16)
                            elif binary_segment_item.tag == "SOURCE-END-ADDRESS":
                                data_end = int(binary_segment_item.text, 16) + 1

                            if filename and data_start != -1 and data_end != -1:
                                data = bin_file.read(data_end - data_start)
                                output_path = os.path.join(folder_path, "out", datablock_name)
                                Path(output_path).mkdir(parents=True, exist_ok=True)
                                output_file_path = os.path.join(output_path, filename)
                                with open(output_file_path, "wb+") as output_file:
                                    output_file.write(data)
                                break

    except IOError as e:
        print ('nERROR - cant find file: %sn' % e)

if __name__ == "__main__":
    main()