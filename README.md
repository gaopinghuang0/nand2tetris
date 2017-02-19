# nand2tetris
All projects for [Nand2Tetris](http://www.nand2tetris.org/)

## notes:
0. 16-bit address: the highest bit (or leftmost bit) is address[15], the rightmost bit is address[0], and the other bits are address[1..14]
1. how to output only part of the pins:
```hack
PC(in=aout, load=PCload, inc=inc, reset=reset, out[0..14]=pc);
```
