"""Generate and visualize synthetic blob data."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_blobs


FIXED_CENTERS = np.array(
    [
        (-2.0, 1.5),
        (2.5, 3.5),
    ],
    dtype=float,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Gaussian blobs and display a scatter plot."
    )
    parser.add_argument(
        "--samples-per-class",
        type=int,
        default=1500,
        help="Samples to generate for each class (default: 1500).",
    )
    parser.add_argument(
        "--cluster-std",
        type=float,
        default=0.6,
        help="Standard deviation of each cluster (default: 0.6).",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=0,
        help="Seed the RNG for reproducibility; use None to disable (default: 0).",
    )
    return parser.parse_args()


def sample_blobs(
    samples_per_class: int = 1500,
    cluster_std: float = 0.6,
    random_state: int | None = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return deterministic blob samples as x, y coordinates and labels."""
    n_classes = len(FIXED_CENTERS)
    total_samples = samples_per_class * n_classes
    features, labels = make_blobs(
        n_samples=total_samples,
        centers=FIXED_CENTERS,
        n_features=2,
        cluster_std=cluster_std,
        random_state=random_state,
        shuffle=False,
    )
    x_coords = features[:, 0]
    y_coords = features[:, 1]
    return x_coords, y_coords, labels


def report_blobs(x_coords: np.ndarray, y_coords: np.ndarray, labels: np.ndarray) -> None:
    features = np.column_stack((x_coords, y_coords))
    n_samples, n_features = features.shape
    cluster_ids, counts = np.unique(labels, return_counts=True)
    print(
        f"Generated {n_samples} samples with {n_features} features in {len(cluster_ids)} classes."
    )
    for cluster_id, count in zip(cluster_ids, counts):
        centroid = features[labels == cluster_id].mean(axis=0)
        centroid_fmt = ", ".join(f"{value:.2f}" for value in centroid)
        print(f"  Class {cluster_id}: {count} samples, centroid=({centroid_fmt})")


def plot_blobs(x_coords: np.ndarray, y_coords: np.ndarray, labels: np.ndarray) -> None:
    features = np.column_stack((x_coords, y_coords))
    if features.shape[1] != 2:
        raise ValueError("Visualization only supports 2-D features (x and y).")
    plt.figure(figsize=(8, 6))
    plt.scatter(features[:, 0], features[:, 1], c=labels, cmap="viridis", s=10, alpha=0.8)
    plt.title("Synthetic Two-Class Blobs")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()
    backend = matplotlib.get_backend().lower()
    if "agg" in backend:
        output_path = Path("blobs.png")
        plt.savefig(output_path, dpi=150)
        print(
            f"Backend '{backend}' is non-interactive; saved plot to {output_path.resolve()}."
        )
    else:
        plt.show()


def main() -> None:
    args = parse_args()
    x_coords, y_coords, labels = sample_blobs(
        samples_per_class=args.samples_per_class,
        cluster_std=args.cluster_std,
        random_state=args.random_state,
    )
    report_blobs(x_coords, y_coords, labels)
    plot_blobs(x_coords, y_coords, labels)


if __name__ == "__main__":
    main()
