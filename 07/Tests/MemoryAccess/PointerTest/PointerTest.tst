// This file is part of the materials accompanying the book
// "The Elements of Computing Systems" by Nisan and Schocken, 
// MIT Press 2004. Book site: http://www.idc.ac.il/tecs
// File name: projects/07/MemoryAccess/PointerTest/PointerTest.tst.
// Version: beta 1.4.

load PointerTest.asm,
output-file PointerTest.out,
compare-to PointerTest.cmp,
output-list RAM[256]%D1.6.1 RAM[3]%D1.6.1 
            RAM[4]%D1.6.1 RAM[3032]%D1.6.1 RAM[3046]%D1.6.1;

set RAM[0] 256,

repeat 150 {
  ticktock;
}

output;
