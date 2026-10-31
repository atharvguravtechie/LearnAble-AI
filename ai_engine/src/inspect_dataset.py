
import zipfile
from pathlib import Path

zip_path = Path("data/raw/ednet/EdNet-KT1.zip")

if not zip_path.exists():
    print("ZIP file not found:", zip_path)
    raise SystemExit

with zipfile.ZipFile(zip_path, "r") as archive:
    csv_files = [
        name for name in archive.namelist()
        if name.endswith(".csv")
    ]

    print("Total CSV files:", len(csv_files))
    print("\nFirst 15 CSV files:")

    for name in csv_files[:15]:
        info = archive.getinfo(name)
        print(name, "-", round(info.file_size / 1024, 2), "KB")
