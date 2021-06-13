# Coptimizer : Automated Tool For  C Source Optimization.

## Optimizations
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

## Functionalities
  - [help](#Help)
  - [set flags](###Set-Flags)
  - [optimize](###Optimize)

## Installation
```python
print("Yet to complete :D")
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

Is a graphical user interface provided by the Coptimizer server:
[www.Coptimizer.com](#www.Coptimizer.com)

![User Interface][images/ui1.png]
