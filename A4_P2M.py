import random
import os
import sys
from glob import glob
from pikepdf import Pdf
from tqdm import tqdm

# Specify input folder!
# Structure should be 'folder/magazine folders/images'
# NOTE: root folder of input folder has to exist already!
input_path = './Input_A4_P2M'
comic_path = './Perscheid'


if __name__ == '__main__':
    # Create output folder
    output_path = input_path.replace('Input', 'Output')
    os.makedirs(output_path, exist_ok=True)

    # Get all folders in input path
    folders = glob(f'{input_path}/*')

    # Iterate over folders
    for f in folders:
        print(f'Processing year {f[-4:]}')
        sub_folders = glob(f'{f}/*')
        for sf in tqdm(sub_folders, file=sys.stdout):
            # Skip if PDF already exists
            magazine = sf.replace('\\', '/').split('/')[-1]
            if os.path.exists(f'{output_path}/{f[-4:]}/{magazine}/{magazine}.pdf'):
                continue

            # Create equivalent path in output folder
            path = '/'.join(sf.replace('\\', '/').replace('Input', 'Output').split('/'))
            os.makedirs(path, exist_ok=True)

            # Get file names/paths from input folder
            names = sorted(glob(f'{sf}/*'))

            # Insert last page to second position
            names.insert(1, names.pop())
            names += random.sample(glob(f'{comic_path}/*'), 6)

            # Merge PDFs
            pdf = Pdf.new()
            for name in names:
                src = Pdf.open(name)
                pdf.pages.extend(src.pages)
            pdf.remove_unreferenced_resources()
            pdf.save(f'{path}/{magazine}.pdf')

    print('All done!')
