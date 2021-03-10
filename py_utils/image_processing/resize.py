from PIL import Image
import argparse
import os

def resize_image(input_file, output_file, frac=0.5, quality=0.95):
    img = Image.open(input_file)
    info = {
        'format': img.format,
        'mode': img.mode,
        'size': img.size,
    }
    print(info)

    # new dimensions
    new_dims = (int(x * frac) for x in img.size)
    img_new = img.resize(new_dims, Image.ANTIALIAS)
    # save
    img_new.save(output_file, optimize=True, quality=quality)

    print(f'resized to: {img_new.size}')
    print(f'written: {output_file}')
