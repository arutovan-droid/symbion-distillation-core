from symbion_distillation import DistillationInput, DistillationPacket, distill_packets


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
