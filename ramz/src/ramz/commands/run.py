import subprocess
from ramz.utils import load_config, resolve_build_dir
from ramz.commands.build import build_command
from compiler.config import BuildConfig

def run_command(args):
    build_dir = args.build_dir
    dump_flags = args.dump
    trace_flags = args.trace
    rebuild = args.rebuild

    config = load_config()
    build_dir = resolve_build_dir(config,build_dir)

    if rebuild:
        cfg = BuildConfig(
            source=None,
            dest=None,
            dump=args.dump,
            trace=args.trace,
            stop_at=None
        )
        build_command(cfg)
        
    exe_path = build_dir / "program.exe"
    pid_file = build_dir / "program.pid"

    process = subprocess.Popen([str(exe_path)])
    pid = process.pid

    with pid_file.open("w") as f:
        f.write(str(pid))

    print("[RUN] program.exe PID:", pid)

    try:
        code = process.wait()
    finally:
        if pid_file.exists():
            pid_file.unlink()
    print(f"[DONE] program.exe finished with exit code {code}")
    