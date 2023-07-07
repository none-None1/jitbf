### What's this? A fast brainfuck JIT interpreter!

#### How to install it?

You can clone this repo, but this package is published on PyPI, too. Therefore, you can also install it using pip:

```commandline
pip install llvmlite jitbf # The package also requires llvmlite
```

[Project link on PyPI](https://pypi.org/project/jitbf/)

#### How to use?

To use it, you can either write your code like this:
```python
from jitbf import bf2jit
code='<code>'
jit=bf2jit(code)
jit()
```

, or use the jitbf command.

You have to install tha package 'llvmlite' before using this package.

#### How fast is it?

I compared this JIT interpreter with the [Quick Dirty Interpreter In C](http://brainfuck.org/qdb.c).
The brainfuck code used in the test is [mandel.b](https://github.com/eriknyquist/bfi/blob/master/bfi/examples/mandel.b).
The operating system used in the test is Windows 10 64 bit.

```python
Interpreter: jitbf 1.0.0                      Time to run: 3.5764139 s

Interpreter: Quick Dirty Interpreter In C     Time to run: 8.3990561 s
```

#### How does it work?

The package is based on LLVM, it first translates brainfuck into LLVM IR code, then uses llvmlite to compile and run it.

#### What advantages and disadvantages does it have?

Advantages:
1. Fast.
2. Consists of only one small Python file.
3. Provides a commandline tool.

Disadvantages:
1. It does NOT free allocated memory.
2. Once you run brainfuck code which never ends, using this package, all you can do to terminate it is to kill it (Ctrl+C won't work).

#### How will you improve it in the future?

I will improve it by making the LLVM IR code it translates smaller, and runs faster.
