// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// This program illustrates low-level handling of the screen and keyboard
// devices, as follows.
//
// The program runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.
// 
// Assumptions:
// Your program may blacken and clear the screen's pixels in any spatial/visual
// Order, as long as pressing a key continuously for long enough results in a
// fully blackened screen, and not pressing any key for long enough results in a
// fully cleared screen.
//
// Test Scripts:
// For completeness of testing, test the Fill program both interactively and
// automatically.
// 
// The supplied FillAutomatic.tst script, along with the supplied compare file
// FillAutomatic.cmp, are designed to test the Fill program automatically, as 
// described by the test script documentation.
//
// The supplied Fill.tst script, which comes with no compare file, is designed
// to do two things:
// - Load the Fill.hack program
// - Remind you to select 'no animation', and then test the program
//   interactively by pressing and releasing some keyboard keys

    // screensize = 8K
    @8192
    D = A
    @screensize
    M = D

    // waspressed = 0, color = white
    @waspressed
    M = 0
    @color
    M = 0

// loop(true)
(LOOP)
    // if keyboard != 0
    @KBD
    D=M
    @UNPRESSED
    D;JEQ

(PRESSED)
    // color = black
    @color
    M = -1

    // waspressed == 0
    @waspressed
    D = M
    M = 1
    @COLORSCREEN
    D;JEQ
    @LOOP
    0;JMP

(UNPRESSED)
    // color = white
    @color
    M = 0
    
    // waspressed == 1
    @waspressed
    D = M
    M = 0
    @COLORSCREEN
    D-1;JEQ
    @LOOP
    0;JMP

(COLORSCREEN)
    @i
    M = 0
    @color
    D = M
    @WHITESCREEN
    D;JEQ

(BLACKSCREEN)
    @SCREEN
    D = A
    @i
    A = D + M
    
    M = -1

    @i
    M = M + 1
    
    D = M
    @screensize
    D = D - M
    @BLACKSCREEN
    D;JLT
    
    @LOOP
    0;JMP
    

(WHITESCREEN)
    @SCREEN
    D = A
    @i
    A = D + M
    
    M = 0

    @i
    M = M + 1

    D = M
    @screensize
    D = D - M
    @WHITESCREEN
    D;JLT
    
    @LOOP
    0;JMP