import argparse, json
from target_of_understanding import process

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", type=str)
    args = ap.parse_args()
    print(json.dumps(process(args.text), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
