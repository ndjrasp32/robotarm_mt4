from pathlib import Path
import sys
import xml.etree.ElementTree as ET


PROJECT_DIR = Path(__file__).resolve().parents[1]
URDF_PATH = PROJECT_DIR / "assets/urdf/mirobot_wlkata_isaac_clean.urdf"
USD_PATH = PROJECT_DIR / "assets/usd/mirobot_real/mt4_from_wlkata_isaac_clean.usd"


def main() -> int:
    print("[INFO] project:", PROJECT_DIR)
    print("[INFO] urdf:", URDF_PATH)
    print("[INFO] usd:", USD_PATH)

    if not URDF_PATH.is_file():
        print("[ERROR] URDF not found:", URDF_PATH)
        return 1
    if not USD_PATH.is_file():
        print("[ERROR] USD not found:", USD_PATH)
        return 1

    root = ET.parse(URDF_PATH).getroot()
    print("[INFO] robot:", root.attrib.get("name"))
    print("[INFO] links:", len(root.findall("link")))
    print("[INFO] joints:", len(root.findall("joint")))
    print()
    print("joints:")
    for joint in root.findall("joint"):
        limit = joint.find("limit")
        axis = joint.find("axis")
        parent = joint.find("parent")
        child = joint.find("child")
        print(
            "-",
            joint.attrib.get("name"),
            joint.attrib.get("type"),
            "parent=" + (parent.attrib.get("link") if parent is not None else "?"),
            "child=" + (child.attrib.get("link") if child is not None else "?"),
            "axis=" + (axis.attrib.get("xyz") if axis is not None else "?"),
            "limit=" + (str(limit.attrib) if limit is not None else "{}"),
        )

    missing_meshes = []
    for mesh in root.findall(".//mesh"):
        filename = mesh.attrib.get("filename")
        if filename and filename.startswith("/") and not Path(filename).exists():
            missing_meshes.append(filename)

    print()
    if missing_meshes:
        print("[ERROR] missing mesh files:")
        for filename in missing_meshes:
            print("  ", filename)
        return 1

    print("[OK] all absolute mesh paths referenced by the URDF exist on this machine.")
    print("[OK] USD asset copy exists.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

