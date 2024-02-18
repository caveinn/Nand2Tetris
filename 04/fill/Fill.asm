// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(LOOP)
@KBD
D=M
@WHITE
D;JEQ
(BLACK)
    @SCREEN
    D=A
    @R0
    M=D
    (BLOOP)
        @0
        D=A-1
        @R0
        A=M
        M=D
        @R0
        MD=M+1
        @24576
        D=A-D
        @BLOOP
        D;JNE
    @LOOP
    0;JMP
(WHITE)
    @SCREEN
    D=A
    @R0
    M=D
    (WLOOP)
        @0
        D=A
        @R0
        A=M
        M=D
        @R0
        MD=M+1
        @24576
        D=A-D
        @WLOOP
        D;JNE
@LOOP
0;JMP



