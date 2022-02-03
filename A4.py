import os
import sys
from glob import glob
from PIL import Image
from tqdm import tqdm

# Specify input folder!
# Structure should be "folder/magazine folders/images"
# NOTE: root folder of input folder has to exist already!
input_path = "D:/Programming/Magazine2PDF/Input_A4"


if __name__ == '__main__':
    # Create output folder
    output_path = input_path.replace("Input", "Output")
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

        # Get file names/paths from input folder
        names = sorted(glob(f"{f}/*.jpg"))
        # Open again and do proper resizing to 1/x of input res
        print("Resizing images...")
        divisor = 2
        for n in tqdm(names, file=sys.stdout):
            img = Image.open(n)
            width, height = img.size
            img = img.resize((width // divisor, height // divisor), Image.ANTIALIAS)
            # Save resized images to output folder
            img.save(n.replace("Input", "Output"))

        # Save images to PDF
        print("Creating PDF...")
        # Get file names/paths from output folder
        names = sorted(glob(f"{path}/*.jpg"))
        # Open images with Pillow
        images = [Image.open(name) for name in names]
        # Save all images into a single PDF
        images[0].save(f"{path}/{magazine}.pdf", resolution=300, save_all=True, append_images=images[1:])

        # Clean up images after PDF is created
        for name in names:
            os.remove(name)

        # Increase folder counter
        counter += 1
        print("Done!")
