from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class Paths():
    """
    Resolves paths to input and output files
    """
    input: str
    output: str
    config: str


def resolve_paths() -> Paths:

    MAIN_DIR = Path(__file__).resolve().parent.parent

    DATA_DIR = MAIN_DIR / 'data'
    CONFIG_DIR = MAIN_DIR / 'config'

    paths = Paths(
        input = DATA_DIR / 'input',
        output = DATA_DIR / 'output',
        config = CONFIG_DIR
        )

    return paths
