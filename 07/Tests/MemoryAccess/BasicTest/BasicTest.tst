// This file is part of the materials accompanying the book
// "The Elements of Computing Systems" by Nisan and Schocken, 
// MIT Press 2004. Book site: http://www.idc.ac.il/tecs
// File name: projects/07/MemoryAccess/BasicTest/BasicTest.tst. 
// Version: beta 1.4.

load BasicTest.asm,
output-file BasicTest.out,
compare-to BasicTest.cmp,
output-list RAM[256]%D1.6.1 RAM[300]%D1.6.1 RAM[401]%D1.6.1 
            RAM[402]%D1.6.1 RAM[3006]%D1.6.1 RAM[3012]%D1.6.1
            RAM[3015]%D1.6.1 RAM[11]%D1.6.1;

set RAM[0] 256,
set RAM[1] 300,
set RAM[2] 400,
set RAM[3] 3000,
set RAM[4] 3010,

repeat 1000 {
  ticktock;
}

output;
