import re
import os
import argparse

reg = re.compile(r'[\x20-\x7E]+?\.(?:mdl|vmt)', re.IGNORECASE)

def pcfFileToContentList(pcfFile):
    """
    Reads a PCF file and returns a dictionary with the contents.
    """
    contentList = []

    with open(pcfFile, 'r', encoding='latin-1') as f:
        # Jump first line, this is a header
        next(f)
        for idx, line in enumerate(f, start=2):
            for match in reg.findall(line):
                n = match.strip().replace("\\", "/")
                contentList.append(n)

    return contentList

def getPCFs(input_dir):
    # Scan files in the dir
    contentList = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.pcf'):
                pcfFile = os.path.join(root, file)
                contentList += pcfFileToContentList(pcfFile)

    return contentList

idx = 0
def generateBrushData(tex):
    global idx
    idx += 1

    x = idx % 128
    y = idx // 128
    dx = x * 4
    dy = y * 4

    def shift_plane(plane_str):
        parts = plane_str.strip("()").split()
        coords = [float(parts[i]) for i in range(3)]
        coords[0] += dx
        coords[1] += dy
        return f'({coords[0]:.6f} {coords[1]:.6f} {coords[2]:.6f})'

    base_planes = [
        ("0 4 4", "4 4 4", "4 0 4"),
        ("0 0 0", "4 0 0", "4 4 0"),
        ("0 4 4", "0 0 4", "0 0 0"),
        ("4 4 0", "4 0 0", "4 0 4"),
        ("4 4 4", "0 4 4", "0 4 0"),
        ("4 0 0", "0 0 0", "0 0 4"),
    ]

    sides = []
    for plane_pts in base_planes:
        p1, p2, p3 = plane_pts
        sides.append(f'''
        side
        {{
            "plane" "{shift_plane(p1)} {shift_plane(p2)} {shift_plane(p3)}"
            vertices_plus
            {{
                "v" "{shift_plane(p1)}"
                "v" "{shift_plane(p2)}"
                "v" "{shift_plane(p3)}"
                "v" "{shift_plane(p1).replace(str(float(p1.split()[1])+dy), str(float(p1.split()[1])+dy-4)) if False else shift_plane(p1)}"
            }}
            "material" "{tex.replace(".vmt", "")}"
        }}''')

    brush = "solid\n{\n" + "\n".join(sides) + "\n}\n"
    return brush

def generateModelsData(model):
    return """
entity
{
	"id" "4"
	"classname" "prop_dynamic"
	"model" "models/MODEL_REPLACE"
	"origin" "0 0 0"
}""".replace("MODEL_REPLACE", model)

