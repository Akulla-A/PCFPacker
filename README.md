# PCF Packer

A simple python script to extract used models and texture of .pcfs ( https://developer.valvesoftware.com/wiki/PCF ) files in a folder, and output a vmf. Then, you can compile the VMF and use VIDE (https://developer.valvesoftware.com/wiki/VIDE) to get all the required contents.

#How to use
python3 script.py FOLDER_PARTICLES OUTPUT_VMF

If it doesn't work, you can give an absolute path to the script, such that:
python3 C:/.../script.py FOLDER_PARTICLES OUTPUT_VMF

A example:
python3 "f:/dev/PCFPacker/main.py" "E:\SteamLibrary\steamapps\common\GarrysMod\garrysmod\addons\akulla_content\particles" "F:\dev\output_particles.vmf"

After that, open the vmf with Hammer, compile and use VIDE to pack everything. You will need to put your particles manually afterwards in the contents to have a ready, working content.
