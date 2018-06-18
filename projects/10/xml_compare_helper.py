#!/usr/bin/env python3
import sys
import os
import subprocess
import platform

# a helper script to compare src/*.xml to dest/*.xml
def compare_xml(src_dir, dest_dir, is_tokenizer):
    for src_file in os.listdir(src_dir):
        if src_file.endswith('.jack'):
            continue
        elif is_tokenizer and not src_file.endswith('T.xml'):
            continue
        elif not is_tokenizer and src_file.endswith('T.xml'):
            continue
        basename = os.path.basename(src_file)
        base = os.path.splitext(basename)[0]
        dest_file = os.path.join(dest_dir, base+'.my.xml')
        src_file = os.path.join(src_dir, src_file)
        print('==> comparing', src_file, dest_file)
        if platform.system() == 'Windows':
            script = os.path.abspath("../../tools/TextComparer.bat")
        else:
            script = os.path.abspath("../../tools/TextComparer.sh")
        subprocess.run("{} {} {}".format(script, src_file, dest_file), shell=True, check=True)

def main():
    if len(sys.argv) < 4:
        print('Usage: ./xml_compare_helper.py [-t|-a] src_dir dest_dir')
        print('-t        compare *T.xml to *T.my.xml')
        print('-a        compare *.xml to *.my.xml')
        print('src_dir   dir for ground-truth xml')
        print('dest_dir  dir for our generated output xml')
        sys.exit(1)
    compare_xml(sys.argv[2], sys.argv[3], sys.argv[1] == '-t')

if __name__ == '__main__':
    main()