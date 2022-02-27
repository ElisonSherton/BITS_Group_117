import re
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description = "Process Log files")
parser.add_argument("--question", type = str, help = "Question Number for which to preprocess the logs")
args = parser.parse_args()

log_files = [x for x in Path("./").glob("**/*") if args.question in x.name]

def parse_log(pth):
    lines = pth.read_text().split("\n")
    lines = [l for l in lines if "moved from READY to RUNNING state" in l]
    process_sequence = [re.findall(r': (P\d)\(\d\)', l)[0] for l in lines]
    return process_sequence

for f in log_files:
    print(f)
    process_sequence = parse_log(f)
    print(" ".join(process_sequence))