import json
import os
import glob
import pandas as pd


def aggregate_results(results_root="results"):
    """
    Przechodzi przez wszystkie foldery konfiguracji w folderze 'results'
    oraz wczytuje dane z plików 'wyniki.csv' z każdego uruchomienia.
    Zwraca DataFrame z uśrednionymi wynikami oraz najlepszym i najgorszym wynikiem.
    """
    config_results = []

    # Przeglądamy wszystkie foldery konfiguracji (np. "rastrigin_ab12cd34")
    config_folders = glob.glob(os.path.join(results_root, "*"))
    for config_folder in config_folders:
        config_name = os.path.basename(config_folder)
        run_folders = glob.glob(os.path.join(config_folder, "*"))

        best_values = []
        mean_values = []
        best_vectors = []
        best_time = []
        # Jeśli masz zapisane inne metryki (np. czas obliczeń), możesz je również zbierać.

        # Przetwarzamy każdy folder z uruchomieniem (np. "0", "1", ...)
        for run_folder in run_folders:
            wyniki_path = os.path.join(run_folder, "wyniki.csv")
            if os.path.exists(wyniki_path):
                # Załóżmy, że CSV nie ma nagłówka i kolumny to:
                # [epoch, best_value, mean_value, std_value]
                df = pd.read_csv(wyniki_path, header=None)
                # Pobieramy ostatni wiersz z wynikami (wyniki końcowe)
                last_row = df.iloc[-1]
                try:
                    best_val = float(last_row[1])
                    mean_val = float(last_row[2])
                except ValueError:
                    # Jeśli wystąpi problem z konwersją, pomiń ten wynik
                    continue

                best_values.append(best_val)
                mean_values.append(mean_val)

            wyniki_path = os.path.join(run_folder, "wyniki.json")
            if os.path.exists(wyniki_path):
                # Załóżmy, że JSON zawiera klucz "best_solution_vector" i "time"
                with open(wyniki_path, "r") as f:
                    data = json.load(f)
                    best_vector = data.get("best_solution_vector", None)
                    time = data.get("time", None)

                if best_vector is not None:
                    best_vectors.append(best_vector)
                if time is not None:
                    best_time.append(time)

        if best_values:
            # Dla minimizacji najlepszy wynik to najmniejsza wartość
            best_run = min(best_values)
            worst_run = max(best_values)
            avg_best = sum(best_values) / len(best_values)
            avg_mean = sum(mean_values) / len(mean_values)

            config_results.append(
                {
                    "Configuration": config_name,
                    "Best Result": best_run,
                    "Average Best": avg_best,
                    "Worst Result": worst_run,
                    "Average Mean": avg_mean,
                    "Runs": len(best_values),
                    "Best Vector": best_vectors[best_values.index(best_run)],
                    "Best Time": best_time[best_values.index(best_run)],
                }
            )

    return pd.DataFrame(config_results)


if __name__ == "__main__":
    # Agregujemy wyniki ze wszystkich konfiguracji
    summary_df = aggregate_results("cec2014_f5_results")
    print(summary_df)

    # Zapisujemy tabelę do pliku CSV, który można wykorzystać do sprawozdania
    summary_df.to_csv("summary_f5_results.csv", index=False)
    summary_df.to_excel("summary_f5_results.xlsx", index=False)
