from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class Paths():
    """
    Container for file system paths used by the application.
    """
    input: str
    output: str
    config: str

def resolve_paths() -> Paths:
    """
    esolve project directory paths relative to the project root.

    Returns:
        Paths: Paths to input, output, and configuration directories
    """

    MAIN_DIR = Path(__file__).resolve().parent.parent

    DATA_DIR = MAIN_DIR / 'data'
    CONFIG_DIR = MAIN_DIR / 'config'

    paths = Paths(
        input = DATA_DIR / 'input',
        output = DATA_DIR / 'output',
        config = CONFIG_DIR
        )

    return paths
