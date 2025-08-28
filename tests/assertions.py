def all_durations_equal(files, tolerance=0.01):
    durations = [f.get_duration() for f in files]
    first = durations[0]
    for i, d in enumerate(durations[1:], 1):
        assert abs(d - first) <= tolerance, f"Duration mismatch at index {i}: {d} vs {first}"
