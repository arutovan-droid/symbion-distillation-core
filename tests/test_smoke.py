from symbion_distillation import DistillationInput, DistillationPacket, distill_packets
from symbion_distillation.types import DistillationDecision


def test_distillation_smoke():
    packets = [
        DistillationPacket(
            packet_id="p1",
            crystal_draft={"principle": "restore power"},
            continuity_event={"open_thread": True},
            state_vector={"mode": "recovery"},
        ),
        DistillationPacket(
            packet_id="p2",
            continuity_event={"unresolved": True},
        ),
        DistillationPacket(
            packet_id="p3",
        ),
    ]

    decision = distill_packets(
        DistillationInput(
            packets=packets,
            operator_id="op",
            session_id="s1",
        )
    )

    crystal_ids = [x.packet_id for x in decision.crystal_candidates]
    thread_ids = [x.packet_id for x in decision.open_threads]
    residue_ids = [x.packet_id for x in decision.burned_residue]

    assert "p1" in crystal_ids
    assert "p1" in thread_ids
    assert "p2" in thread_ids
    assert "p3" in residue_ids

    assert decision.metadata["packets_total"] == 3
    assert "p1" in decision.metadata["packets_with_crystal"]
    assert "p1" in decision.metadata["packets_with_shift"]
    assert "p1" in decision.metadata["packets_with_open_thread"]
    assert "p3" in decision.metadata["fully_burned_packets"]

    assert decision.operator_essence_delta.dominant_crystal_principle["packet_id"] == "p1"
    assert decision.operator_essence_delta.dominant_state_shift["packet_id"] == "p1"
    assert decision.operator_essence_delta.dominant_open_thread["packet_id"] == "p1"

    snapshot = decision.to_snapshot_dict()
    restored = DistillationDecision.from_snapshot_dict(snapshot)

    assert restored.metadata["packets_total"] == 3
    assert restored.operator_essence_delta.dominant_crystal_principle["packet_id"] == "p1"
    assert restored.operator_essence_delta.dominant_state_shift["packet_id"] == "p1"
    assert restored.operator_essence_delta.dominant_open_thread["packet_id"] == "p1"
    assert [x.packet_id for x in restored.crystal_candidates] == crystal_ids
