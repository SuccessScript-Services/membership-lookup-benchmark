import csv
import matplotlib.pyplot as plt

COLORS = {"list": "C0", "set": "C1", "dict": "C2"}


def load(path="benchmark_results.csv"):
    with open(path, newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for key in ("count", "queries", "repeats", "seconds", "comparisons", "lookups_per_second"):
            row[key] = float(row[key])
    return rows


def draw(axis, rows, ykey):
    for method in ("list", "set", "dict"):
        chosen = sorted((row for row in rows if row["method"] == method), key=lambda row: row["count"])
        axis.plot(
            [row["count"] for row in chosen],
            [row[ykey] for row in chosen],
            marker="o",
            color=COLORS[method],
            label=method,
        )
    axis.set_yscale("log")
    axis.set_xlabel("items in the collection")
    axis.legend()


def save(figure, path):
    figure.tight_layout()
    figure.savefig(path, dpi=140)
    plt.close(figure)
    print("saved", path)


def main():
    rows = load()
    figure, axis = plt.subplots(figsize=(8, 4.5))
    draw(axis, rows, "seconds")
    axis.set_ylabel("seconds (log scale)")
    axis.set_title("Membership lookup time by collection type")
    save(figure, "lookup_time.png")

    figure, axis = plt.subplots(figsize=(8, 4.5))
    draw(axis, rows, "comparisons")
    axis.set_ylabel("comparisons (log scale)")
    axis.set_title("Comparisons needed for the same queries")
    save(figure, "comparison_count.png")

    figure, axis = plt.subplots(figsize=(8, 4.5))
    draw(axis, rows, "lookups_per_second")
    axis.set_ylabel("lookups per second (log scale)")
    axis.set_title("Lookup throughput as the collection grows")
    save(figure, "throughput.png")


if __name__ == "__main__":
    main()
