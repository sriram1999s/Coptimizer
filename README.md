# Coptimizer : Automated Tool For  C Source Optimization.

>**NOTE :** Combinations of optimizations do not work currently due to implementation issues.

## Optimizations
> The optimizations are goverened by Jon Bentley's rules for optimizing work.

Find the link to a pdf explaining the rules [here](http://progforperf.github.io/Bentley_Rules.pdf)

  - Function Inlining
  - Loop Unrolling
  - Combining Tests(If-Else to Switch)
  - Compile Time Initialization
  - Tail End Recursion Elimination
  - Loop Jamming

# Interfaces
  - [Command Line Utility](#Command-Line-Utility)
  - [Online Graphical User Interface](#GUI)

# Command Line Utility
Is a software tool with command line interface

## Dependancies

  - Python3.6+
  - linux

## Functionalities
  - [help](#Help)
  - [set flags](###Set-Flags)
  - [optimize](###Optimize)

## Installation

1. Clone the repository
2. Run the install script (install.sh)
3. add this to your shell config file : ```export PATH=$PATH":<enter-path-to-directory>/env```
4. add this to your shell config file : ```export COPTIMIZER_PATH="<enter-path-to-directory>"```

To verify installation type:
```sh
Coptimizer help
```

The output should look like this:
```sh

Welcome to the command line Coptimizer....🔥

Usage sf ➡️  Coptimizer sf [FLAGS]
Usage ox ➡️  Coptimizer ox [PATH]
sf [options] ➡️  setflags in from this pool [UNROLL,COMPILE_INIT,INLINE,IF_TO_SWITCH,TAIL_RECURSION,JAMMING]
ox [PATH] ➡️  optimize file in given path and create output.c file in same path

```

## Usage

### Help

provides general information about the interface

```shell
Coptimizer help
```

### Set flags

Set flags for selected optimization [found here](#Optimizations)
Used to select which optimizations are applied on the next run.

```shell
Coptimizer sf <flags list>
```
Use [help](#Help) to see flags options

### Optimize

Optimizes input source code. Outputs processed source code to stdout and stores it in output.c

```shell
Coptimizer ox <path to file>
```

# GUI

Is a graphical user interface provided by the Coptimizer server

Find the link for the demonstration [here](https://www.youtube.com/watch?v=Oyf43YoXJuI)

![User Interface](https://github.com/sriram1999s/Capstone/blob/third_echelon/images/ui1.png?raw=true)
