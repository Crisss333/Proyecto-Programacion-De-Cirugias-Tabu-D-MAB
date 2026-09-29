"""Random-key encoding and strict, flexible room decoder.

Adapted from the team's exploratory modules. Room choices are independent for
the two stages; the decoder repairs preferences to preserve max_wait.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .model import InstanceContext


LOWER_BOUND = -5.0
UPPER_BOUND = 5.0


def decode_raw(position: np.ndarray, context: InstanceContext) -> dict[str, Any]:
    job_ids = [job.job_id for job in context.jobs]
    n = len(job_ids)
    dimension = n + sum(len(job.operations) for job in context.jobs)
    if len(position) != dimension:
        raise ValueError(f"expected {dimension} random keys")
    sequence = [job_ids[i] for i in np.argsort(position[:n])]
    assignments: dict[int, dict[int, str]] = {}
    key_index = n
    for job in context.jobs:
        assignments[job.job_id] = {}
        for operation in job.operations:
            eligible = operation.eligible_rooms
            normalized = (position[key_index] - LOWER_BOUND) / (UPPER_BOUND - LOWER_BOUND)
            normalized = min(max(normalized, 0.0), 1.0 - 1e-9)
            assignments[job.job_id][operation.operation_id] = eligible[int(normalized * len(eligible))]
            key_index += 1
    return {"job_sequence_base": sequence, "room_assignment": assignments}


def encode_solution(solution: dict[str, Any], context: InstanceContext) -> np.ndarray:
    """Choose the midpoint of each discrete random-key cell."""
    job_ids = [job.job_id for job in context.jobs]
    order = {job_id: rank for rank, job_id in enumerate(solution["job_sequence_base"])}
    n = len(job_ids)
    keys = np.empty(n + sum(len(job.operations) for job in context.jobs), dtype=float)
    for index, job_id in enumerate(job_ids):
        keys[index] = -4.5 + 9.0 * order[job_id] / max(1, n - 1)
    index = n
    for job in context.jobs:
        for operation in job.operations:
            eligible = operation.eligible_rooms
            room = solution["room_assignment"][job.job_id][operation.operation_id]
            room_index = eligible.index(room)
            keys[index] = LOWER_BOUND + (UPPER_BOUND - LOWER_BOUND) * (
                room_index + 0.5
            ) / len(eligible)
            index += 1
    return keys


def decode_feasible(position: np.ndarray, context: InstanceContext) -> dict[str, Any]:
    """Repair room preferences while enforcing the strict wait constraint.

    If a preferred job cannot be scheduled now, try later jobs. For a chosen
    job, select the feasible room pair that deviates least from the raw keys.
    No room balance or same-room condition is imposed. An unrepairable input
    is returned as raw and will be rejected by the strict evaluator.
    """
    raw = decode_raw(position, context)
    jobs = {job.job_id: job for job in context.jobs}
    pending = list(raw["job_sequence_base"])
    room_release = {room: 0.0 for room in context.rooms}
    personnel_release = {
        person: 0.0 for _, people in context.personnel_by_operation for person in people
    }
    assignments: dict[int, dict[int, str]] = {}
    sequence: list[int] = []
    while pending:
        selected = None
        for job_id in pending:
            anesthesia, surgery = jobs[job_id].operations
            preferred = raw["room_assignment"][job_id]
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
                    if surgery_start - anesthesia_finish > surgery.max_wait + 1e-9:
                        continue
                    finish = surgery_start + surgery.duration + surgery.cleanup
                    deviation = (room_1 != preferred[1]) + (room_2 != preferred[2])
                    options.append((deviation, finish, room_1, room_2, surgery_start))
            if options:
                selected = (job_id, person_1, person_2, min(options))
                break
        if selected is None:
            return raw
        job_id, person_1, person_2, (_, finish, room_1, room_2, surgery_start) = selected
        pending.remove(job_id)
        sequence.append(job_id)
        assignments[job_id] = {1: room_1, 2: room_2}
        room_release[room_1] = finish if room_1 == room_2 else surgery_start
        room_release[room_2] = finish
        personnel_release[person_1] = surgery_start
        personnel_release[person_2] = finish
    return {"job_sequence_base": sequence, "room_assignment": assignments}
