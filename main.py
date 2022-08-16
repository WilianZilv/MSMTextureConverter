from pathlib import Path
import os
import sys
import shutil
import subprocess

CWD = getattr(sys, '_MEIPASS', os.getcwd())

RAWTEX = os.path.join(CWD, 'bin/RawtexCmd.exe')

def has_header(raw):
    return 'Texture Built File' in str(raw[:128])

def unpack_dds(file_name):

    input_path = Path(file_name)
    output_path = os.path.join(input_path.parent, input_path.stem + "_MOD")

    shutil.copyfile(str(input_path), output_path)

    raw = open(output_path, 'rb').read()

    offset = '0x80' if has_header(raw) else '0x00'

    subprocess.Popen([RAWTEX, output_path, 'BC7', offset]).wait()
    os.remove(output_path)
    print('Unpacked:', str(input_path))

def pack_dds(file_name):

    input_path = Path(file_name)
    original_file_path = str(input_path).replace("_MOD.dds", ".texture")

    if not os.path.isfile(original_file_path):
        print(f'Original texture file not found. Expected file: {original_file_path}')
        input()
        quit(1)

    raw = open(input_path, "rb").read()
    raw = raw[148:]

    original = open(original_file_path, "rb").read()

    header = original[:128] if has_header(original) else b''

    out_data = (header + raw)[:len(original)]

    output_path = Path(os.path.join(input_path.parent, input_path.stem + ".texture"))
    open(output_path, "wb").write(out_data)
    print('Packed:', str(input_path))

def read_input():
    files = sys.argv[1:]

    files = list(filter(lambda x: x.endswith(".dds") or x.endswith(".texture"), files))

    if not len(files):
        print('Input must be a file path or file name ending in ".dds" or ".texture"')
        print('Tip: Drag and drop the file into the executable.')
        input()
        quit(1)

    return files

if __name__ == "__main__":

    files = read_input()

    for file in files:
        if file.endswith('.dds'):
            pack_dds(file)
            continue

        if file.endswith('.texture'):
            unpack_dds(file)
            continue