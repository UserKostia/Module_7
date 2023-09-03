# scan.py
import re
import shutil
import sys
from pathlib import Path
image_extensions = ('JPEG', 'PNG', 'JPG', 'SVG')
video_extensions = ('AVI', 'MP4', 'MOV', 'MKV')
docs_extensions = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
audio_extensions = ('MP3', 'OGG', 'WAV', 'AMR')
archive_extensions = ('ZIP', 'GZ', 'TAR')

registered_extensions = image_extensions + video_extensions + docs_extensions + audio_extensions + archive_extensions

images = []
documents = []
audio = []
video = []
archives = []
unknown = []

categories = {'images': images,
              'documents': documents,
              'audio': audio,
              'video': video,
              'archives': archives}

known_extensions = set()
unknown_extensions = set()


def scan(path):
    for item in path.iterdir():
        if item.is_file():
            suffix = item.suffix

            suff_upp = suffix[1:].upper()
            if suff_upp in registered_extensions:
                known_extensions.add(suffix)
            else:
                unknown_extensions.add(suffix)

            if suff_upp in image_extensions:
                images.append(item)
            elif suff_upp in video_extensions:
                video.append(item)
            elif suff_upp in audio_extensions:
                audio.append(item)
            elif suff_upp in docs_extensions:
                documents.append(item)
            elif suff_upp in archive_extensions:
                archives.append(item)
            else:
                unknown.append(item)

        else:
            scan(item)
            if not any(item.iterdir()):
                item.rmdir()
            continue


# normalize.py


UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t",
    "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def normalize(name):
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"


# sort.py

def main(path):
    scan(path)
    for category, files in categories.items():
        category_dir = path / category
        category_dir.mkdir(exist_ok=True)

        for file in files:
            new_path = normalize(file.name)
            file.replace(path / category / new_path)

    scan(path)

    arch_path = Path(path / 'archives')
    for arch in arch_path.iterdir():
        shutil.unpack_archive(arch, arch_path / arch.stem)
        arch.unlink()

        scan(arch_path)


if __name__ == '__main__':
    main(Path(sys.argv[1]))
