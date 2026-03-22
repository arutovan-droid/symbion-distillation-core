from __future__ import annotations

from typing import Any, Dict, List

from .types import (
    BurnedResidue,
    CrystalCandidate,
    DistillationDecision,
    DistillationInput,
    DistillationPacket,
    OpenThread,
    StateVectorShift,
)


def _extract_principle(packet: DistillationPacket) -> str | None:
    crystal = packet.crystal_draft or {}
    principle = crystal.get("principle") or crystal.get("summary") or crystal.get("title")
    if isinstance(principle, str):
        principle = principle.strip()
    return principle or None


def _extract_state_shift(packet: DistillationPacket) -> Dict[str, Any] | None:
    continuity = packet.continuity_event or {}
    state_vector = packet.state_vector or {}

    if continuity:
        return {
            "continuity_event": continuity,
            "state_vector": state_vector,
        }

    if state_vector:
        return {
            "state_vector": state_vector,
        }

    return None


def _extract_open_thread(packet: DistillationPacket) -> Dict[str, Any] | None:
    continuity = packet.continuity_event or {}
    resonance = packet.resonance_candidate or {}

    if continuity.get("open_thread") or continuity.get("unresolved"):
        return {
            "continuity_event": continuity,
        }

    if resonance.get("status") in {"open", "unresolved", "pending"}:
        return {
            "resonance_candidate": resonance,
        }

    return None


def distill_packets(inp: DistillationInput) -> DistillationDecision:
    decision = DistillationDecision()
    decision.metadata = {
        "operator_id": inp.operator_id,
        "session_id": inp.session_id,
        "packets_total": len(inp.packets),
    }

    for packet in inp.packets:
        principle = _extract_principle(packet)
        if principle:
            decision.crystal_candidates.append(
                CrystalCandidate(
                    packet_id=packet.packet_id,
                    principle=principle,
                    support={
                        "laetitia_index": packet.laetitia_index,
                        "metadata": packet.metadata,
                    },
                )
            )
        else:
            decision.burned_residue.append(
                BurnedResidue(
                    packet_id=packet.packet_id,
                    residue_type="no_crystal_principle",
                    payload={"crystal_draft": packet.crystal_draft},
                )
            )

        shift_payload = _extract_state_shift(packet)
        if shift_payload:
            decision.state_vector_shifts.append(
                StateVectorShift(
                    packet_id=packet.packet_id,
                    shift_type="continuity_shift",
                    payload=shift_payload,
                )
            )

        thread_payload = _extract_open_thread(packet)
        if thread_payload:
            decision.open_threads.append(
                OpenThread(
                    packet_id=packet.packet_id,
                    thread_type="unresolved_thread",
                    payload=thread_payload,
                )
            )

        if not shift_payload and not thread_payload and not principle:
            decision.burned_residue.append(
                BurnedResidue(
                    packet_id=packet.packet_id,
                    residue_type="fully_burned",
                    payload={"metadata": packet.metadata},
                )
            )

    decision.rationale.append("distillation_extracts_only_structural_outputs")
    decision.rationale.append("non_structural_material_is_burned_not_stored")
    return decision
