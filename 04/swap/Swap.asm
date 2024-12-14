// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

    // if array length < 2 end
    @R15
    D = M - 1
    @END
    D;JLE

    // min_index, max_index = arr[0]
    @R14
    D = M
    @minindex
    M = D
    @maxindex
    M = D

    @i
    M = 1
    // foreach elem in R14
(LOOP)
    @R14
    D = M
    @i
    A = D + M
    D = M
    @elem
    M = D

    // if arr[min_index] > elem update min_index
    @minindex
    A = M
    D = M
    @elem
    D = D - M
    
    @DONTUPDATEMIN
    D;JLE

    @R14
    D = M
    @i
    D = D + M
    @minindex
    M = D

(DONTUPDATEMIN)

    // if arr[max_index] < elem update max_index
    @maxindex
    A = M
    D = M
    @elem
    D = D - M
    
    @DONTUPDATEMAX
    D;JGE

    @R14
    D = M
    @i
    D = D + M
    @maxindex
    M = D

(DONTUPDATEMAX)
    
    @i
    M = M + 1
    D = M
    @R15
    D = D - M
    @LOOP
    D;JLT
    
    // swap arr[min_index] and arr[max_index]
    @minindex
    A = M
    D = M
    
    @temp
    M = D
    
    @maxindex
    A = M
    D = M

    @minindex
    A = M
    M = D

    @temp
    D = M

    @maxindex
    A = M
    M = D

(END)
    @END
    0;JMP