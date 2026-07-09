#!/usr/bin/env python3

import os
import yaml

# ToDo: Make this more robust and agnostic of the file structure
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_yaml(config_file: str = "config/system.yaml"):
    config_path = os.path.join(ROOT, config_file)

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config


def main():
    config = load_yaml()
    print(config)


if __name__ == "__main__":
    main()
