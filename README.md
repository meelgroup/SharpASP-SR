# SharpASP-SR 
The codebase of answer set counter SharpASP-SR

# Run sharpASP-SR
**We run our experiments in linux systems**

Copy necessary binaries (`ganak`, `gringo`, `clark`) in the current folder:
```
cp bin/* .
```

__Please ensure that the binaries ganak, gringo, clark are executable (chmod +x), run_sharpASPSR.py is executable and they all are in the current directory__

**Run:** execute `run_sharpASPSR.py`:
```
python run_sharpASPSR.py -i Snf1_pathway.bnet.lp
```
Finally the output will be as follows:
```
SharpASP-SR: Number of answer sets: 10096027719780900754667077632
SharpASP-SR: Total time: XXX
```
The input program has `10096027719780900754667077632` answer sets.

# Source of Binary
- `ganak`: the propositional (projected) model counter --- compiled from Model Counting Competition 2024
- `clark`: clark completion + copy operation --- adapted from ASP solver [Cmodels](https://www.cs.utexas.edu/~tag/cmodels/)

# Benchmark and Experimental logfiles
The benchmark and experimental logfiles are available at: [zenodo link](https://zenodo.org/records/15710200)

