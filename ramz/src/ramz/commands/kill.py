import subprocess
from ramz.utils import load_config, resolve_build_dir


def kill_command(args):
    config = load_config()
    build_dir = resolve_build_dir(config)

    pid_file = build_dir / "program.pid"

    try:
        with pid_file.open("r") as f:
            pid = f.read().strip()

        subprocess.run(["taskkill", "/PID", pid, "/F"])
        print(f"[KILL] process {pid} terminated")

        pid_file.unlink()

    except FileNotFoundError:
        print("[KILL] no pid file found")

    except Exception as e:
        print(f"[KILL] error: {e}")
