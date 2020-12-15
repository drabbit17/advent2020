import collections


def problem10a(data):
    sorted_data = sorted([int(e) for e in data])
    last_point, differences = 0, []
    for idx, adapter in enumerate(sorted_data):
        differences.append(adapter - last_point)
        last_point = sorted_data[idx]
    # add device difference
    differences.append(3)
    diffs_counts = collections.Counter(differences)
    return diffs_counts[1] * diffs_counts[3]


def problem10b(data):
    def get_possible_paths_count(current_jolt, sorted_adapters):
        possible_paths_count = 0

        if not sorted_adapters:
            return 1

        for idx, adapter in enumerate(sorted_adapters):
            if (adapter - current_jolt) <= 3:
                adapter_paths_count = memory.get(adapter)
                if not adapter_paths_count:
                    adapter_paths_count = get_possible_paths_count(
                        adapter, sorted_adapters[(idx + 1) :]  # noqa: E203
                    )  # noqa: E203
                    memory[adapter] = adapter_paths_count
                possible_paths_count += adapter_paths_count
        return possible_paths_count

    sorted_adapters = sorted([int(e) for e in data])
    sorted_adapters.append(max(sorted_adapters) + 3)
    memory = {}
    paths_count = get_possible_paths_count(0, sorted_adapters)
    return paths_count
