from typing import Optional
from .types import RawInput, Essence


def distill_to_structure(raw: RawInput) -> Optional[Essence]:
    """
    Stub implementation of the distillation still.

    In production this will include:
      - structural extraction,
      - slag filtering (emotions, rhetoric, fluff),
      - normalization into a graph / PSL / other formalism.

    For now, returns None as a placeholder.
    """
    # TODO: implement the real distillation pipeline
    return None
