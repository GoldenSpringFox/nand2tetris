// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// Multiplies R0 and R1 and stores the result in R2.
//
// Assumptions:
// - R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.
// - You can assume that you will only receive arguments that satisfy:
//   R0 >= 0, R1 >= 0, and R0*R1 < 32768.
// - Your program does not need to test these conditions.
//
// Requirements:
// - Your program should not change the values stored in R0 and R1.
// - You can implement any multiplication algorithm you want.

    // R2 = 0, i = 0
    @R2
    M = 0
    @i
    M = 0

    // for (i=0..R1)
(LOOP)
    @i
    D = M
    @R1
    D = D - M
    @END
    D;JGE
    
    // R2 += R2 + R0
    @R0
    D = M
    @R2
    M = M + D
    
    @i
    M = M + 1

    @LOOP
    0;JMP

(END)
    @END
    0;JMP