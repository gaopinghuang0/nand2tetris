// bootstrap code
@256
D=A
@SP
M=D
@Global.Bootstrap.ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(Global.Bootstrap.ret.1)
// function Class1.set 0
(Class1.set)
@0
D=A
// push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 0
@SP
M=M-1
@SP
A=M
D=M
@Class1.Static.0
M=D
// push argument 1
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 1
@SP
M=M-1
@SP
A=M
D=M
@Class1.Static.1
M=D
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// return
@LCL
D=M
@R6
M=D
@R6
D=M
@5
A=D-A
D=M
@R7
M=D
@ARG
D=M
@0
D=D+A
@R15
M=D
@SP
M=M-1
@SP
A=M
D=M
@R15
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R6
D=M
@1
A=D-A
D=M
@THAT
M=D
@R6
D=M
@2
A=D-A
D=M
@THIS
M=D
@R6
D=M
@3
A=D-A
D=M
@ARG
M=D
@R6
D=M
@4
A=D-A
D=M
@LCL
M=D
@R7
A=M
0;JMP
// function Class1.get 0
(Class1.get)
@0
D=A
// push static 0
@Class1.Static.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@Class1.Static.1
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
// return
@LCL
D=M
@R6
M=D
@R6
D=M
@5
A=D-A
D=M
@R7
M=D
@ARG
D=M
@0
D=D+A
@R15
M=D
@SP
M=M-1
@SP
A=M
D=M
@R15
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R6
D=M
@1
A=D-A
D=M
@THAT
M=D
@R6
D=M
@2
A=D-A
D=M
@THIS
M=D
@R6
D=M
@3
A=D-A
D=M
@ARG
M=D
@R6
D=M
@4
A=D-A
D=M
@LCL
M=D
@R7
A=M
0;JMP
// function Class2.set 0
(Class2.set)
@0
D=A
// push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 0
@SP
M=M-1
@SP
A=M
D=M
@Class2.Static.0
M=D
// push argument 1
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 1
@SP
M=M-1
@SP
A=M
D=M
@Class2.Static.1
M=D
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// return
@LCL
D=M
@R6
M=D
@R6
D=M
@5
A=D-A
D=M
@R7
M=D
@ARG
D=M
@0
D=D+A
@R15
M=D
@SP
M=M-1
@SP
A=M
D=M
@R15
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R6
D=M
@1
A=D-A
D=M
@THAT
M=D
@R6
D=M
@2
A=D-A
D=M
@THIS
M=D
@R6
D=M
@3
A=D-A
D=M
@ARG
M=D
@R6
D=M
@4
A=D-A
D=M
@LCL
M=D
@R7
A=M
0;JMP
// function Class2.get 0
(Class2.get)
@0
D=A
// push static 0
@Class2.Static.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@Class2.Static.1
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
// return
@LCL
D=M
@R6
M=D
@R6
D=M
@5
A=D-A
D=M
@R7
M=D
@ARG
D=M
@0
D=D+A
@R15
M=D
@SP
M=M-1
@SP
A=M
D=M
@R15
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R6
D=M
@1
A=D-A
D=M
@THAT
M=D
@R6
D=M
@2
A=D-A
D=M
@THIS
M=D
@R6
D=M
@3
A=D-A
D=M
@ARG
M=D
@R6
D=M
@4
A=D-A
D=M
@LCL
M=D
@R7
A=M
0;JMP
// function Sys.init 0
(Sys.init)
@0
D=A
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class1.set 2
@Sys.init.ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@2
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(Sys.init.ret.1)
// pop temp 0 // Dumps the return value
@SP
M=M-1
@SP
A=M
D=M
@R5
M=D
// push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class2.set 2
@Sys.init.ret.2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@2
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(Sys.init.ret.2)
// pop temp 0 // Dumps the return value
@SP
M=M-1
@SP
A=M
D=M
@R5
M=D
// call Class1.get 0
@Sys.init.ret.3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.get
0;JMP
(Sys.init.ret.3)
// call Class2.get 0
@Sys.init.ret.4
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.get
0;JMP
(Sys.init.ret.4)
// label WHILE
(WHILE)
// goto WHILE
@WHILE
0;JMP
