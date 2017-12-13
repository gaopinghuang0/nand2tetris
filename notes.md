# My notes of learning Nand2Tetris

## About `*.hdl` (hardware description language) file 
* [HDL Survival Guide](http://nand2tetris.org/software/HDL%20Survival%20Guide.html)

* A good way to write `*.hdl` file.
  * The order of chips doesn't matter when flip-flops exist, so start with any familiar chips, fill with known pins, leave the unknown pins blank, which will be generated later by other chips. 
  * Do not wait until all the pins of a chip are ready; otherwise, chicken-and-egg things might happen (e.g., the output of A chip is the input of B chip while the output of B is the input of A).

## About HACK assembly language
* 16-bit address: the highest bit (or leftmost bit) is address[15], the rightmost bit is address[0], and the other bits are address[1..14]
* How to output only part of the pins:
  ```hack
  PC(in=aout, load=PCload, inc=inc, reset=reset, out[0..14]=pc);
  ```
* Syntax of A-instruction
  * For RAM and M register
  ```hack
  @value
  ```
  Sets the A register to `value`; Side effect: RAM[A] becomes the selected RAM register, in which M register refers to RAM[A].  For example `@21`, sets A register to 21, RAM[21] becomes the selected RAM, and M register refers to RAM[21].
  ```hack
  @21
  D=M   // load RAM[21] to D

  @22
  M=D+1  // save D+1 to RAM[22], here, D+1 is RAM[21]+1
  ```

  * For ROM and jump:
  ```hack
  // if (D-1==0) then jump to location ROM[56]
  @56   // set A=56
  D-1;JEQ    // jump to instruction ROM[A] if true, namely ROM[56]
  ```

  * For variable and pointer
  ```hack
  @temp
  M=D  // temp = D

  // suppose arr and i are defined
  // set RAM[arr+i] = -1, namely, arr[i] = -1
  @arr   
  D=M
  @i
  A=D+M  <-- key of pointer
  M=-1
  ```

* More about A, D, M registers
    * A - Use to store address or immediate value (number)
    * D - Use to store temp data, and do simple calculation
    * M - Always refer to RAM[A]. Make sure that A is corret before using M since A may have been changed since the last A-instruction.