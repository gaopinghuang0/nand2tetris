# nand2tetris
All projects for [Nand2Tetris](http://www.nand2tetris.org/)

## notes:
1. A good way to write .hdl file. The order of chips doesn't matter when flip-flops exist, so start with any familiar chips, fill with known pins, leave the unknown pins blank, which will be generated later by other chips. Do not wait until all the pins of a chip are ready; otherwise, chicken-and-egg things might happen (e.g., the output of A chip is the input of B chip while the output of B is the input of A).
1. 16-bit address: the highest bit (or leftmost bit) is address[15], the rightmost bit is address[0], and the other bits are address[1..14]
2. How to output only part of the pins:
```hack
PC(in=aout, load=PCload, inc=inc, reset=reset, out[0..14]=pc);
```
