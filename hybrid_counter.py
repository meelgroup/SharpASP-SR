import os, glob, argparse, subprocess, math

parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input ASP file', required=True)
parser.add_argument('-t','--t', help='total time', default=5000, required=False)
parser.add_argument('-n','--n', help='threshold', default=10000, required=False)
parser.add_argument('-c','--c', help='counter', default="SharpASP-SR", required=False)
args = parser.parse_args()
python_path = "python"

def get_time(file, solver):
    file_name = os.path.basename(file)
    res_dir = "."
    output_file = res_dir + "/" + solver + "_" + \
        file_name[len("result-"):-len(".out")] + ".timeout"
    time = subprocess.Popen('grep "User time (seconds)" {0}'.format(
        output_file), shell=True, stdout=subprocess.PIPE).stdout
    time = time.read().decode("utf-8").strip().split()
    user_time = float(time[-1])

    time = subprocess.Popen('grep "System time (seconds)" {0}'.format(
        output_file), shell=True, stdout=subprocess.PIPE).stdout
    time = time.read().decode("utf-8").strip().split()
    system_time = float(time[-1])
    return user_time + system_time

os.system('echo "Setting Enumeration time: {0}" >> result-{1}.out'.format(args.t, args.i))
os.system('echo "Running counter: {0}" >> result-{1}.out'.format(args.c, args.i))
# it is one version
# os.system('./clingo -n 0 --time-limit {0} -q {1} >> result-{1}.out'.format(args.t, args.i))
# it is second version
os.system('clingo -n {0} --time-limit {1} -q {2} >> result-{2}.out'.format(args.n, args.t, args.i))

out_file = open('result-{0}.out'.format(args.i))

nSol = None
runCounter = False
execution_time = 0
time = None
for line in out_file:
    if line.startswith("Models"):
        l = line.strip().split(":")
        if l[-1].endswith("+"):
            runCounter = True
            l[-1] = l[-1][:-1]
        nSol = int(l[-1])
    elif line.startswith("CPU Time"):
        time = line.strip().split()[-1][:-1]

out_file.close()

execution_time = float(time)
if runCounter == True:
    nSol = None
    os.system('echo "Time remaining for {2}: {0}" >> result-{1}.out'.format(5000 - execution_time, args.i, args.c))
    if args.c == "SharpASP-SR":
        os.system('{0} run_sharpASPSR.py -i {1} -t {2} >> result-{1}.out'.format(python_path, args.i, math.ceil(5000 - execution_time)))
    else:
        assert(False)
    out_file = open('result-{0}.out'.format(args.i))
    for line in out_file:
        if args.c == "SharpASP-SR":
            if line.startswith("SharpASP-SR: Number of answer sets:"):
                l = line.split()
                nSol = int(l[-1])
            elif line.startswith("SharpASP-SR: Total time"):
                l = line.split()
                sharpasp_time = float(l[-1])
    out_file.close()
    
    if nSol != None:
        if args.c == "SharpASP-SR":
            execution_time += sharpasp_time 
        print("Solved by hybrid >> Answer sets: {0}".format(int(nSol), args.i))
        print("Solved by hybrid >> Execution time: {0}".format(execution_time, args.i))
    else:
        print("Unsolved by hybrid")
else:
    print("Solved by hybrid >> Answer sets: {0}".format(nSol, args.i))
    print("Solved by hybrid >> Execution time: {0}".format(execution_time, args.i))