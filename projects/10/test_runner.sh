#!/usr/bin/env bash
echo $1
if [ $1 = "-t" ]; then
  echo
  ./main_tokenizer.py  ExpressionlessSquare/  test/
  ./xml_compare_helper.py -t ExpressionlessSquare/  test/
  echo
  ./main_tokenizer.py  Square/  test/
  ./xml_compare_helper.py -t Square/  test/
  echo
  ./main_tokenizer.py  ArrayTest/  test/
  ./xml_compare_helper.py -t ArrayTest/  test/
else
  echo
  ./main_analyzer.py  ExpressionlessSquare/  test/
  ./xml_compare_helper.py -a ExpressionlessSquare/  test/
  echo
  ./main_analyzer.py  Square/  test/
  ./xml_compare_helper.py -a Square/  test/
  echo
  ./main_analyzer.py  ArrayTest/  test/
  ./xml_compare_helper.py -a ArrayTest/  test/
fi