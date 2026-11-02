import csv
import time

COUNTS = [5_000, 20_000, 80_000]
QUERY_COUNT = 2_000
METHODS = ["list", "set", "dict"]


def queries_for(count):
    step = max(1, count // QUERY_COUNT)
    return list(range(0, count, step))[:QUERY_COUNT]


def list_lookup(values, queries):
    found = 0
    comparisons = 0
    for query in queries:
        for index, value in enumerate(values, start=1):
            comparisons += 1
            if value == query:
                found += 1
                break
    return found, comparisons


def set_lookup(values, queries):
    found = 0
    for query in queries:
        if query in values:
            found += 1
    return found, len(queries)


def dict_lookup(values, queries):
    found = 0
    for query in queries:
        if query in values:
            found += 1
    return found, len(queries)


FUNCTIONS = {
    "list": list_lookup,
    "set": set_lookup,
    "dict": dict_lookup,
}


def prepare(method, count):
    numbers = list(range(count))
    if method == "list":
        return numbers
    if method == "set":
        return set(numbers)
    return {number: True for number in numbers}


def repeats_for(count):
    if count <= 5_000:
        return 5
    if count <= 20_000:
        return 2
    return 1


def main():
    rows = []
    for count in COUNTS:
        repeats = repeats_for(count)
        queries = queries_for(count)
        for method in METHODS:
            container = prepare(method, count)
            started = time.perf_counter()
            comparisons = 0
            for _ in range(repeats):
                _, comparisons = FUNCTIONS[method](container, queries)
            seconds = (time.perf_counter() - started) / repeats
            rows.append([
                method,
                count,
                len(queries),
                repeats,
                round(seconds, 6),
                comparisons,
                round(len(queries) / seconds, 1),
            ])

    with open("benchmark_results.csv", "w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "method", "count", "queries", "repeats",
            "seconds", "comparisons", "lookups_per_second",
        ])
        writer.writerows(rows)

    print(len(rows), "measurements written")


if __name__ == "__main__":
    main()
