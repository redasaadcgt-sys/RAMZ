from pathlib import Path
import tomli
import os
import subprocess
import json
from compiler.config import CACHE_FILE



def load_cache():
    if CACHE_FILE.exists():
        try:
            with CACHE_FILE.open("r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_cache(data):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with CACHE_FILE.open("w") as f:
        json.dump(data, f, indent=2)


def find_vcvars():
    cache = load_cache()

    # Use cached path
    cached = cache.get("vcvars")

    if cached and Path(cached).exists():
        return cached


    vswhere = r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe"

    result = subprocess.run(
        [
            vswhere,
            "-latest",
            "-products",
            "*",
            "-requires",
            "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
            "-find",
            r"VC\Auxiliary\Build\vcvars64.bat"
        ],
        capture_output=True,
        text=True,
        check=True
    )

    path = result.stdout.strip()

    if not path:
        raise RuntimeError(
            "MSVC toolchain not found. "
            "Install Visual Studio C++ Build Tools."
        )

    cache["vcvars"] = path
    save_cache(cache)

    return path


def get_msvc_env():
    cache = load_cache()

    # Use cached environment
    if "msvc_env" in cache:
        env = cache["msvc_env"]

        # restore as strings
        return {
            str(k): str(v)
            for k, v in env.items()
        }


    vcvars = find_vcvars()

    result = subprocess.run(
        f'"{vcvars}" && set',
        shell=True,
        capture_output=True,
        text=True,
        executable=r"C:\Windows\System32\cmd.exe",
        check=True
    )

    env = os.environ.copy()

    for line in result.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            env[key] = value


    cache["msvc_env"] = env
    save_cache(cache)

    return env


def find_clang():
    # 1. RAMZ custom environment variable 
    llvm_bin = os.environ.get("RAMZ_LLVM_BIN")

    if llvm_bin:
        clang = Path(llvm_bin) / ("clang.exe" if os.name == "nt" else "clang")
        if clang.exists():
            return str(clang)

    # 2. Program Files LLVM 
    program_llvm = Path(r"C:\Program Files\LLVM\bin") / (
        "clang.exe" if os.name == "nt" else "clang"
    )

    if program_llvm.exists():
        return str(program_llvm)

    # 3. Bundled toolchain 
    root = Path(__file__).resolve().parents[2]
    bundled = root / "toolchain" / "LLVM" / "bin" / (
        "clang.exe" if os.name == "nt" else "clang"
    )

    if bundled.exists():
        return str(bundled)

    raise RuntimeError(
        "LLVM/clang not found. Set RAMZ_LLVM_BIN, install LLVM in Program Files, or run setup."
    )


def find_project_root(start: Path | None = None) -> Path | None:
    current = (start or Path.cwd()).resolve()

    for path in [current, *current.parents]:
        if (path / "ramz.toml").exists():
            return path

    return None


def get_project_root() -> Path:
    return find_project_root() or Path.cwd()


def load_config(root: Path | None = None) -> dict:
    root = root or find_project_root()

    if root is None:
        return {}

    config_file = root / "ramz.toml"

    if not config_file.exists():
        return {}

    with config_file.open("rb") as f:
        return tomli.load(f)


def resolve_entry(config: dict | None = None) -> Path | None:
    root = get_project_root()
    config = config or load_config(root)

    entry = config.get("entry")
    if not entry:
        return None

    return (root / entry).resolve()


def resolve_source_file(arg_file: str | None):
    root = get_project_root()

    # 1. explicit file 
    if arg_file:
        return Path(arg_file).resolve()
        
    # 2. try config
    entry = resolve_entry()
    if entry and entry.exists():
        return entry

    # 3. fallback to guessing 
    search_dir = root if root else Path.cwd()

    candidates = [
        "main.rz",
        "main.rmz",
        "src/main.rz",
        "src/main.rmz",
        "examples/main.rz",
        "examples/main.rmz",
    ]

    for c in candidates:
        p = search_dir / c
        if p.exists():
            return p.resolve()

    raise FileNotFoundError(
        "No entry file found. Provide a file or define 'entry' in ramz.toml."
    )


def resolve_build_dir(config: dict | None = None, dest: str | None = None) -> Path:

    root = get_project_root()
    config = config or load_config(root)

    # 1. CLI override 
    if dest:
        return Path(dest).resolve()

    # 2. config value
    output = config.get("output", "build")
    return (root / output).resolve()
