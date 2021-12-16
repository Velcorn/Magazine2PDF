import cv2
import os
import sys
from glob import glob
from PIL import Image
from tqdm import tqdm

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
        names = glob(f"{f}/*")
        pages = len(names) * 2 - 1

        print("Cutting pages...")
        for i, n in enumerate(tqdm(names, file=sys.stdout)):
            # Skip if image already present
            if os.path.exists(f"{path}/image{i:04n}.jpg"):
                continue

            # Read image
            img = cv2.imread(n)
            # Resize image to third of input
            height, width = img.shape[0] // 3, img.shape[1] // 3
            img = cv2.resize(img, (width, height))
            # Get middle of resized image
            middle = width // 2
            # If page number is odd, right side is lower page number, otherwise reverse
            # Save both pages with correct number
            if i % 2 == 0:
                cv2.imwrite(f"{path}/image{i:04n}.jpg", img[:, middle:])
                cv2.imwrite(f"{path}/image{pages - i:04n}.jpg", img[:, :middle])
            else:
                # Rotate image by 180 degrees
                img = cv2.rotate(img, cv2.cv2.ROTATE_180)
                cv2.imwrite(f"{path}/image{i:04n}.jpg", img[:, :middle])
                cv2.imwrite(f"{path}/image{pages - i:04n}.jpg", img[:, middle:])

        # Save images to PDF
        print("Creating PDF...")
        # Get file names/paths from output folder
        names = sorted(glob(f"{path}/*.jpg"))
        # Open images with Pillow
        imgs = [Image.open(name) for name in names]
        # Save all images into a single PDF
        imgs[0].save(f"{path}/{magazine}.pdf", save_all=True, append_images=imgs[1:])

        # Clean up images after PDF is created
        for name in names:
            os.remove(name)

        # Increase folder counter
        counter += 1
        print("Done!")
