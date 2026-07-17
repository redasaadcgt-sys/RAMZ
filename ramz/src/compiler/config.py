from dataclasses import dataclass
from pathlib import Path

STAGES = ["tokens", "ast", "type-checker", "ir", "llvm"]

CACHE_FILE = Path(".ramz/cache.json")

@dataclass
class BuildConfig:
    source: str | None
    dest: str | None
    dump: list[str] 
    trace: list[str] 
    stop_at: str | None
