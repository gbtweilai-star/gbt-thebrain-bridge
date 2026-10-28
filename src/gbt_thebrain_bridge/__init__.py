"""thebrain_bridge — integration capability, packaged standalone.

Contract, validation and CLI for one capability bit extracted from the
GBT V8 registry. Nothing here is invented: the spec is copied verbatim from
the registry snapshot, and the atlas page it came from is linked in the README.

    >>> from gbt_thebrain_bridge import SPEC, run
    >>> SPEC.name
    'thebrain_bridge'
    >>> run({}).status   # doctest: +SKIP
    'validated'
"""

from .core import Result, run
from .errors import BackendRequired, CapError, PayloadError
from .spec import SPEC, CapSpec

__version__ = "1.0.0"
__all__ = [
    "SPEC",
    "CapSpec",
    "run",
    "Result",
    "CapError",
    "PayloadError",
    "BackendRequired",
    "__version__",
]
