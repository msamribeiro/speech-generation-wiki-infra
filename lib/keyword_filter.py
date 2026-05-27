from pathlib import Path
import yaml

_CONFIG_PATH = Path(__file__).parent.parent / "config" / "keyword_filter.yaml"


def load_keyword_filter(config_path: Path = _CONFIG_PATH) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def _include_terms(kf: dict) -> list:
    terms = []
    for group in kf["include"].values():
        terms.extend(t.lower() for t in group)
    return terms


def passes_filter(title: str, abstract: str, kf: dict) -> bool:
    include = _include_terms(kf)
    exclude = [t.lower() for t in kf["exclude"]]
    combined = (title + " " + abstract).lower()
    if any(t in combined for t in exclude):
        return False
    title_hits = sum(1 for t in include if t in title.lower())
    abstract_hits = sum(1 for t in include if t in abstract.lower())
    return title_hits >= kf["title_min_matches"] or abstract_hits >= kf["abstract_min_matches"]
