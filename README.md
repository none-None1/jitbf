<p><span><span style="font-family:Verdana, Arial, Helvetica, sans-serif;line-height:19px;text-indent:26px;"><span style="font-size:14px;"><span style="font-family:Arial;line-height:26px;"><br></span></span></span></span></p>

### What's this? A fast brainfuck JIT interpreter!

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

Interpreter: jitbf 1.0.0                  Time to run: 3.5764139s

Interpreter: Quick Dirty Interpreter In C Time to run: 8.3990561s

The 
#### How does it work?

The package is based on LLVM, it first translates brainfuck into LLVM IR code, then uses llvmlite to compile and run it.

#### How will you improve it in the future?

I will improve it by making the LLVM IR code it translates smaller, and runs faster.