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
A=A-1
D=D-M
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
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 16
@16
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
A=A-1
D=D-M
@COMP_SUCCESS1
D;JEQ
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
// push constant 16
@16
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
A=A-1
D=D-M
@COMP_SUCCESS2
D;JEQ
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
A=A-1
D=D-M
@COMP_SUCCESS3
D;JGT
@SP
A=M-1
M=0
@COMP_END3
0;JMP
(COMP_SUCCESS3)
@SP
A=M-1
M=-1
(COMP_END3)
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 892
@892
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
A=A-1
D=D-M
@COMP_SUCCESS4
D;JGT
@SP
A=M-1
M=0
@COMP_END4
0;JMP
(COMP_SUCCESS4)
@SP
A=M-1
M=-1
(COMP_END4)
// push constant 891
@891
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
A=A-1
D=D-M
@COMP_SUCCESS5
D;JGT
@SP
A=M-1
M=0
@COMP_END5
0;JMP
(COMP_SUCCESS5)
@SP
A=M-1
M=-1
(COMP_END5)
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
A=A-1
D=D-M
@COMP_SUCCESS6
D;JLT
@SP
A=M-1
M=0
@COMP_END6
0;JMP
(COMP_SUCCESS6)
@SP
A=M-1
M=-1
(COMP_END6)
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32767
@32767
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
A=A-1
D=D-M
@COMP_SUCCESS7
D;JLT
@SP
A=M-1
M=0
@COMP_END7
0;JMP
(COMP_SUCCESS7)
@SP
A=M-1
M=-1
(COMP_END7)
// push constant 32766
@32766
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
A=A-1
D=D-M
@COMP_SUCCESS8
D;JLT
@SP
A=M-1
M=0
@COMP_END8
0;JMP
(COMP_SUCCESS8)
@SP
A=M-1
M=-1
(COMP_END8)
// push constant 57
@57
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
// not
@SP
A=M-1
M=!M
