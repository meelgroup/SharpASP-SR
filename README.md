# SharpASP-SR 
SharpASP-SR is an answer set counter for disjunctive logic programs. The publication is here: [ICLP25](https://www.cambridge.org/core/journals/theory-and-practice-of-logic-programming/article/counting-answer-sets-of-disjunctive-answer-set-programs/2695D99F659828956391D95B409E6448)

# Clone the repo
```
git clone --recurse-submodules https://github.com/meelgroup/SharpASP-SR.git
```

# Dependencies
Install:
```
sudo apt-get install -y build-essential gringo python3-pip
```


# Build and Download ganak
SharpASP-SR uses ganak as projected model counter. The _best_ way to obtain ganak is to obtain its released static binaries from [https://github.com/meelgroup/ganak](https://github.com/meelgroup/ganak). 

Build all required binaries as follows:
```
chmod +x build.sh
./build.sh
```

The `build.sh` compiles required binaries and also downloads a compiled binary of [ganak](https://github.com/meelgroup/ganak).


# Run sharpASP-SR
execute `run_sharpASPSR.py` as follows:
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
The benchmark and experimental logfiles are available at: [zenodo link](https://zenodo.org/records/19640592)

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