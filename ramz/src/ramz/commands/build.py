import time
from compiler.frontend.lexer import lexer
from compiler.frontend.parser import Parser
from compiler.frontend.type_checker import TypeChecker
from compiler.ir.lower import generate_lower
from compiler.backend.llvm_generator import LLVMGen
from ramz.debug import DebugContext
from ramz.utils import (
    get_msvc_env,
    find_clang,
    load_config,
    resolve_source_file,
    resolve_build_dir
)

import subprocess


def run_lexer(code):
    return lexer(code)

def run_parser(tokens):
    return Parser(tokens).parse()

def run_type_checker(tree):
    checker = TypeChecker()
    typed_ast, variables, functions = checker.check_program(tree)
    return {
        "ast": typed_ast,
        "variables": variables,
        "functions": functions
    }

def run_ir(data):
    return generate_lower(data["ast"])


def run_llvm(ir, gen):
    return gen.compile_ir(ir)


def build_command(args):
    start_time = time.perf_counter()

    source = args.source
    dest = args.dest
    dump_flags = args.dump
    trace_flags = args.trace
    stop_at = args.stop_at

    env = get_msvc_env()
    config = load_config()
    source = resolve_source_file(source)
    build_dir = resolve_build_dir(config,dest)
    dump_dir = build_dir/"logs"/"stage"

    debug = DebugContext(trace_flags, dump_flags, dump_dir)

    gen = LLVMGen()

    if source.suffix.lower() not in  {".rz", ".rmz"}:
        raise ValueError(
            f"Unsupported source file '{source.name}'. "
            "Only .rz and .rmz files can be built."
        )

    with open(source, "r") as f:
        code = f.read()
    pipeline = [
        ("tokens", run_lexer),
        ("ast", run_parser),
        ("type-checker", run_type_checker),
        ("ir", run_ir),
        ("llvm", lambda ir: run_llvm(ir, gen))
    ]
    data = code

    for name, stage_fn in pipeline:
        data = stage_fn(data)
        debug.trace(name, data)
        debug.dump(name, data)
        if stop_at == name:
            debug.flush()
            return
    

    build_dir.mkdir(parents=True, exist_ok=True)
    ll_path = build_dir / "output.ll"
    exe_path = build_dir / "program.exe"

    with ll_path.open("w") as f:
        f.write(str(data))

    clang = find_clang()

    subprocess.run([
    str(clang),
    str(ll_path),
    "runtime/runtime.c",
    "-o",
    str(exe_path)
], check=True,env=env)

    debug.flush()

    end_time = time.perf_counter()
    elapsed = end_time - start_time

    print(f"[OK] Built → {exe_path}")
    print(f"[TIME] Build completed in {elapsed:.3f} seconds")
