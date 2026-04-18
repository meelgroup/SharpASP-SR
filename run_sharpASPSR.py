#!/usr/bin/env python3

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="input ASP program")
parser.add_argument("-t", "--timeout", type=float, default=5000, help="timeout in seconds")
args = parser.parse_args()

ganak_binary = Path("./ganak")
clark_binary = Path("./clark")
input_file = Path(args.input)

if not ganak_binary.exists():
    print(f"Tool {ganak_binary} does not exist")
    sys.exit(1)

if shutil.which("gringo") is None:
    print("gringo is not installed. Please install gringo")
    sys.exit(1)

if not clark_binary.exists():
    print(f"Tool {clark_binary} does not exist")
    sys.exit(1)

if not input_file.exists():
    print(f"input {input_file} does not exist")
    sys.exit(1)


def run_command(cmd, stdout_file=None):
    try:
        if stdout_file is None:
            result = subprocess.run(cmd, check=True, text=True, capture_output=True)
            return result.stdout
        else:
            with open(stdout_file, "w", encoding="utf-8") as f:
                subprocess.run(cmd, check=True, text=True, stdout=f)
            return None
    except subprocess.CalledProcessError as e:
        print("Command failed:")
        print(" ".join(str(x) for x in cmd))
        if e.stderr:
            print(e.stderr)
        sys.exit(1)


def parse_count(output_file):
    with open(output_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("c s exact arb int"):
                parts = line.strip().split()
                return int(parts[-1])
    return None


def run_ganak(formula_file, output_file, timeout_seconds):
    start = time.time()
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            subprocess.run(
                [
                    str(ganak_binary),
                    "--verb", "0",
                    "--prob", "0",
                    "--maxcache", "4000",
                    str(formula_file),
                ],
                check=True,
                text=True,
                stdout=f,
                timeout=timeout_seconds,
            )
    except subprocess.TimeoutExpired:
        print("SharpASP-SR timed out")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("SharpASP-SR failed while running ganak")
        sys.exit(1)

    elapsed = time.time() - start
    count = parse_count(output_file)
    if count is None:
        print("SharpASP-SR timed out")
        sys.exit(1)

    return count, elapsed


# compute phi_1 and phi_2
with open(input_file, "r", encoding="utf-8") as f:
    gringo = subprocess.Popen(
        ["gringo", "-o", "smodels", str(input_file)],
        stdout=subprocess.PIPE,
        text=False,
    )
    subprocess.run(
        [str(clark_binary), "-dimacs", "-output", str(input_file)],
        stdin=gringo.stdout,
        check=True,
    )
    gringo.stdout.close()
    gringo.wait()

model_file = Path(f"model_{input_file}.out")
non_sm_file = Path(f"non_sm_{input_file}.out")

if not model_file.exists():
    print("Cannot compute formulas phi_1 and phi_2 !!!")
    print("Some issue with input file")
    print(f"{model_file} does not exist")
    sys.exit(1)

if not non_sm_file.exists():
    print("Cannot compute formulas phi_1 and phi_2 !!!")
    print("Some issue with input file")
    print(f"{non_sm_file} does not exist")
    sys.exit(1)

print("The formulas phi_1 and phi_2 are computed already !!!")

total_time = args.timeout

print("Invoking the first counter call ... ")
first_count, first_time = run_ganak(
    model_file,
    f"output_{input_file}.out",
    total_time,
)
print(f"SharpASP-SR: first count done, count: {first_count} and time: {first_time}")

remaining_time = total_time - first_time
if remaining_time <= 0:
    print("SharpASP-SR timed out")
    sys.exit(1)

print("Invoking the second counter call ... ")
second_count, second_time = run_ganak(
    non_sm_file,
    f"output_{input_file}.out",
    remaining_time,
)
print(f"SharpASP-SR: second count done, count: {second_count} and time: {second_time}")

print(f"SharpASP-SR: Number of answer sets: {first_count - second_count}")
print(f"SharpASP-SR: Total time: {first_time + second_time}")