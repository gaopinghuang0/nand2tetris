## Project 11: Compiler II - Code Generation
1. Description: https://www.nand2tetris.org/project11
2. Lecture notes: https://docs.wixstatic.com/ugd/44046b_78430a86b638470fba194ed461044ae9.pdf


### Getting Started
Unit test for a single dir
```bash
# tokenizer
./main_tokenizer.py  Square/  test/
./xml_compare_helper.py -t Square/  test/
# analyzer
./main_analyzer.py  Square/  test/
./xml_compare_helper.py -a Square/  test/
```

Integral test for all dirs
```bash
$ ./test_runner.sh -t   # test tokenizer
$ ./test_runner.sh -a   # test analyzer
```

### Recommended implementation and test
* JackCompiler -> Tokenizer (done in project 10) -> SymbolTable -> CompilationEngine (done in project 10, but needs update) -> VMWriter
* Seven -> 
* All the APIs are given in the lecture notes mentioned above
* To unit test SymbolTable, just reuse project 10 code, output special/customized tag (e.g., not just `identifier` but `field 0 | static 1 | ...`) for each variable into xml code, and then check the output xml code
* To unit test JackCompiler, load the generated `*.vm` file into `tools/VMEmulator.[bat|sh]` and run script.


### Notes:
* Jack language has no operator precedence, `a + b * c` is not the same as `a + (b * c)`. In this project, we also don't consider operator precedence, for simplicity.
* For `void function`, we still need to add `return` statement at the bottom. When compile callee, we push a constant 0 before return, in caller, we pop temp 0 to remove it from stack.
* We use `this` for object, `that` for array. 
* **Array access**. We only use `pop that 0` to access array element.
```c
// version 1
// arr[2] = 17
push arr  // base address
push 2    // offset
add
pop pointer 1
push 17
pop that 0 // only pop that 0
```
Note that the compiler could have generated the following code:
```c
// version 2
push arr
pop pointer 1
push 17
pop that 2
```
Why not? Because the simple code (version 2) works only for constant offsets (indices). It cannot be used when the source statement is, say, `let arr[x]=y`. But even the code of version 1 has a problem, see `images/array-access-*.png` for detail.