def writeVMF(textures, models, path):
    # Map textures with the function
    with open(path, 'w', encoding='utf-8') as f:
        texturesMapped = list(map(generateBrushData, textures))
        modelsMapped = list(map(generateModelsData, models))
        vmfFile = """versioninfo
    {
        "editorversion" "400"
        "editorbuild" "8869"
        "mapversion" "5"
        "formatversion" "100"
        "prefab" "0"
    }
    world
    {
        NODRAW_HOLD
        TEXTURES_REPLACE
    }
    entity
    {
        "classname" "info_player_start"
        "origin" "1504 768 -1690.92"
    }
    ENTITY_REPLACE
    """.replace("TEXTURES_REPLACE", "\n".join(texturesMapped)).replace("ENTITY_REPLACE", "\n".join(modelsMapped))
        
        # Disgusting place to put it, but I'm too bored to do it properly
        vmfFile = vmfFile.replace("NODRAW_HOLD", """
    solid
        {
            "id" "3791"
            side
            {
                "id" "22554"
                "plane" "(-2496 3008 1728) (5760 3008 1728) (5760 -5888 1728)"
                vertices_plus
                {
                    "v" "-2496 -5888 1728"
                    "v" "-2496 3008 1728"
                    "v" "5760 3008 1728"
                    "v" "5760 -5888 1728"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
            side
            {
                "id" "22553"
                "plane" "(-2496 3008 1728) (-2496 -5888 1728) (-2496 -5888 -1723.92)"
                vertices_plus
                {
                    "v" "-2496 3008 1696"
                    "v" "-2496 3008 1728"
                    "v" "-2496 -5888 1728"
                    "v" "-2496 -5888 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
            side
            {
                "id" "22552"
                "plane" "(5760 3008 -1723.92) (5760 -5888 -1723.92) (5760 -5888 1728)"
                vertices_plus
                {
                    "v" "5760 -5888 1696"
                    "v" "5760 -5888 1728"
                    "v" "5760 3008 1728"
                    "v" "5760 3008 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
            side
            {
                "id" "22551"
                "plane" "(5760 3008 1728) (-2496 3008 1728) (-2496 3008 -1723.92)"
                vertices_plus
                {
                    "v" "5760 3008 1696"
                    "v" "5760 3008 1728"
                    "v" "-2496 3008 1728"
                    "v" "-2496 3008 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
            side
            {
                "id" "22550"
                "plane" "(5760 -5888 -1723.92) (-2496 -5888 -1723.92) (-2496 -5888 1728)"
                vertices_plus
                {
                    "v" "-2496 -5888 1696"
                    "v" "-2496 -5888 1728"
                    "v" "5760 -5888 1728"
                    "v" "5760 -5888 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
            side
            {
                "id" "22549"
                "plane" "(5728 -5856 1696) (5728 2976 1696) (-2464 2976 1696)"
                vertices_plus
                {
                    "v" "-2496 3008 1696"
                    "v" "-2496 -5888 1696"
                    "v" "5760 -5888 1696"
                    "v" "5760 3008 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
        }
        solid
        {
            "id" "3793"
            side
            {
                "id" "22560"
                "plane" "(-2496 -5888 -1723.92) (5760 -5888 -1723.92) (5760 3008 -1723.92)"
                vertices_plus
                {
                    "v" "-2496 3008 -1723.92"
                    "v" "-2496 -5888 -1723.92"
                    "v" "5760 -5888 -1723.92"
                    "v" "5760 3008 -1723.92"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
            side
            {
                "id" "22559"
                "plane" "(-2496 3008 1728) (-2496 -5888 1728) (-2496 -5888 -1723.92)"
                vertices_plus
                {
                    "v" "-2496 -5888 -1691.92"
                    "v" "-2496 -5888 -1723.92"
                    "v" "-2496 3008 -1723.92"
                    "v" "-2496 3008 -1691.92"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
            side
            {
                "id" "22558"
                "plane" "(5760 3008 -1723.92) (5760 -5888 -1723.92) (5760 -5888 1728)"
                vertices_plus
                {
                    "v" "5760 3008 -1691.92"
                    "v" "5760 3008 -1723.92"
                    "v" "5760 -5888 -1723.92"
                    "v" "5760 -5888 -1691.92"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
            side
            {
                "id" "22557"
                "plane" "(5760 3008 1728) (-2496 3008 1728) (-2496 3008 -1723.92)"
                vertices_plus
                {
                    "v" "-2496 3008 -1691.92"
                    "v" "-2496 3008 -1723.92"
                    "v" "5760 3008 -1723.92"
                    "v" "5760 3008 -1691.92"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
            side
            {
                "id" "22556"
                "plane" "(5760 -5888 -1723.92) (-2496 -5888 -1723.92) (-2496 -5888 1728)"
                vertices_plus
                {
                    "v" "5760 -5888 -1691.92"
                    "v" "5760 -5888 -1723.92"
                    "v" "-2496 -5888 -1723.92"
                    "v" "-2496 -5888 -1691.92"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
            side
            {
                "id" "22555"
                "plane" "(5728 2976 -1691.92) (5728 -5856 -1691.92) (-2464 -5856 -1691.92)"
                vertices_plus
                {
                    "v" "-2496 -5888 -1691.92"
                    "v" "-2496 3008 -1691.92"
                    "v" "5760 3008 -1691.92"
                    "v" "5760 -5888 -1691.92"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }

        }
        solid
        {
            "id" "3795"
            side
            {
                "id" "22566"
                "plane" "(-2496 3008 1728) (-2496 -5888 1728) (-2496 -5888 -1723.92)"
                vertices_plus
                {
                    "v" "-2496 -5888 1696"
                    "v" "-2496 -5888 -1691.92"
                    "v" "-2496 3008 -1691.92"
                    "v" "-2496 3008 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
            side
            {
                "id" "22565"
                "plane" "(5760 3008 1728) (-2496 3008 1728) (-2496 3008 -1723.92)"
                vertices_plus
                {
                    "v" "-2496 3008 1696"
                    "v" "-2496 3008 -1691.92"
                    "v" "-2464 3008 -1691.92"
                    "v" "-2464 3008 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
            side
            {
                "id" "22564"
                "plane" "(5760 -5888 -1723.92) (-2496 -5888 -1723.92) (-2496 -5888 1728)"
                vertices_plus
                {
                    "v" "-2464 -5888 -1691.92"
                    "v" "-2496 -5888 -1691.92"
                    "v" "-2496 -5888 1696"
                    "v" "-2464 -5888 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
            side
            {
                "id" "22563"
                "plane" "(-2464 2976 1696) (5728 2976 1696) (5728 -5856 1696)"
                vertices_plus
                {
                    "v" "-2496 -5888 1696"
                    "v" "-2496 3008 1696"
                    "v" "-2464 3008 1696"
                    "v" "-2464 -5888 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
            side
            {
                "id" "22562"
                "plane" "(-2464 -5856 -1691.92) (5728 -5856 -1691.92) (5728 2976 -1691.92)"
                vertices_plus
                {
                    "v" "-2496 3008 -1691.92"
                    "v" "-2496 -5888 -1691.92"
                    "v" "-2464 -5888 -1691.92"
                    "v" "-2464 3008 -1691.92"
                }
                "material" "TOOLS/TOOLSNODRAW"

            }
            side
            {
                "id" "22561"
                "plane" "(-2464 -5856 -1691.92) (-2464 -5856 1696) (-2464 2976 1696)"
                vertices_plus
                {
                    "v" "-2464 3008 1696"
                    "v" "-2464 3008 -1691.92"
                    "v" "-2464 -5888 -1691.92"
                    "v" "-2464 -5888 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"

            }

        }
        solid
        {
            "id" "3797"
            side
            {
                "id" "22572"
                "plane" "(5760 3008 -1723.92) (5760 -5888 -1723.92) (5760 -5888 1728)"
                vertices_plus
                {
                    "v" "5760 3008 1696"
                    "v" "5760 3008 -1691.92"
                    "v" "5760 -5888 -1691.92"
                    "v" "5760 -5888 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"

            }
            side
            {
                "id" "22571"
                "plane" "(5760 3008 1728) (-2496 3008 1728) (-2496 3008 -1723.92)"
                vertices_plus
                {
                    "v" "5728 3008 -1691.92"
                    "v" "5760 3008 -1691.92"
                    "v" "5760 3008 1696"
                    "v" "5728 3008 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"

            }
            side
            {
                "id" "22570"
                "plane" "(5760 -5888 -1723.92) (-2496 -5888 -1723.92) (-2496 -5888 1728)"
                vertices_plus
                {
                    "v" "5760 -5888 1696"
                    "v" "5760 -5888 -1691.92"
                    "v" "5728 -5888 -1691.92"
                    "v" "5728 -5888 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"

            }
            side
            {
                "id" "22569"
                "plane" "(-2464 2976 1696) (5728 2976 1696) (5728 -5856 1696)"
                vertices_plus
                {
                    "v" "5728 3008 1696"
                    "v" "5760 3008 1696"
                    "v" "5760 -5888 1696"
                    "v" "5728 -5888 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"

            }
            side
            {
                "id" "22568"
                "plane" "(-2464 -5856 -1691.92) (5728 -5856 -1691.92) (5728 2976 -1691.92)"
                vertices_plus
                {
                    "v" "5728 -5888 -1691.92"
                    "v" "5760 -5888 -1691.92"
                    "v" "5760 3008 -1691.92"
                    "v" "5728 3008 -1691.92"
                }
                "material" "TOOLS/TOOLSNODRAW"

            }
            side
            {
                "id" "22567"
                "plane" "(5728 -5856 1696) (5728 -5856 -1691.92) (5728 2976 -1691.92)"
                vertices_plus
                {
                    "v" "5728 -5888 1696"
                    "v" "5728 -5888 -1691.92"
                    "v" "5728 3008 -1691.92"
                    "v" "5728 3008 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"

            }

        }
        solid
        {
            "id" "3799"
            side
            {
                "id" "22578"
                "plane" "(5760 3008 1728) (-2496 3008 1728) (-2496 3008 -1723.92)"
                vertices_plus
                {
                    "v" "-2464 3008 -1691.92"
                    "v" "5728 3008 -1691.92"
                    "v" "5728 3008 1696"
                    "v" "-2464 3008 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"

            }
            side
            {
                "id" "22577"
                "plane" "(-2464 2976 1696) (5728 2976 1696) (5728 -5856 1696)"
                vertices_plus
                {
                    "v" "-2464 2976 1696"
                    "v" "-2464 3008 1696"
                    "v" "5728 3008 1696"
                    "v" "5728 2976 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"

            }
            side
            {
                "id" "22576"
                "plane" "(-2464 -5856 -1691.92) (5728 -5856 -1691.92) (5728 2976 -1691.92)"
                vertices_plus
                {
                    "v" "5728 3008 -1691.92"
                    "v" "-2464 3008 -1691.92"
                    "v" "-2464 2976 -1691.92"
                    "v" "5728 2976 -1691.92"
                }
                "material" "TOOLS/TOOLSNODRAW"

            }
            side
            {
                "id" "22575"
                "plane" "(-2464 2976 1696) (-2464 -5856 1696) (-2464 -5856 -1691.92)"
                vertices_plus
                {
                    "v" "-2464 2976 -1691.92"
                    "v" "-2464 3008 -1691.92"
                    "v" "-2464 3008 1696"
                    "v" "-2464 2976 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"

            }
            side
            {
                "id" "22574"
                "plane" "(5728 2976 -1691.92) (5728 -5856 -1691.92) (5728 -5856 1696)"
                vertices_plus
                {
                    "v" "5728 3008 1696"
                    "v" "5728 3008 -1691.92"
                    "v" "5728 2976 -1691.92"
                    "v" "5728 2976 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"

            }
            side
            {
                "id" "22573"
                "plane" "(-2464 2976 -1691.92) (-2464 2976 1696) (5728 2976 1696)"
                vertices_plus
                {
                    "v" "5728 2976 -1691.92"
                    "v" "-2464 2976 -1691.92"
                    "v" "-2464 2976 1696"
                    "v" "5728 2976 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"

            }

        }
        solid
        {
            "id" "3801"
            side
            {
                "id" "22584"
                "plane" "(5760 -5888 -1723.92) (-2496 -5888 -1723.92) (-2496 -5888 1728)"
                vertices_plus
                {
                    "v" "5728 -5888 -1691.92"
                    "v" "-2464 -5888 -1691.92"
                    "v" "-2464 -5888 1696"
                    "v" "5728 -5888 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"

            }
            side
            {
                "id" "22583"
                "plane" "(-2464 2976 1696) (5728 2976 1696) (5728 -5856 1696)"
                vertices_plus
                {
                    "v" "5728 -5888 1696"
                    "v" "-2464 -5888 1696"
                    "v" "-2464 -5856 1696"
                    "v" "5728 -5856 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"

            }
            side
            {
                "id" "22582"
                "plane" "(-2464 -5856 -1691.92) (5728 -5856 -1691.92) (5728 2976 -1691.92)"
                vertices_plus
                {
                    "v" "-2464 -5856 -1691.92"
                    "v" "-2464 -5888 -1691.92"
                    "v" "5728 -5888 -1691.92"
                    "v" "5728 -5856 -1691.92"
                }
                "material" "TOOLS/TOOLSNODRAW"

            }
            side
            {
                "id" "22581"
                "plane" "(-2464 2976 1696) (-2464 -5856 1696) (-2464 -5856 -1691.92)"
                vertices_plus
                {
                    "v" "-2464 -5888 1696"
                    "v" "-2464 -5888 -1691.92"
                    "v" "-2464 -5856 -1691.92"
                    "v" "-2464 -5856 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
            side
            {
                "id" "22580"
                "plane" "(5728 2976 -1691.92) (5728 -5856 -1691.92) (5728 -5856 1696)"
                vertices_plus
                {
                    "v" "5728 -5856 -1691.92"
                    "v" "5728 -5888 -1691.92"
                    "v" "5728 -5888 1696"
                    "v" "5728 -5856 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
            side
            {
                "id" "22579"
                "plane" "(-2464 -5856 1696) (-2464 -5856 -1691.92) (5728 -5856 -1691.92)"
                vertices_plus
                {
                    "v" "-2464 -5856 -1691.92"
                    "v" "5728 -5856 -1691.92"
                    "v" "5728 -5856 1696"
                    "v" "-2464 -5856 1696"
                }
                "material" "TOOLS/TOOLSNODRAW"
            }
        }
    """)

        f.write(vmfFile)
        print(f"VMF file '{path}' created successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse .pcf files into a vmf, ready for packing"
    )
    parser.add_argument(
        "input_dir",
        help="Path to the folder with .pcf files"
    )
    parser.add_argument(
        "output_vmf",
        help="Path to the output vmf"
    )
    args = parser.parse_args()

    # Get the list of pcf files
    contentList = getPCFs(args.input_dir)
    contentList = list(set(contentList))  # Remove duplicates

    # Split it
    models, textures = [], []

    for content in contentList:
        if content.endswith('.mdl'):
            models.append(content)
        elif content.endswith('.vmt'):
            textures.append(content)

    # Write VMF
    if args.output_vmf.endswith('.txt'):
        # Open file
        with open(args.output_vmf, 'w', encoding='utf-8') as f:
            f.write(str(textures) + "\n" * 5 + str(models))
    else:
        writeVMF(textures, models, args.output_vmf)