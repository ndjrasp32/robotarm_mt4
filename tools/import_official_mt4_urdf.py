from __future__ import annotations

from pathlib import Path

try:
    from isaacsim import SimulationApp
except Exception:
    from omni.isaac.kit import SimulationApp


PROJECT_DIR = Path(__file__).resolve().parents[1]
URDF_PATH = PROJECT_DIR / "assets/urdf/wlkata_mt4_official/wlkata_mt4_official.urdf"
OUT_DIR = PROJECT_DIR / "assets/usd/wlkata_mt4_official"
OUT_USD = OUT_DIR / "wlkata_mt4_official.usd"

simulation_app = SimulationApp({"headless": True})

import omni.kit.commands
from pxr import Usd, UsdPhysics

from isaacsim.asset.importer.urdf import _urdf


def log(message: str) -> None:
    print(message, flush=True)


def main() -> int:
    if not URDF_PATH.exists():
        raise SystemExit(f"[ERROR] URDF not found: {URDF_PATH}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    import_config = _urdf.ImportConfig()
    import_config.convex_decomp = False
    import_config.fix_base = True
    import_config.make_default_prim = True
    import_config.self_collision = False
    import_config.distance_scale = 1
    import_config.density = 0.0

    optional_settings = {
        "merge_fixed_joints": False,
        "replace_cylinders_with_capsules": False,
        "import_inertia_tensor": True,
        "parse_mimic": True,
        "create_physics_scene": True,
        "make_instanceable": False,
    }
    for key, value in optional_settings.items():
        if hasattr(import_config, key):
            setattr(import_config, key, value)

    log(f"[INFO] URDF: {URDF_PATH}")
    log(f"[INFO] OUT : {OUT_USD}")

    result, robot_model = omni.kit.commands.execute(
        "URDFParseFile",
        urdf_path=str(URDF_PATH),
        import_config=import_config,
    )
    if not result:
        raise SystemExit("[ERROR] URDFParseFile failed")

    log(f"[PARSED LINKS] {len(robot_model.links)}")
    log(f"[PARSED JOINTS] {len(robot_model.joints)}")
    for name, joint in robot_model.joints.items():
        log(f" - JOINT: {name}")
        if hasattr(joint, "drive"):
            joint.drive.strength = 1000.0
            joint.drive.damping = 100.0

    result, prim_path = omni.kit.commands.execute(
        "URDFParseAndImportFile",
        urdf_path=str(URDF_PATH),
        import_config=import_config,
        dest_path=str(OUT_USD),
    )
    log(f"[IMPORT RESULT] {result}")
    log(f"[PRIM PATH] {prim_path}")
    if not result:
        raise SystemExit("[ERROR] URDFParseAndImportFile failed")

    for _ in range(60):
        simulation_app.update()

    if not OUT_USD.exists():
        raise SystemExit(f"[ERROR] USD not created: {OUT_USD}")

    stage = Usd.Stage.Open(str(OUT_USD), Usd.Stage.LoadAll)
    prims = list(stage.Traverse())
    joint_like = [
        prim
        for prim in prims
        if "joint" in str(prim.GetPath()).lower() or "Joint" in prim.GetTypeName()
    ]
    articulation_roots = [prim for prim in prims if prim.HasAPI(UsdPhysics.ArticulationRootAPI)]
    rigid_bodies = [prim for prim in prims if prim.HasAPI(UsdPhysics.RigidBodyAPI)]

    log(f"[OK] USD exists: {OUT_USD}")
    log(f"[PRIM COUNT] {len(prims)}")
    log(f"[JOINT-LIKE COUNT] {len(joint_like)}")
    log(f"[ARTICULATION ROOT COUNT] {len(articulation_roots)}")
    log(f"[RIGID BODY COUNT] {len(rigid_bodies)}")
    return 0


try:
    raise SystemExit(main())
finally:
    simulation_app.close()
