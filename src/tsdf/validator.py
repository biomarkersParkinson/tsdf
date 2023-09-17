import os
import argparse
import traceback
import json
from tsdf import read_tsdf, read_binary

def validate_tsdf_format(file_path):
    try:
        # Read the meta data (this will check for compulsory fields and such)
        metadata = read_tsdf.load_metadata_from_path(file_path)

        # Get the absolute path of the file and cut off the file name
        abs_path = os.path.abspath(file_path)
        abs_dir = os.path.dirname(abs_path)

        # Loop through all the files in the metadata
        for file_name, file_metadata in metadata.items():

            # print the file_metadata as json
            # print(json.dumps(file_metadata.get_plain_tsdf_dict_copy(), indent=4))

            # Load the binary data
            binary_data = read_binary.load_binary_from_metadata(abs_dir, file_metadata)

            # Success message
            print(f"Successfully loaded binary file {file_name}, resulting shape: {binary_data.shape}")

        return True

    except Exception as e:
        print(f"Error while validating: {e}")
        #traceback.print_exc()
        return False

def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(description='Validate a file content against the TSDF format.')
    parser.add_argument('file_path', help='Path to the file to validate')
    args = parser.parse_args()

    # Perform validation
    is_valid = validate_tsdf_format(args.file_path)

    # Exit with error code 1 if the validation failed
    exit(0 if is_valid else 1)

if __name__ == '__main__':
    main()
