import os

def create_output_filepath(input_path, output_path=None, suffix='new'):
    """ Given an input filepath [option given an output dir path], create an
    output filepath with a new suffix.
    """
    # define output filename
    fname_in, ext = os.path.splitext(os.path.basename(input_path))
    fname_out = fname_in + '_' + suffix + ext
    # define output path
    if output_path is not None:
        outfile = os.path.join(output_path, fname_out)
    else:
        outfile = os.path.join(os.path.dirname(input_path), fname_out)

    return outfile
