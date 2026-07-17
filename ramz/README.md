# RAMZ Programming Language

Welcome to **RAMZ**, an open-source programming language built using **Python** and **C**.

Created by:

* GitHub: **redasaadcgt-sys**
* LinkedIn: **Reda Saad**

RAMZ is a custom compiler project that includes its own frontend, type checker, intermediate representation, and LLVM-based backend.

---

## Requirements

RAMZ depends on:

* Python
* msvc
* LLVM

---

## Installation and Setup

It is recommended to install RAMZ in the default system directory:

```text
C:\Program Files\Ramz
```

To configure RAMZ and install all required components, run:

```powershell
& "C:\Program Files\Ramz\scripts\setup.ps1"
```

The setup script will:

* Check system requirements
* Create the required Python environment
* Install RAMZ dependencies
* Configure LLVM
* Add required environment paths

---

## Cleanup

To remove RAMZ environment settings and paths:

```powershell
& "C:\Program Files\Ramz\scripts\clean_setup.ps1"
```

This will clean the configured paths and LLVM settings created during setup.

---

# Commands

RAMZ currently supports the following commands:

## Build

Compile a RAMZ source file:

```text
ramz build <source> <destination>
```

Example:

```powershell
ramz build examples/main.rz build
```

### Build options

```text
--trace  [options]
--dump  [options]
--stop-at <stage>
```

Available compiler stages:

```text
tokens
ast
ir
type-checker
llvm
```

If no stage is specified, all stages will be enabled.

---

## Run

Run a compiled RAMZ program:

```text
ramz run <build_directory>
```

### Run options

```text
--rebuild

--trace  [options]

--dump  [options]
```

---

## Kill

Terminate the running RAMZ process:

```text
ramz kill
```

---

# File Extensions

RAMZ source files can use either:

```text
.rz
```

or

```text
.rmz
```

---

# Project Configuration

RAMZ supports a configuration file named:

```text
ramz.toml
```

Create this file in the root directory of your project.

Example:

```toml
entry = "main.rz"
output = "program"
```

Supported settings:

| Setting  | Description                          |
| -------- | ------------------------------------ |
| `entry`  | The main source file to compile      |
| `output` | The name of the generated executable |

When `ramz.toml` exists, the `ramz build` and `ramz run` commands will automatically use these settings.

---

# Compiler Stages

RAMZ provides debugging tools to inspect different compiler stages:

```text
Source Code
    |
    v
Lexer
    |
    v
Parser
    |
    v
AST
    |
    v
Type Checker
    |
    v
IR
    |
    v
LLVM
    |
    v
Executable
```

Tracing and dumping options can be used to inspect the output of each stage during compilation.

---
## More Information

For more information, updates, and documentation, visit:

[RAMZ Official Website](https://redasaadcgt-sys.github.io/RAMZ/)

# Enjoy RAMZ

Thank you for trying RAMZ.
Have fun exploring the language and building programs with it!
