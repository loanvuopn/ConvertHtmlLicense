import sys
import argparse

from bs4 import BeautifulSoup


def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in {'FALSE', 'False', 'false', 'f', '0', 'no', 'n'}:
        return False
    elif value.lower() in {'TRUE', 'True' ,'true', 't', '1', 'yes', 'y'}:
        return True
    raise ValueError(f'{value} is not a valid boolean value')

def main():
    # ==== Arguments ====
    parser = argparse.ArgumentParser(description='Perform merging static content.')
    parser.add_argument('-input', metavar='INPUT', type=str, nargs='+', help='path of input file')
    parser.add_argument('-output', metavar='OUTPUT', type=str, nargs='+', help='path of output file')
    parser.add_argument('--header', type=str_to_bool, nargs='?', const=True, default=False)

    args = parser.parse_args()

    # List input files
    file_names = args.input

    # Output file
    output_file = args.output

    # Header file
    header = args.header

    # ==== MAIN ====
    # Append content to license_info_android.html file
    with open(output_file[0], 'w') as result:
        for name in file_names:
            body_license = ''
            with open(name) as f:
                lines = f.readlines()

                # Build license header
                if header:
                    head_license = '<p class="m_txt s_small mb_20 m_alignCenter">{}<br />{}<br /><a href="{}" target="_blank">{' \
                                    '}</a></p>'.format(lines[0].strip(), lines[1].strip(), lines[2].strip(), lines[2].strip())
                else:
                    head_license = ''

                del lines[0:3]

                # Check and built license body
                content_block = ''
                for index, line in enumerate(lines):
                    content_line = line

                    if "http://" in content_line:
                        content_line = '<a href="{}" target="_blank">{}</a>'.format(content_line.strip(), content_line.strip())

                    # First blank line
                    if len(content_line.strip()) == 0:
                        if len(content_block) > 0:
                            body_license += '<p class="m_txt s_small mb_20">{}</p>'.format(content_block)
                            content_block = ''
                    else:
                        content_block += content_line

                # Re-format html
                full_license = head_license + body_license
                soup = BeautifulSoup(full_license, features = "html.parser")
                html = soup.prettify()

                # Write result
                result.truncate()
                result.write(html)


if __name__ == "__main__":
    main()