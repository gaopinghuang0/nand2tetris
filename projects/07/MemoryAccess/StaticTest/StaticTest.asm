// push constant 111
@111
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 333
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 888
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop static 8
@SP
M=M-1
@SP
A=M
D=M
@FooStatic.8
M=D
// pop static 3
@SP
M=M-1
@SP
A=M
D=M
@FooStatic.3
M=D
// pop static 1
@SP
M=M-1
@SP
A=M
D=M
@FooStatic.1
M=D
// push static 3
@FooStatic.3
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@FooStatic.1
D=M
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1
// push static 8
@FooStatic.8
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
A=M-1
D=M
A=A-1
M=D+M
@SP
M=M-1
