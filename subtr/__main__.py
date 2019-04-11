#!/usr/bin/env python3
# Copyright(c) 2019 Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Main Modules"""

import os
import io
import argparse
import mmap
from tqdm import tqdm
from google.cloud import translate_v3beta1 as translate

def do_translate(client, parent, args):
    """Do translation request and write response to target file"""
    filepath = args.file_path
    source = args.source_lang
    target = args.target_lang

    fpath = open(filepath, "r+")
    buf = mmap.mmap(fpath.fileno(), 0)
    num_lines = 0
    while buf.readline():
        num_lines += 1

    with tqdm(total=num_lines, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
        filename, ext = os.path.splitext(filepath)
        with io.open(filename + "-" + target.split('-')[0] + ext, 'wb') as output_file:
            with io.open(filepath, 'r') as input_file:
                contents = input_file.readlines()
                contents[0] = "1\n"
                for i, _ in enumerate(contents):
                    if contents[i][0].isdigit():
                        output_file.write(contents[i].encode())
                    else:
                        response = client.translate_text(
                            parent=parent,
                            contents=[contents[i]],
                            mime_type='text/plain',
                            source_language_code=source,
                            target_language_code=target)
                        for translation in response.translations:
                            output_file.write(
                                (translation.translated_text).encode())
                    pbar.set_postfix(file=filepath[-10:], refresh=False)
                    pbar.update()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Subtitle translator.")
    parser.add_argument("-s", "--source_lang", dest="source_lang",
                        help="Source language translate from.", required=True, default="en-US")
    parser.add_argument("-t", "--target_lang", dest="target_lang",
                        help="Target language translate to.", required=True)
    parser.add_argument("-f", "--file", dest="file_path",
                        help="PATH to subtitle file.", required=True)
    args = parser.parse_args()

    client = translate.TranslationServiceClient()

    project_id = os.environ.get("PROJECT_ID")
    location = 'global'

    parent = client.location_path(project_id, location)

    do_translate(client, parent, args)

if __name__ == "__main__":
    main()
