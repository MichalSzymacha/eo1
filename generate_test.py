import json
import itertools


def load_configurations(json_file):
    with open(json_file, "r") as f:
        config = json.load(f)
    return config


def generate_configurations(config):
    # Wybieramy klucze, dla których mamy listy wartości
    keys = list(config.keys())
    # Tworzymy listę list wartości dla każdego klucza; dla pojedynczych wartości (np. vars_number) możemy opakować je w listę, jeśli nie są już listą
    values = [
        config[key] if isinstance(config[key], list) else [config[key]] for key in keys
    ]

    # Wygeneruj wszystkie kombinacje przy użyciu product
    for combination in itertools.product(*values):
        yield dict(zip(keys, combination))


# Przykład użycia:
if __name__ == "__main__":
    config = load_configurations("test.json")
    all_configs = list(generate_configurations(config))
    print(f"Liczba wygenerowanych konfiguracji: {len(all_configs)}")
    with open("all_configs.json", "w") as f:
        json.dump(all_configs, f, indent=4)

    # Możesz teraz iterować po all_configs i wykonywać testy dla każdej konfiguracji.
