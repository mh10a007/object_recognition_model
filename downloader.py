from bing_image_downloader import downloader
from PIL import Image
import os
import glob

# -----------------------------
# PARAMETERS
# -----------------------------
queries = [
"over-ear headphones on office desk with notebook and pen, focus on the headphones",
"wireless earbuds in charging case on table, focus on the earbuds",
"headphones worn around neck of person walking outside, focus on the headphones",
"gaming headset on RGB-lit desk setup, focus on the headset",
"studio monitoring headphones on audio mixer, focus on the headphones",
"wireless earbuds in human hand closeup, focus on the earbuds",
"headphones hanging on monitor edge in dim room, focus on the headphones",
"sport earbuds worn during workout gym environment, focus on the earbuds",
"over-ear headphones placed on bed morning light, focus on the headphones",
"wired headphones tangled next to phone on desk, focus on the headphones",
"noise-cancelling headphones in airplane seat environment, focus on the headphones",
"earbuds hanging from person's ears outdoors walking, focus on the earbuds",
"headphones with torn ear cushion damaged condition, focus on the damaged headphones",
"wireless earbuds dropped on floor dramatic lighting, focus on the earbuds",
"headphones on coffee shop table next to a latte, focus on the headphones",
"over-ear headphones placed on chair armrest, focus on the headphones",
"headphones resting on keyboard in studio setup, focus on the headphones",
"earbuds inside pocket partially visible, focus on the earbuds",
"gaming headset worn by person playing at PC, focus on the headset",
"headphones around neck DJ wearing them backstage, focus on the headphones",
"over-ear headphones on books stack study environment, focus on the headphones",
"wired earbuds wrapped around phone, focus on the earbuds",
"bluetooth headphones charging with USB cable, focus on the charging port",
"headphones in open backpack everyday scenario, focus on the headphones",
"earbuds on gym bench next to water bottle, focus on the earbuds",
"headphones hanging on wall hook warm light, focus on the headphones",
"wireless earbuds worn by runner on trail, focus on the earbuds",
"over-ear headphones beside spilled coffee cup accident, focus on the headphones",
"headphones lying on car passenger seat, focus on the headphones",
"earbuds on beach towel outdoor sunny scene, focus on the earbuds",
"studio headphones on microphone stand, focus on the headphones",
"premium headphones unboxed packaging scene, focus on the headphones",
"headphones on metal table industrial environment, focus on the headphones",
"earbuds next to laptop mid-zoom call scenario, focus on the earbuds",
"gaming headset on shelf with collectibles, focus on the headset",
"headphones resting on sofa cozy evening lighting, focus on the headphones",
"sport earbuds with sweat droplets after workout, focus on the earbuds",
"over-ear headphones placed on vinyl record player, focus on the headphones",
"noise cancelling headphones worn on train commute, focus on the headphones",
"earbuds on bedside table next to lamp, focus on the earbuds",
]



output_dir = "dataset"
final_folder = os.path.join(output_dir, "downloader")
os.makedirs(final_folder, exist_ok=True)

images_per_query = 25  # number of images per query
resize_to = (224, 224)  # width x height

counter = 1  # sequential numbering for images

# -----------------------------
# DOWNLOAD IMAGES
# -----------------------------
for query in queries:
    print(f"Downloading images for: {query}")
    
    downloader.download(
        query,
        limit=images_per_query,
        output_dir=final_folder,
        adult_filter_off=True,
        force_replace=False,
        timeout=60,
        filter="photo",
        verbose=True
    )

# -----------------------------
# COLLECT ALL IMAGE FILES
# -----------------------------
# bing-image-downloader creates a folder per query
all_folders = [
    os.path.join(final_folder, f)
    for f in os.listdir(final_folder)
    if os.path.isdir(os.path.join(final_folder, f))
]

all_images = []
for f in all_folders:
    all_images.extend(glob.glob(os.path.join(f, "*.*")))

# -----------------------------
# PROCESS: Resize, Convert to JPG, Rename as pen_0001.jpg, pen_0002.jpg, ...
# -----------------------------
for img_path in all_images:
    try:
        img = Image.open(img_path).convert("RGB")
        img_resized = img.resize(resize_to)

        # zero-padded counter: pen_0001.jpg, pen_0002.jpg, ...
        new_filename = f"img_{counter:04d}.jpg"
        new_path = os.path.join(final_folder, new_filename)

        img_resized.save(new_path, "JPEG")
        counter += 1
    except Exception as e:
        print(f"Skipping {img_path}, error: {e}")

# -----------------------------
# CLEANUP: Remove original query subfolders
# -----------------------------
for f in all_folders:
    try:
        for file in os.listdir(f):
            os.remove(os.path.join(f, file))
        os.rmdir(f)
    except Exception as e:
        print(f"Cleanup issue in {f}: {e}")

print(f"Done! Total images: {counter-1}")
print(f"All images are in folder: {final_folder}, named pen_0001.jpg, pen_0002.jpg, ... and resized to {resize_to}")
