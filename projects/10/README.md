## Project 10: Compiler I - Syntax Analysis
1. Description: http://www.nand2tetris.org/10.php
2. Lecture notes: http://www.nand2tetris.org/lectures/PDF/lecture%2010%20compiler%20I.pdf


### Recommended order of implementation and test
1. `jack_tokenizer.py`: get `*.jack`, output `*T.xml` (T means tokenizer).
2. `jack_analyzer.py`: get `*.jack`, output `*.xml`
3. ExpressionLessSquare -> Square -> ArrayTest
4. The `tools/TextCompiler.[bat|sh]` can be used to compare the generated xml file with given compare file. It will ignore the while space of the XML output, namely, the indentation of XML is only for readability.

### Getting Started
```bash
# tokenizer
./jack_tokenizer.py  Square/  test/
./xml_compare_helper.py -t Square/  test/
# analyzer
./jack_analyzer.py  Square/  test/
./xml_compare_helper.py -a Square/  test/
```


### Notes