import argparse

from ramz.commands.build import build_command
from ramz.commands.run import run_command
from ramz.commands.kill import kill_command
from compiler.config import STAGES





def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")
    #build
    build_cmd = sub.add_parser("build")
    build_cmd.add_argument("source", nargs="?", default=None)
    build_cmd.add_argument("dest", nargs="?", default=None)
    build_cmd.add_argument("--dump", nargs="*", choices=STAGES , default=None)
    build_cmd.add_argument("--trace", nargs="*" , choices=STAGES , default=None)
    build_cmd.add_argument("--stop-at", choices=STAGES , default=None,)
    build_cmd.set_defaults(func=build_command)
    #run
    run_cmd = sub.add_parser("run")
    run_cmd.add_argument("build_dir", nargs="?", default=None)
    run_cmd.add_argument("--dump", nargs="*", choices=STAGES , default=None)
    run_cmd.add_argument("--trace", nargs="*", choices=STAGES , default=None)
    run_cmd.add_argument("--rebuild", action="store_true")
    run_cmd.set_defaults(func=run_command)
    #kill
    kill_cmd = sub.add_parser("kill")
    kill_cmd.set_defaults(func=kill_command)
    
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()



if __name__ == "__main__":
    main()
