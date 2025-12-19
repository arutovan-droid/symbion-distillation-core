from dataclasses import dataclass
from typing import Any, Optional, Dict, List


@dataclass
class RawInput:
    """
    Raw text input for the distillation still.
    Can come from:
    - external corpora,
    - dialogs,
    - AI outputs,
    - any other textual stream.
    """
    content: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class Essence:
    """
    Structural crystal – what is allowed to enter the Librarium.

    `structure` may be:
    - a graph,
    - a PSL contract,
    - a set of propositions,
    - any other formal representation.
    """
    structure: Any
    sources: List[str]
    notes: Optional[Dict[str, Any]] = None
