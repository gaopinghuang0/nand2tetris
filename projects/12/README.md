## Project 12: Jack OS
Jack OS: (Math, Memory, Screen, Output, Keyboard, String, Array, Sys).jack

* Description: https://www.nand2tetris.org/project12
* Lecture notes: https://docs.wixstatic.com/ugd/44046b_06740a902eeb478da9a178c4ce6ec50f.pdf

### Getting Started
Unit test a single dir
```bash
# compile *.jack into *.vm, then load into VMEmulator.[bat|sh]
$ ../../tools/JackCompiler.[bat|sh] MathTest

# use when-changed to auto-compile
$ when-changed -v MathTest/*.jack -c F:/course/Nand2Tetris/tools/JackCompiler.bat MathTest
```

### Recommended implementation and test
* Implement in any desired order. 
* Put the `*.jack` in each corresponding folder to short-cut built-in OS implementation.


### Notes:
* A nice thing about Two's Complement of Integer is that addition and substraction is made very simple (i.e., unified). Check [this link](https://www.cs.cornell.edu/~tomf/notes/cps104/twoscomp.html). It means that the addition and substraction involving negative integer is handled automatically in binary format. It also makes multiplication handle sign (+-) automatically, since it will be calculated in terms of addition.