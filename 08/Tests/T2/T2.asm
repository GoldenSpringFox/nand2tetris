// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
@FIRST_NEG0
D;JLT
@SP
A=M-1
D=M
@SECOND_NEG_FIRST_POS0
D;JLT
@REGULAR_COMPARISON0
0;JMP
(FIRST_NEG0)
@SP
A=M-1
D=M
@SECOND_NEG_FIRST_NEG0
D;JLT
@SP
A=M-1
M=0
@COMP_END0
0;JMP
(SECOND_NEG_FIRST_POS0)
@SP
A=M-1
M=0
@COMP_END0
0;JMP
(SECOND_NEG_FIRST_NEG0)
@REGULAR_COMPARISON0
0;JMP
(REGULAR_COMPARISON0)
@SP
A=M
D=M
A=A-1
D=M-D
@COMP_SUCCESS0
D;JEQ
@SP
A=M-1
M=0
@COMP_END0
0;JMP
(COMP_SUCCESS0)
@SP
A=M-1
M=-1
(COMP_END0)
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
@FIRST_NEG1
D;JLT
@SP
A=M-1
D=M
@SECOND_NEG_FIRST_POS1
D;JLT
@REGULAR_COMPARISON1
0;JMP
(FIRST_NEG1)
@SP
A=M-1
D=M
@SECOND_NEG_FIRST_NEG1
D;JLT
@SP
A=M-1
M=0
@COMP_END1
0;JMP
(SECOND_NEG_FIRST_POS1)
@SP
A=M-1
M=-1
@COMP_END1
0;JMP
(SECOND_NEG_FIRST_NEG1)
@REGULAR_COMPARISON1
0;JMP
(REGULAR_COMPARISON1)
@SP
A=M
D=M
A=A-1
D=M-D
@COMP_SUCCESS1
D;JLT
@SP
A=M-1
M=0
@COMP_END1
0;JMP
(COMP_SUCCESS1)
@SP
A=M-1
M=-1
(COMP_END1)
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
@FIRST_NEG2
D;JLT
@SP
A=M-1
D=M
@SECOND_NEG_FIRST_POS2
D;JLT
@REGULAR_COMPARISON2
0;JMP
(FIRST_NEG2)
@SP
A=M-1
D=M
@SECOND_NEG_FIRST_NEG2
D;JLT
@SP
A=M-1
M=-1
@COMP_END2
0;JMP
(SECOND_NEG_FIRST_POS2)
@SP
A=M-1
M=0
@COMP_END2
0;JMP
(SECOND_NEG_FIRST_NEG2)
@REGULAR_COMPARISON2
0;JMP
(REGULAR_COMPARISON2)
@SP
A=M
D=M
A=A-1
D=M-D
@COMP_SUCCESS2
D;JGT
@SP
A=M-1
M=0
@COMP_END2
0;JMP
(COMP_SUCCESS2)
@SP
A=M-1
M=-1
(COMP_END2)
// push constant 56
@56
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
// push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// neg
@SP
A=M-1
M=-M
// and
@SP
AM=M-1
D=M
A=A-1
M=M&D
// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
AM=M-1
D=M
A=A-1
M=M|D
// push constant 100
@100
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop static 8
@SP
AM=M-1
D=M
@T2.8
M=D
// push static 8
@T2.8
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 3030
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
AM=M-1
D=M
@THIS
M=D
// push constant 3040
@3040
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
AM=M-1
D=M
@THAT
M=D
// push constant 32
@32
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop this 2
@THIS
D=M
@2
D=A+D
@pop
M=D
@SP
AM=M-1
D=M
@pop
A=M
M=D
// push constant 46
@46
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 6
@THAT
D=M
@6
D=A+D
@pop
M=D
@SP
AM=M-1
D=M
@pop
A=M
M=D
// push pointer 0
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push pointer 1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
// push this 2
@THIS
D=M
@2
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// push that 6
@THAT
D=M
@6
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
// push constant 3038
@3038
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
AM=M-1
D=M
@THIS
M=D
// push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop this 2
@THIS
D=M
@2
D=A+D
@pop
M=D
@SP
AM=M-1
D=M
@pop
A=M
M=D
