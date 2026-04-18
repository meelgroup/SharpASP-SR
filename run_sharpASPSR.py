#!/usr/bin/env python3

import os
import argparse
import subprocess
import shutil
import sys
import time


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--i", help="input ASP program", required=True)
parser.add_argument("-t", "--t", help="timeout", default=5000, required=False, type=float)
args = parser.parse_args()

ganak_binary = "ganak"
clark = "clark"

if not os.path.exists(f"./{ganak_binary}"):
    print(f"Tool {ganak_binary} does not exist")
    sys.exit(1)

if shutil.which("gringo") is None:
    print("gringo is not installed. Please install gringo")
    sys.exit(1)

if not os.path.exists(f"./{clark}"):
    print(f"Tool {clark} does not exist")
    sys.exit(1)

if not os.path.exists(args.i):
    print("input " + args.i + " does not exist")
    sys.exit(1)


# gringo -o smodels input | ./clark -dimacs -output input
try:
    gringo_proc = subprocess.Popen(
        ["gringo", "-o", "smodels", args.i],
        stdout=subprocess.PIPE,
    )
    clark_proc = subprocess.run(
        [f"./{clark}", "-dimacs", "-output", args.i],
        stdin=gringo_proc.stdout,
        check=True,
    )
    gringo_proc.stdout.close()
    gringo_proc.wait()
except subprocess.CalledProcessError:
    print("Failed to compute formulas phi_1 and phi_2 !!!")
    print("Some issue with input file")
    sys.exit(1)

if not os.path.exists("model_" + args.i + ".out"):
    print("Cannot compute formulas phi_1 and phi_2 !!!")
    print("Some issue with input file")
    print("model_" + args.i + ".out does not exist")
    sys.exit(1)

if not os.path.exists("non_sm_" + args.i + ".out"):
    print("Cannot compute formulas phi_1 and phi_2 !!!")
    print("Some issue with input file")
    print("non_sm_" + args.i + ".out does not exist")
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
                    f"./{ganak_binary}",
                    "--verb", "0",
                    "--prob", "0",
                    "--maxcache", "4000",
                    formula_file,
                ],
                stdout=f,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout_seconds,
                check=True,
            )
    except subprocess.TimeoutExpired:
        print("SharpASP-SR timeouted")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("SharpASP-SR failed")
        sys.exit(1)

    elapsed = time.time() - start
    count = parse_count(output_file)

    if count is None:
        print("SharpASP-SR timeouted")
        sys.exit(1)

    return count, elapsed


total_time = float(args.t)
first_count = None
first_time = None
second_count = None
second_time = None

print("The formulas phi_1 and phi_2 are computed already !!!")

print("Invoking the first counter call ... ")
first_count, first_time = run_ganak(
    "model_" + args.i + ".out",
    f"output_{args.i}.out",
    total_time,
)
print("SharpASP-SR: first count done, count: {0} and time: {1}".format(first_count, first_time))

total_time = total_time - first_time
if total_time <= 0:
    print("SharpASP-SR timeouted")
    sys.exit(1)

print("Invoking the second counter call ... ")
second_count, second_time = run_ganak(
    "non_sm_" + args.i + ".out",
    f"output_{args.i}.out",
    total_time,
)
print("SharpASP-SR: second count done, count: {0} and time: {1}".format(second_count, second_time))

print("SharpASP-SR: Number of answer sets: {0}".format(first_count - second_count))
print("SharpASP-SR: Total time: {0}".format(first_time + second_time))