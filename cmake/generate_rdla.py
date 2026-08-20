
# Script to generate rdla from usd using usdrecord.
# It fixes up elements that vary between runs, like hex ids, to enable stable comparison

import os
import sys
import re

if len(sys.argv) < 3:
    print("Usage: generate_rdla.py <input_path> <output_path> [rs=<rendersettings>] [cam=<camera>]")
    sys.exit(1)
input_path = sys.argv[1]
output_path = sys.argv[2]

import tempfile
tmp_fd, tmp_path = tempfile.mkstemp(prefix="generate_rdla_", suffix=".rdla")
os.close(tmp_fd)

camera_arg = ""
rs_arg = ""
for i in range(3, len(sys.argv)):
    if sys.argv[i].startswith("cam="):
        camera_arg = "-cam " + sys.argv[i].split("=")[1]
    elif sys.argv[i].startswith("rs="):
        rs_arg = "-rs " + sys.argv[i].split("=")[1]
    else:
        print("Unknown argument: ", sys.argv[i])
        sys.exit(1)

os.environ["HDMOONRAY_DISABLE_RENDER"] = "1"
os.environ["HDMOONRAY_RDLA_OUTPUT"] = tmp_path
os.environ["HDMOONRAY_SIMPLIFY_PATHS"] = "1"
os.environ["USDIMAGINGGL_ENGINE_ENABLE_SCENE_INDEX"] = "1"

ret = os.system(f"usdrecord -r Moonray -c medium --disableCameraLight {camera_arg} {rs_arg} {input_path} /tmp/dummy.exr")

if ret:
    sys.exit(ret)

# replace sequences of 16 hex digits with "H16X"
reps = [ (re.compile(r'_UsdImaging_HdMoonrayRendererPlugin_0x[0-9a-fA-F]{2,16}') , "_UsdImaging_HdMoonrayRendererPlugin_0xID")
]

with open(tmp_path, "r") as f:
    data = f.read()

for regex, replacement in reps:
    data = re.sub(regex, replacement, data)

with open(output_path, "w") as f:
    f.write(data)

# Clean up temporary file
os.remove(tmp_path)
