
import zipfile

path = "data/raw/ednet/EdNet-Content.zip"

with zipfile.ZipFile(path, "r") as archive:
    for name in archive.namelist():
        info = archive.getinfo(name)
        print(name, info.file_size, "bytes")
