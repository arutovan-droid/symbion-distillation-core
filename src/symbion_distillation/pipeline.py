from __future__ import annotations

from typing import Any, Dict

from .types import (
    BurnedResidue,
    CrystalCandidate,
    DistillationDecision,
    DistillationInput,
    DistillationPacket,
    OpenThread,
    OperatorEssenceDelta,
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
        return {"continuity_event": continuity}

    if resonance.get("status") in {"open", "unresolved", "pending"}:
        return {"resonance_candidate": resonance}

    return None


def distill_packets(inp: DistillationInput) -> DistillationDecision:
    decision = DistillationDecision()
    packets_with_crystal = []
    packets_with_shift = []
    packets_with_open_thread = []
    fully_burned_packets = []

    for packet in inp.packets:
        packet_has_crystal = False
        packet_has_shift = False
        packet_has_thread = False

        principle = _extract_principle(packet)
        if principle:
            packet_has_crystal = True
            packets_with_crystal.append(packet.packet_id)
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
            packet_has_shift = True
            packets_with_shift.append(packet.packet_id)
            decision.state_vector_shifts.append(
                StateVectorShift(
                    packet_id=packet.packet_id,
                    shift_type="continuity_shift",
                    payload=shift_payload,
                )
            )

        thread_payload = _extract_open_thread(packet)
        if thread_payload:
            packet_has_thread = True
            packets_with_open_thread.append(packet.packet_id)
            decision.open_threads.append(
                OpenThread(
                    packet_id=packet.packet_id,
                    thread_type="unresolved_thread",
                    payload=thread_payload,
                )
            )

        if not packet_has_crystal and not packet_has_shift and not packet_has_thread:
            fully_burned_packets.append(packet.packet_id)
            decision.burned_residue.append(
                BurnedResidue(
                    packet_id=packet.packet_id,
                    residue_type="fully_burned",
                    payload={"metadata": packet.metadata},
                )
            )

    decision.metadata = {
        "operator_id": inp.operator_id,
        "session_id": inp.session_id,
        "packets_total": len(inp.packets),
        "packets_with_crystal": packets_with_crystal,
        "packets_with_shift": packets_with_shift,
        "packets_with_open_thread": packets_with_open_thread,
        "fully_burned_packets": fully_burned_packets,
    }

    dominant_shift = decision.state_vector_shifts[0] if decision.state_vector_shifts else None
    dominant_crystal = decision.crystal_candidates[0] if decision.crystal_candidates else None
    dominant_thread = decision.open_threads[0] if decision.open_threads else None

    decision.operator_essence_delta = OperatorEssenceDelta(
        dominant_state_shift={
            "packet_id": dominant_shift.packet_id,
            "shift_type": dominant_shift.shift_type,
            "payload": dominant_shift.payload,
        } if dominant_shift else {},
        dominant_crystal_principle={
            "packet_id": dominant_crystal.packet_id,
            "principle": dominant_crystal.principle,
            "support": dominant_crystal.support,
        } if dominant_crystal else {},
        dominant_open_thread={
            "packet_id": dominant_thread.packet_id,
            "thread_type": dominant_thread.thread_type,
            "payload": dominant_thread.payload,
        } if dominant_thread else {},
    )

    decision.rationale.append("distillation_extracts_only_structural_outputs")
    decision.rationale.append("operator_essence_delta_is_minimal_not_total_memory")
    decision.rationale.append("non_structural_material_is_burned_not_stored")
    return decision
