// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.

(LOOP)
    @status
    M = 0

    @KBD
    D = M
    @SETSCREEN
    D; JEQ
    @status
    M = -1  // press any key
    


   (SETSCREEN)
    @8191
    D = A
    @i
    M = D

    (LOOP1)
        @i
        D = M
        @LOOP
        D; JLT

        @SCREEN
        D = A
        @i
        D = D + M
        @tmp
        M = D
        @status
        D = M   // RAM[i] = 0 or -1 based on status
        @tmp
        A = M
        M = D

        @i
        M = M - 1

        @LOOP1
        0; JMP

    @LOOP
    0; JMP