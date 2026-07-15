from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CheckArgs:
    paper_id: str | None = None
    wiki_dir: Path | None = None
    concept: str | None = None
    phase: int | None = None


@dataclass
class Issue:
    severity: str        # "error" | "warning"
    module: str
    paper_id: str | None
    check: str
    message: str


@dataclass
class ModuleResult:
    module: str
    passed: bool
    issues: list[Issue] = field(default_factory=list)
    stats: dict = field(default_factory=dict)
