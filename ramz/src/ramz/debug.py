from pathlib import Path

class DebugContext:
    def __init__(self, trace_flags=None, dump_flags=None, dump_dir=None):
        self.trace_flags = set(trace_flags) if trace_flags is not None else None
        self.dump_flags = set(dump_flags) if dump_flags is not None else None
        self.dump_dir = dump_dir
        self.trace_buffer=[]
        self.dump_buffer={}

    def _enabled(self, stage, flags):
        if flags is None:
            return False
        if len(flags) == 0:
            return True
        return stage in flags
    
    def trace(self, stage, value):
        if not self._enabled(stage, self.trace_flags):
            return
        debug_value = str(value) # fixs the reference bug 
        if stage == "type-checker":
            variables = "•Variables: \n" + ("\n".join(str(var) for var in value["variables"]) if value["variables"] else "no variables")
            functions = "•Functions: \n" + ("\n".join(str(func) for func in value["functions"]) if value["functions"] else "no functions")
            ast = f"•Typed ast: \n{value["ast"]}"
            debug_value = f"{variables}\n{functions}\n{ast}"
        self.trace_buffer.append((stage, debug_value))

    def dump(self, stage, content):
        if not self._enabled(stage, self.dump_flags):
            return
        debug_content = str(content)
        if stage == "type-checker":
            variables = "•Variables: \n" + ("\n".join(str(var) for var in content["variables"]) if content["variables"] else "no variables")
            functions = "•Functions: \n" + ("\n".join(str(func) for func in content["functions"]) if content["functions"] else "no functions")
            ast = f"•Typed ast: \n{content["ast"]}"
            debug_content = f"{variables}\n{functions}\n{ast}"
        self.dump_buffer[stage] = debug_content
    
    def flush(self):
        if self.trace_buffer:
            print("\n### TRACE ###")
            for stage, value in self.trace_buffer :
                print(f"\n{stage.upper()}")
                print(f"{value}\n")

        if self.dump_buffer:
            print("\n### DUMP ###")
            for stage, value in self.dump_buffer.items():
                print(f"\nSaving {stage}...")
                path = (self.dump_dir / f"{stage}.txt").resolve()
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(str(value), encoding="utf-8")
                print(f"✓ {path}\n")