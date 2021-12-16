import os
from glob import glob
from PIL import Image

# Specify input folder!
# Structure should be "folder/magazine folders/images"
# NOTE: root folder of input folder has to exist already!
input_path = "F:/Programming/Magazine2PDF/Input"


if __name__ == '__main__':
    # Create output folder
    output_path = f"{'/'.join(input_path.split('/')[:-1])}/Output"
    os.makedirs(output_path, exist_ok=True)
    # Get all folders in input path
    folders = glob(f"{input_path}/*")
    # Iterate over folders
    counter = 1
    for f in folders:
        print(f"Processing magazine {counter}/{len(folders)}...")
        # Skip if PDF already exists
        magazine = f.replace('\\', '/').split('/')[-1]
        if os.path.exists(f"{output_path}/{magazine}/{magazine}.pdf"):
            counter += 1
            print("Done!\n")
            continue

        # Create equivalent path in output folder
        path = "/".join(f.replace("\\", "/").replace("Input", "Output").split("/"))
        os.makedirs(path, exist_ok=True)
        # Get file names from input folder
        names = sorted(glob(f"{f}/*.jpg"))
        # Save images to PDF
        print("Creating PDF...")
        # Open images with Pillow
        imgs = [Image.open(name) for name in names]
        # Save all images into a single PDF
        imgs[0].save(f"{path}/{magazine}.pdf", save_all=True, append_images=imgs[1:])
        # Increase folder counter
        counter += 1
        print("Done!")
