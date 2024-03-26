@256
D=A
@SP
M=D
//// This file is part of www.nand2tetris.org
//// and the book "The Elements of Computing Systems"
//// by Nisan and Schocken, MIT Press.
//// File name: projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.vm
//
//// Puts the first argument[0] elements of the Fibonacci series
//// in the memory, starting in the address given in argument[1].
//// Argument[0] and argument[1] are initialized by the test script
//// before this code starts running.
//
//push argument 1
@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//pop pointer 1           // that = argument[1]
@SP
A=M-1
D=M
@THAT
M=D
@SP
M=M-1
//
//push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
//pop that 0              // first element in the series = 0
@0
D=A
@R13
M=D
@THAT
D=M
@R13
M=M+D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
//push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
//pop that 1              // second element in the series = 1
@1
D=A
@R13
M=D
@THAT
D=M
@R13
M=M+D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
//
//push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
@SP
A=M-1
D=M
@SP
M=M-1
@SP
A=M-1
D=M-D
@SP
A=M-1
M=D
//pop argument 0          // num_of_elements -= 2 (first 2 elements are set)
@0
D=A
@R13
M=D
@ARG
D=M
@R13
M=M+D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
//
//label MAIN_LOOP_START
(MAIN_LOOP_START)
//
//push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//if-goto COMPUTE_ELEMENT // if num_of_elements > 0, goto COMPUTE_ELEMENT
@SP
A=M-1
D=M
@SP
M=M-1
@COMPUTE_ELEMENT
D;JNE
//goto END_PROGRAM        // otherwise, goto END_PROGRAM
@END_PROGRAM
0;JMP
//
//label COMPUTE_ELEMENT
(COMPUTE_ELEMENT)
//
//push that 0
@0
D=A
@THAT
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//push that 1
@1
D=A
@THAT
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//add
@SP
A=M-1
D=M
@SP
M=M-1
@SP
A=M-1
D=M+D
@SP
A=M-1
M=D
//pop that 2              // that[2] = that[0] + that[1]
@2
D=A
@R13
M=D
@THAT
D=M
@R13
M=M+D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
//
//push pointer 1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
//push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
//add
@SP
A=M-1
D=M
@SP
M=M-1
@SP
A=M-1
D=M+D
@SP
A=M-1
M=D
//pop pointer 1           // that += 1
@SP
A=M-1
D=M
@THAT
M=D
@SP
M=M-1
//
//push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
@SP
A=M-1
D=M
@SP
M=M-1
@SP
A=M-1
D=M-D
@SP
A=M-1
M=D
//pop argument 0          // num_of_elements--
@0
D=A
@R13
M=D
@ARG
D=M
@R13
M=M+D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
//
//goto MAIN_LOOP_START
@MAIN_LOOP_START
0;JMP
//
//label END_PROGRAM
(END_PROGRAM)
