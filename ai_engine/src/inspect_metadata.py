
import zipfile
from pathlib import Path

zip_path = Path("data/raw/ednet/EdNet-KT1.zip")

with zipfile.ZipFile(zip_path, "r") as archive:

    files = archive.namelist()

    print("Possible metadata files:")

    metadata = [
        name for name in files
        if name.lower().endswith((".csv", ".json"))
        and not (
            name.startswith("KT1/u")
            and name.lower().endswith(".csv")
        )
    ]

    for name in metadata[:30]:
        print(name)

    print("\nSample student CSV:")

    student_file = next(
        name for name in files
        if name.startswith("KT1/u") and name.endswith(".csv")
    )

    with archive.open(student_file) as f:
        print(f.read(1500).decode("utf-8", errors="replace"))
