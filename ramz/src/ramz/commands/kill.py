import subprocess
from ramz.utils import load_config, resolve_build_file


def kill_command(args):
    config = load_config()
    build_file = resolve_build_file(config)
    build_dir = build_file.parent

    pid_file = build_dir / "program.pid"

    try:
        with pid_file.open("r") as f:
            pid = f.read().strip()

        result = subprocess.run(
            ["taskkill", "/PID", pid, "/F"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"[KILL] process {pid} terminated")
        else:
            print(f"[KILL] process {pid} is not running")

        if pid_file.exists():
            pid_file.unlink()

    except FileNotFoundError:
        print("[KILL] no pid file found")

    except Exception as e:
        print(f"[KILL] error: {e}")