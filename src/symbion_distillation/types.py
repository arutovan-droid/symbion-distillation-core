from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


@dataclass
class DistillationPacket:
    packet_id: str
    state_vector: Dict[str, Any] = field(default_factory=dict)
    crystal_draft: Dict[str, Any] = field(default_factory=dict)
    continuity_event: Dict[str, Any] = field(default_factory=dict)
    resonance_candidate: Dict[str, Any] = field(default_factory=dict)
    laetitia_index: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DistillationInput:
    packets: List[DistillationPacket]
    operator_id: str = "unknown"
    session_id: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CrystalCandidate:
    packet_id: str
    principle: str
    support: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StateVectorShift:
    packet_id: str
    shift_type: str
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OpenThread:
    packet_id: str
    thread_type: str
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BurnedResidue:
    packet_id: str
    residue_type: str
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OperatorEssenceDelta:
    dominant_state_shift: Dict[str, Any] = field(default_factory=dict)
    dominant_crystal_principle: Dict[str, Any] = field(default_factory=dict)
    dominant_open_thread: Dict[str, Any] = field(default_factory=dict)

    def to_snapshot_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_snapshot_dict(cls, data: Dict[str, Any]) -> "OperatorEssenceDelta":
        return cls(
            dominant_state_shift=dict(data.get("dominant_state_shift", {})),
            dominant_crystal_principle=dict(data.get("dominant_crystal_principle", {})),
            dominant_open_thread=dict(data.get("dominant_open_thread", {})),
        )


@dataclass
class DistillationDecision:
    crystal_candidates: List[CrystalCandidate] = field(default_factory=list)
    state_vector_shifts: List[StateVectorShift] = field(default_factory=list)
    open_threads: List[OpenThread] = field(default_factory=list)
    burned_residue: List[BurnedResidue] = field(default_factory=list)
    operator_essence_delta: OperatorEssenceDelta = field(default_factory=OperatorEssenceDelta)
    rationale: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_snapshot_dict(self) -> Dict[str, Any]:
        return {
            "crystal_candidates": [asdict(x) for x in self.crystal_candidates],
            "state_vector_shifts": [asdict(x) for x in self.state_vector_shifts],
            "open_threads": [asdict(x) for x in self.open_threads],
            "burned_residue": [asdict(x) for x in self.burned_residue],
            "operator_essence_delta": self.operator_essence_delta.to_snapshot_dict(),
            "rationale": list(self.rationale),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_snapshot_dict(cls, data: Dict[str, Any]) -> "DistillationDecision":
        return cls(
            crystal_candidates=[
                CrystalCandidate(**item) for item in data.get("crystal_candidates", [])
            ],
            state_vector_shifts=[
                StateVectorShift(**item) for item in data.get("state_vector_shifts", [])
            ],
            open_threads=[
                OpenThread(**item) for item in data.get("open_threads", [])
            ],
            burned_residue=[
                BurnedResidue(**item) for item in data.get("burned_residue", [])
            ],
            operator_essence_delta=OperatorEssenceDelta.from_snapshot_dict(
                data.get("operator_essence_delta", {})
            ),
            rationale=list(data.get("rationale", [])),
            metadata=dict(data.get("metadata", {})),
        )
