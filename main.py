from pathlib import Path
import os
import sys
import shutil
import subprocess

CWD = getattr(sys, '_MEIPASS', os.getcwd())

RAWTEX = os.path.join(CWD, 'bin/RawtexCmd.exe')

def unpack_dds(file_name):

    input_path = Path(file_name)
    output_path = os.path.join(input_path.parent, input_path.stem + "_MOD")

    shutil.copyfile(str(input_path), output_path)

    subprocess.Popen([RAWTEX, output_path, 'BC7', '0x80']).wait()
    os.remove(output_path)

def pack_dds(file_name):

    input_path = Path(file_name)

    raw = open(input_path, "rb").read()

    original_file_path = str(input_path).replace("_MOD.dds", ".texture")

    if not os.path.isfile(original_file_path):
        print(f'Original texture file not found. Expected file: {original_file_path}')
        input()
        quit(1)

    original = open(original_file_path, "rb").read()

    raw = raw[148:]
    out_data = (original[:128] + raw)[:len(original)]

    output_path = Path(os.path.join(input_path.parent, input_path.stem + ".texture"))
    open(output_path, "wb").write(out_data)

if __name__ == "__main__":

    file = sys.argv[-1]

    if not file.endswith('.dds') and not file.endswith('.texture'):
        print('Input must be a file path or file name ending in ".dds" or ".texture"')
        print('Tip: Drag and drop the file into the executable.')
        input()
        quit(1)

    if file.endswith('.dds'):
        pack_dds(file)
        quit()

    unpack_dds(file)


