import os, argparse, subprocess, shutil

parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input ASP program', required=True)
parser.add_argument('-t','--t', help='timeout', default=5000, required=False)
args = parser.parse_args()
ganak_binary = 'ganak'
clark = 'clark'
if not os.path.exists('./{0}'.format(ganak_binary)):
    print("Tool {0} does not exist".format(ganak_binary))
    exit(1)

if shutil.which("gringo"):
    # print("Gringo Installed")
    pass
else:
    print("gringo is not installed. Please install gringo")
    exit(1)

if not os.path.exists('./{0}'.format(clark)):
    print("Tool {0} does not exist".format(clark))
    exit(1)

if not os.path.exists(args.i):
    print('input ' + args.i + ' does not exist')
    exit(1)

os.system('gringo -o smodels {0} | ./clark -dimacs -output {0}'.format(args.i))

if not os.path.exists('model_' + args.i + '.out'):
    print('Cannot compute formulas phi_1 and phi_2 !!!')
    print('Some issue with input file')
    print('model_' + args.i + '.out does not exist')
    exit(1)

if not os.path.exists('non_sm_' + args.i + '.out'):
    print('Cannot compute formulas phi_1 and phi_2 !!!')
    print('Some issue with input file')
    print('non_sm_' + args.i + '.out does not exist')
    exit(1)

def get_time(file, solver):
    file_name = os.path.basename(file)
    res_dir = "."
    output_file = res_dir + "/" + solver + "_" + \
        file_name[len("output_"):-len(".out")] + ".timeout"
    time = subprocess.Popen('grep "User time (seconds)" {0}'.format(
        output_file), shell=True, stdout=subprocess.PIPE).stdout
    time = time.read().decode("utf-8").strip().split()
    user_time = float(time[-1])

    time = subprocess.Popen('grep "System time (seconds)" {0}'.format(
        output_file), shell=True, stdout=subprocess.PIPE).stdout
    time = time.read().decode("utf-8").strip().split()
    system_time = float(time[-1])
    return user_time + system_time


total_time = int(args.t)
first_count = None
first_time = None
second_count = None
second_time = None

print('The formulas phi_1 and phi_2 are computed already !!!')
# count the models of the first formula
# print('timeout {0}s /usr/bin/time --verbose -o first_{2}.timeout ./{1} -v 0 --maxcache 4000 model_{2}.out > output_{2}.out'.format(total_time, ganak_binary, args.i))
print('Invoking the first counter call ... ')
os.system('timeout {0}s /usr/bin/time --verbose -o first_{2}.timeout ./{1} --verb 0 --prob 0 --maxcache 4000 model_{2}.out > output_{2}.out'.format(total_time, ganak_binary, args.i))

out_file = open('output_{0}.out'.format(args.i))
for line in out_file:
    if line.startswith("c s exact arb int"):
        l = line.strip().split()
        first_count = int(l[-1])

out_file.close()
if first_count == None:
    # indicate unsolved
    print("SharpASP-SR timeouted")
    exit(1)
else:
    first_time = get_time("output_{0}.out".format(args.i), "first")
    print("SharpASP-SR: first count done, count: {0} and time: {1}".format(first_count, first_time))


# count the (projected) models of the second formula
total_time = total_time - first_time # remaining time
if (total_time <= 0):
    # indicate unsolved
    print("SharpASP-SR timeouted")
    exit(1)

print('Invoking the second counter call ... ')
# print('timeout {0}s /usr/bin/time --verbose -o second_{2}.timeout ./{1} -v 0 --maxcache 4000 non_sm_{2}.out > output_{2}.out'.format(total_time, ganak_binary, args.i))
os.system('timeout {0}s /usr/bin/time --verbose -o second_{2}.timeout ./{1} --verb 0 --prob 0 --maxcache 4000 non_sm_{2}.out > output_{2}.out'.format(total_time, ganak_binary, args.i))
out_file = open('output_{0}.out'.format(args.i))
for line in out_file:
    if line.startswith("c s exact arb int"):
        l = line.strip().split()
        second_count = int(l[-1])

out_file.close()
if second_count == None:
    # indicate unsolved
    print("SharpASP-SR timeouted")
    exit(1)
else:
    second_time = get_time("output_{0}.out".format(args.i), "second")
    print("SharpASP-SR: second count done, count: {0} and time: {1}".format(second_count, second_time))

if first_count != None and second_count != None:
    print("SharpASP-SR: Number of answer sets: {0}".format(first_count - second_count))
    print("SharpASP-SR: Total time: {0}".format(first_time + second_time))

os.system('rm second_{0}.timeout first_{0}.timeout'.format(args.i))