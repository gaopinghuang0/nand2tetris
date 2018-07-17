## Project 10: Compiler I - Syntax Analysis
1. Description: https://www.nand2tetris.org/project10
2. Lecture notes: https://docs.wixstatic.com/ugd/44046b_aca87ffea29e416f8c0d7e9edbd6b273.pdf


### Recommended order of implementation and test
1. `jack_tokenizer.py`: get `*.jack`, output `*T.xml` (T means tokenizer).
2. `jack_analyzer.py`: get `*.jack`, output `*.xml`
3. ExpressionLessSquare -> Square -> ArrayTest
4. The `tools/TextCompiler.[bat|sh]` can be used to compare the generated xml file with given compare file. It will ignore the while space of the XML output, namely, the indentation of XML is only for readability.

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

### Notes