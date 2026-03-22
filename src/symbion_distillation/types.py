from __future__ import annotations

from dataclasses import dataclass, field
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
class DistillationDecision:
    crystal_candidates: List[CrystalCandidate] = field(default_factory=list)
    state_vector_shifts: List[StateVectorShift] = field(default_factory=list)
    open_threads: List[OpenThread] = field(default_factory=list)
    burned_residue: List[BurnedResidue] = field(default_factory=list)
    rationale: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
