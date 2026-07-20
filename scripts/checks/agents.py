"""Agent interoperability module for the Pipeline Health Suite."""

from checks._base import CheckArgs, Issue, ModuleResult
from check_agent_compat import SKILLS, validate


def run(_args: CheckArgs) -> ModuleResult:
    errors = validate()
    issues = [
        Issue(
            severity="error",
            module="agents",
            paper_id=None,
            check="agent_compat",
            message=message,
        )
        for message in errors
    ]
    return ModuleResult(
        module="agents",
        passed=not issues,
        issues=issues,
        stats={
            "errors": len(issues),
            "warnings": 0,
            "workflows_checked": len(SKILLS),
        },
    )
