import argparse
from wheatvol.cli import run_all

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    args = p.parse_args()
    run_all(args.config)
