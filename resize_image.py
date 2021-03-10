import argparse
from py_utils.io.filehandling import create_output_filepath
from py_utils.image_processing.resize import resize_image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('f', help='file')
    parser.add_argument('--frac', default=0.5, type=float, help='fraction to resize to')
    parser.add_argument('--o', default=None, help='output_path [default same as input]')
    parser.add_argument('--q', default=0.95, type=float, help='image save quality (frac)')
    args = parser.parse_args()

    # output filename
    outfile = create_output_filepath(args.f, args.o, suffix='resized')
    resize_image(args.f, outfile, frac=args.frac, quality=args.q)


if __name__=='__main__':
    main()
