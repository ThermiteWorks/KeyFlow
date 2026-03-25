#!/usr/bin/env python3
# Converts icon.png -> KeyFlow.icns using macOS sips + iconutil
import subprocess, os, shutil

src = "icon.png"
iconset = "KeyFlow.iconset"

# Clean up any existing iconset
if os.path.exists(iconset):
    shutil.rmtree(iconset)
os.makedirs(iconset)

# Create PNG files at different sizes
sizes = [16, 32, 64, 128, 256, 512]
for s in sizes:
    subprocess.run(["sips", "-z", str(s), str(s), src,
                    "--out", f"{iconset}/icon_{s}x{s}.png"], capture_output=True)
    s2 = s * 2
    subprocess.run(["sips", "-z", str(s2), str(s2), src,
                    "--out", f"{iconset}/icon_{s}x{s}@2x.png"], capture_output=True)

# Convert all images to proper PNG format (sips saves as JPEG with PNG extension)
for f in os.listdir(iconset):
    if f.endswith('.png'):
        path = os.path.join(iconset, f)
        subprocess.run(["sips", "-s", "format", "png", path, "--out", path], capture_output=True)

# Create Contents.json
import json
contents = {
    "images": [
        {"filename": f"icon_{s}x{s}.png", "idiom": "mac", "scale": "1x", "size": f"{s}x{s}"}
        for s in sizes
    ] + [
        {"filename": f"icon_{s}x{s}@2x.png", "idiom": "mac", "scale": "2x", "size": f"{s}x{s}"}
        for s in sizes
    ],
    "info": {"author": "xcode", "version": 1}
}
with open(f"{iconset}/Contents.json", "w") as f:
    json.dump(contents, f, indent=2)

# Generate icns
result = subprocess.run(["iconutil", "-c", "icns", iconset, "-o", "KeyFlow.icns"], capture_output=True, text=True)
if os.path.exists("KeyFlow.icns"):
    print("KeyFlow.icns written")
    shutil.rmtree(iconset)
else:
    print("ERROR:", result.stderr if result.stderr else "Failed to generate ICNS")
