"""Deterministic FIFO/SPT/LPT priorities under the strict hospital scheduler."""

from __future__ import annotations

from typing import Any, Literal

from .model import InstanceContext
from .scheduler import schedule_instance_solution


Rule = Literal["fifo", "spt", "lpt"]


def construct_baseline(context: InstanceContext, rule: Rule) -> dict[str, Any]:
    """Choose the earliest feasible completion for each job in rule order.

    SPT and LPT rank by the sum of both processing durations. If the next
    preferred job cannot meet max_wait now, it is deferred until a later step.
    Room pairs are free and the strict simulator verifies the final schedule.
    """
    if rule not in ("fifo", "spt", "lpt"):
        raise ValueError(f"unknown baseline rule: {rule}")
    jobs = {job.job_id: job for job in context.jobs}
    order = [job.job_id for job in context.jobs]
    if rule != "fifo":
        order.sort(key=lambda job_id: (
            sum(op.duration for op in jobs[job_id].operations)
            * (1 if rule == "spt" else -1), job_id
        ))
    room_release = {room: 0.0 for room in context.rooms}
    personnel_release = {
        person: 0.0 for _, people in context.personnel_by_operation for person in people
    }
    pending = list(order)
    sequence: list[int] = []
    assignments: dict[int, dict[int, str]] = {}

    while pending:
        selected = None
        for job_id in pending:
            anesthesia, surgery = jobs[job_id].operations
            person_1 = min(anesthesia.eligible_personnel,
                           key=lambda person: (personnel_release[person], person))
            person_2 = min(surgery.eligible_personnel,
                           key=lambda person: (personnel_release[person], person))
            options = []
            for room_1 in anesthesia.eligible_rooms:
                setup_start = max(room_release[room_1], personnel_release[person_1])
                anesthesia_finish = (
                    setup_start + max(anesthesia.transition, anesthesia.setup)
                    + anesthesia.duration + anesthesia.cleanup
                )
                for room_2 in surgery.eligible_rooms:
                    surgery_setup = max(
                        anesthesia_finish, room_release[room_2], personnel_release[person_2]
                    )
                    surgery_start = surgery_setup + max(surgery.transition, surgery.setup)
                    wait = surgery_start - anesthesia_finish
                    if wait > surgery.max_wait:
                        continue
                    finish = surgery_start + surgery.duration + surgery.cleanup
                    options.append((finish, wait, room_1, room_2, surgery_start))
            if options:
                selected = (job_id, person_1, person_2, min(options))
                break
        if selected is None:
            raise ValueError(f"no feasible completion for {context.instance_id} using {rule}")
        job_id, person_1, person_2, (finish, _, room_1, room_2, surgery_start) = selected
        pending.remove(job_id)
        sequence.append(job_id)
        assignments[job_id] = {1: room_1, 2: room_2}
        room_release[room_1] = finish if room_1 == room_2 else surgery_start
        room_release[room_2] = finish
        personnel_release[person_1] = surgery_start
        personnel_release[person_2] = finish

    solution = {"job_sequence_base": sequence, "room_assignment": assignments}
    schedule_instance_solution(context, solution)
    return solution


__all__ = ["construct_baseline"]
