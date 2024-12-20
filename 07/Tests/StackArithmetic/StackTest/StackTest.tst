// This file is part of the materials accompanying the book
// "The Elements of Computing Systems" by Nisan and Schocken, 
// MIT Press 2004. Book site: http://www.idc.ac.il/tecs
// File name: projects/07/StackArithmetic/StackTest/StackTest.tst.
// Version: beta 1.4.

load StackTest.asm,
output-file StackTest.out,
compare-to StackTest.cmp,
output-list RAM[0]%D2.6.2 RAM[256]%D2.6.2 RAM[257]%D2.6.2 
            RAM[258]%D2.6.2 RAM[259]%D2.6.2;

set RAM[0] 256,

repeat 200 {
  ticktock;
}

output;
