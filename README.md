# PCF Packer

A simple python script to extract used models and texture of .pcfs ( https://developer.valvesoftware.com/wiki/PCF ) files in a folder, and output a vmf. You can then compile the VMF and use VIDE (https://developer.valvesoftware.com/wiki/VIDE) to get all the required content.

# How to use
python3 script.py <PCF_FOLDER> <OUTPUT.vmf|.txt>

If it doesn't work, you can give an absolute path to the script, such that:
python3 C:/.../script.py FOLDER_PARTICLES OUTPUT_VMF

An example:
python3 "f:/dev/PCFPacker/main.py" "E:\SteamLibrary\steamapps\common\GarrysMod\garrysmod\addons\akulla_content\particles" "F:\dev\output_particles.vmf"

If your output path ends with ".txt", it will write the list of models and textures rather than a vmf.

Then, compile the vmf, pack it with VIDE and extract the packed content somewhere. You will need to put your particles manually afterward in the contents to have ready, working content.
