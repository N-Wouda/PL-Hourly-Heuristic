def max_capacity(room_capacity: int,
                 max_batch: int,
                 is_self_study: bool) -> int:
    """
    Computes the maximum room capacity, subject to constraints.
    """
    if is_self_study:
        return room_capacity

    return min(max_batch, room_capacity)
