import csv
import os


def clear_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["epoch", "best", "mean", "std"])


def save_results_to_csv(filename, *args):
    with open(filename, mode="a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(args)
