from dataclasses import dataclass, field


@dataclass
class CheckArgs:
    paper_id: str | None = None


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
