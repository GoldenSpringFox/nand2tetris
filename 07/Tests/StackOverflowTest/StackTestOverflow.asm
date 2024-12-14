// push constant 0
@0
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
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// push constant 2
@2
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
@COMP_SUCCESS0
D;JGT
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
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 0
@0
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
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// lt
@SP
AM=M-1
D=M
A=A-1
D=D-M
@COMP_SUCCESS1
D;JGT
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
// push constant 0
@0
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
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// push constant 2
@2
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
@COMP_SUCCESS2
D;JLT
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
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 0
@0
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
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// gt
@SP
AM=M-1
D=M
A=A-1
D=D-M
@COMP_SUCCESS3
D;JLT
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
