# SharpASP-SR 
SharpASP-SR is an answer set counter for disjunctive logic programs. The publication is here: [ICLP25](https://www.cambridge.org/core/journals/theory-and-practice-of-logic-programming/article/counting-answer-sets-of-disjunctive-answer-set-programs/2695D99F659828956391D95B409E6448)

# Clone the repo
```
git clone --recurse-submodules git@github.com:meelgroup/SharpASP-SR.git
```

# Dependencies
- **Ganak** The recommeneded way to have Ganak is to obtain its released binaries from their [github](https://github.com/meelgroup/ganak). The `bin` directory also has a ganak binary. 
- **Clark**: The clark completion and copy operation implementation is given with submodule in the directory `Compl`
- **gringo**: we used gringo as grounder. You can install it from [potassco](https://potassco.org/clingo/). One static binary of gringo is in the `bin` directory.

# Build Compl
First you need to build Compl. This is the implementation to run Clark completion and copy operations. 
```
cd Compl
make
```
After compling, you should see the binary `clark` in the directory.

# Run sharpASP-SR

Make sure that the binaries (`ganak`, `gringo`, and `clark`) are present in the current directory.

**Run:** execute `run_sharpASPSR.py` as follow:
```
python run_sharpASPSR.py -i Snf1_pathway.bnet.lp
```
Finally the output will be as follows:
```
SharpASP-SR: Number of answer sets: 10096027719780900754667077632
SharpASP-SR: Total time: XXX
```
The input program has `10096027719780900754667077632` answer sets.


# Benchmark and Experimental logfiles
The benchmark and experimental logfiles are available at: [zenodo link](https://zenodo.org/records/15710200)

# Publication

```
@article{KCM2025,
  title={Counting Answer Sets of Disjunctive Answer Set Programs},
  author={Kabir, Md Mohimenul and Chakraborty, Supratik and Meel, Kuldeep S},
  journal={Theory and Practice of Logic Programming},
  volume={25},
  number={4},
  pages={703--721},
  year={2025},
  publisher={Cambridge University Press}
}
```