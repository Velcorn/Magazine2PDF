import cv2
import os
import sys
from glob import glob
from PIL import Image
from tqdm import tqdm

# Specify input folder!
# Structure should be "folder/magazine folders/images"
# NOTE: root folder of input folder has to exist already!
input_path = "D:/Programming/Magazine2PDF/Input_A3"


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
        in_names = glob(f"{f}/*")
        pages = len(in_names) * 2 - 1

        print("Cutting pages...")
        for i, n in enumerate(tqdm(in_names, file=sys.stdout)):
            # Skip if image already present
            if os.path.exists(f"{path}/image{i:04n}.jpg"):
                continue

            # Read image
            img = cv2.imread(n)

            # Resize image to 1/x of original size
            divisor = 2
            height, width, _ = [x // divisor for x in img.shape]
            img = cv2.resize(img, (width, height), cv2.INTER_AREA)

            # Get middle of image
            middle = width // 2

            # If page number is odd, right side is lower page number, otherwise reverse
            # Save both pages with correct number
            if i % 2 == 0:
                cv2.imwrite(f"{path}/image{i:04n}.jpg", img[:, middle:])
                cv2.imwrite(f"{path}/image{pages - i:04n}.jpg", img[:, :middle])
            else:
                cv2.imwrite(f"{path}/image{i:04n}.jpg", img[:, :middle])
                cv2.imwrite(f"{path}/image{pages - i:04n}.jpg", img[:, middle:])

        # Save images to PDF
        print("Creating PDF...")

        # Get name/path of images in output folder
        out_names = sorted(glob(f"{path}/*.jpg"))

        # Open images with Pillow
        images = [Image.open(name) for name in out_names]

        # Save all images into a single PDF
        images[0].save(f"{path}/{magazine}.pdf", resolution=300, save_all=True, append_images=images[1:])

        # Clean up images after PDF is created
        for n in out_names:
            os.remove(n)

        # Increase folder counter
        counter += 1
        print("Done!")
