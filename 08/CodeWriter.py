"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


INITIAL_STACK_POINTER = 256
INITIAL_SYSTEM_FUNCTION_NAME = "Sys.init"

"""
add, sub, and, or, eq, gt, lt
neg, not, shiftleft, shiftright
"""
ARITHMETIC_TRANSLATOR = {
    "add": (
        "// add\n"
        "@SP\n"
        "AM=M-1\n"
        "D=M\n"
        "A=A-1\n"
        "M=M+D\n"
    ),
    "sub": (
        "// sub\n"
        "@SP\n"
        "AM=M-1\n"
        "D=M\n"
        "A=A-1\n"
        "M=M-D\n"
    ),
    "and": (
        "// and\n"
        "@SP\n"
        "AM=M-1\n"
        "D=M\n"
        "A=A-1\n"
        "M=M&D\n"
    ),
    "or": (
        "// or\n"
        "@SP\n"
        "AM=M-1\n"
        "D=M\n"
        "A=A-1\n"
        "M=M|D\n"
    ),
    "neg": (
        "// neg\n"
        "@SP\n"
        "A=M-1\n"
        "M=-M\n"
    ),
    "not": (
        "// not\n"
        "@SP\n"
        "A=M-1\n"
        "M=!M\n"
    ),
    "shiftleft": (
        "// shiftleft\n"
        "@SP\n"
        "A=M-1\n"
        "M=M<<\n"
    ),
    "shiftright": (
        "// shiftright\n"
        "@SP\n"
        "A=M-1\n"
        "M=M>>\n"
    )
}

SEGMENT_TO_ASSEMBLY = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
}

SEGMENT_TEMP_START_INDEX = 5

class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.output_stream = output_stream
        self.comparisonCounter = 0
        self.callCounter = 0
        self.current_function = ""

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.filename = filename

    def write_bootstrap(self) -> None:
        result = (
            f"@{INITIAL_STACK_POINTER}\n"
            "D=A\n"
            "@SP\n"
            "M=D\n"
            )
        result += (
            f"@{INITIAL_SYSTEM_FUNCTION_NAME}\n"
            "0;JMP\n"
        )
        self.output_stream.write(result)

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        
        add, sub, and, or, eq, gt, lt
        neg, not, shiftleft, shiftright
        """
        
        if (command in ["eq", "gt", "lt"]):
            self.write_comparison(command)
        else:
            self.output_stream.write(ARITHMETIC_TRANSLATOR[command])
        
    def write_comparison(self, command: str):
        jumpComparison = {
            "eq": "JEQ",
            "gt": "JGT",
            "lt": "JLT"
        }
        comparisonResult = {
            "eq": ("0", "0"),
            "gt": ("-1", "0"),
            "lt": ("0", "-1")
        }

        result = (
            f"// {command}\n"
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            # jump #1 D sign 
            f"@FIRST_NEG{self.comparisonCounter}\n"
            "D;JLT\n"
            "@SP\n"
            "A=M-1\n"
            # jump #2 D sign
            "D=M\n"
            f"@SECOND_NEG_FIRST_POS{self.comparisonCounter}\n"
            "D;JLT\n"
            # both are positive
            f"@REGULAR_COMPARISON{self.comparisonCounter}\n"
            "0;JMP\n"
            f"(FIRST_NEG{self.comparisonCounter})\n"
            "@SP\n"
            "A=M-1\n"
            "D=M\n"
            f"@SECOND_NEG_FIRST_NEG{self.comparisonCounter}\n"
            "D;JLT\n"
            # first is negative second is positive
            "@SP\n"
            "A=M-1\n"
            f"M={comparisonResult[command][0]}\n"
            f"@COMP_END{self.comparisonCounter}\n"
            "0;JMP\n"
            # first is positive second is negative
            f"(SECOND_NEG_FIRST_POS{self.comparisonCounter})\n"
            "@SP\n"
            "A=M-1\n"
            f"M={comparisonResult[command][1]}\n"
            f"@COMP_END{self.comparisonCounter}\n"
            "0;JMP\n"
            f"(SECOND_NEG_FIRST_NEG{self.comparisonCounter})\n"
            f"@REGULAR_COMPARISON{self.comparisonCounter}\n"
            "0;JMP\n"
            f"(REGULAR_COMPARISON{self.comparisonCounter})\n"
            "@SP\n"
            "A=M\n"
            "D=M\n"
            "A=A-1\n"
            "D=M-D\n"
            f"@COMP_SUCCESS{self.comparisonCounter}\n"
            f"D;{jumpComparison[command]}\n"
            "@SP\n"
            "A=M-1\n"
            "M=0\n"
            f"@COMP_END{self.comparisonCounter}\n"
            "0;JMP\n"
            f"(COMP_SUCCESS{self.comparisonCounter})\n"
            "@SP\n"
            "A=M-1\n"
            "M=-1\n"
            f"(COMP_END{self.comparisonCounter})\n"
        )
        self.output_stream.write(result)
        self.comparisonCounter += 1


    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        if command == "C_PUSH":
            self.output_stream.write(self.push_code(segment, index))
        elif command == "C_POP":
            self.output_stream.write(self.pop_code(segment, index))

    def push_code(self, segment: str, index: int):
        result = f"// push {segment} {index}\n"
        if segment in SEGMENT_TO_ASSEMBLY.keys():
            result += (
                f"@{SEGMENT_TO_ASSEMBLY[segment]}\n"
                "D=M\n"
                f"@{index}\n"
                "A=A+D\n"
                "D=M\n"
            )
        elif segment == "constant":
            result += (
                f"@{index}\n"
                "D=A\n"
            )
        elif segment == "static":
            static_name = self.filename + "." + str(index)
            result += (
                f"@{static_name}\n"
                "D=M\n"
            )
        elif segment == "temp":
            result += (
                f"@{SEGMENT_TEMP_START_INDEX + index}\n"
                "D=M\n"
            )
        elif segment == "pointer":
            ramLocation = SEGMENT_TO_ASSEMBLY["this"] if index == 0 else SEGMENT_TO_ASSEMBLY["that"]
            result += (
                f"@{ramLocation}\n"
                "D=M\n"
            )
        else:
            return ""
        result += (
            "@SP\n"
            "A=M\n"
            "M=D\n"
            "@SP\n"
            "M=M+1\n"
            )
        return result

    def pop_code(self, segment: str, index: int):
        result = f"// pop {segment} {index}\n"
        if segment in SEGMENT_TO_ASSEMBLY.keys():
            result += (
                f"@{SEGMENT_TO_ASSEMBLY[segment]}\n"
                "D=M\n"
                f"@{index}\n"
                "D=A+D\n"
                "@pop\n"
                "M=D\n"
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                "@pop\n"
                "A=M\n"
                "M=D\n"
            )
        elif segment == "static":
            static_name = self.filename + "." + str(index)
            result += (
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                f"@{static_name}\n"
                "M=D\n"
            )
        elif segment == "temp":
            result += (
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                f"@{SEGMENT_TEMP_START_INDEX + index}\n"
                "M=D\n"
            )
        elif segment == "pointer":
            ramLocation = SEGMENT_TO_ASSEMBLY["this"] if index == 0 else SEGMENT_TO_ASSEMBLY["that"]
            result += (
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                f"@{ramLocation}\n"
                "M=D\n"
            )
        else:
            return ""
        return result

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        result = f"({self.filename}.{self.current_function}${label})\n"
        self.output_stream.write(result)
    
    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        result = (
            f"@{self.filename}.{self.current_function}${label}\n"
            "0;JMP\n")
        self.output_stream.write(result)
    
    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        result = (
            f"// if-goto {label}\n"
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            f"@{self.filename}.{self.current_function}${label}\n"
            "D;JNE\n")
        self.output_stream.write(result)
    
    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0

        self.current_function = function_name

        push_zero_on_stack = (
            "@SP\n"
            "A=M\n"
            "M=0\n"
            "@SP\n"
            "M=M+1\n")

        result = (f"// function {function_name} {n_vars}\n"
            f"({self.filename}.{function_name})\n") + push_zero_on_stack * n_vars
        self.output_stream.write(result)

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        
        return_address = f"{self.filename}.{self.current_function}$ret.{self.callCounter}"
        result = f"// call {function_name} {n_args}\n"
        result += (
            f"@{return_address}\n"
            "D=A\n"
            "@SP\n"
            "A=M\n"
            "M=D\n"
            "@SP\n"
            "M=M+1\n"
        )
        for pointer in ["LCL", "ARG", "THIS", "THAT"]:
            result += self.str_push_pointer_on_stack(pointer)
        result += (         # ARG = SP-5-n_args
            "@SP\n"
            "D=M\n"
            "@5\n"
            "D=D-A\n"
            f"@{n_args}\n"
            "D=D-A\n"
            "@ARG\n"
            "M=D\n"
        )
        result += (
            "@SP\n"
            "D=M\n"
            "@LCL\n"
            "M=D\n"
        )
        result += (
            f"@{self.filename}.{function_name}\n"
            "0;JMP\n"
        )
        result += f"({return_address})\n"
        
        self.output_stream.write(result)
        self.callCounter += 1

    def str_push_pointer_on_stack(self, pointer: str) -> str:
        return (
            f"@{pointer}\n"
            "D=M\n"
            "@SP\n"
            "A=M\n"
            "M=D\n"
            "@SP\n"
            "M=M+1\n")
    
    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        
        result = "// return\n"
        result += (             # frame = LCL
            "@LCL\n"
            "D=M\n"
            "@R13\n"
            "M=D\n"
        )
        result += (             # return_address = *(frame-5)
            "@R13\n"
            "D=M\n"
            "@5\n"
            "A=D-A\n"
            "D=M\n"
            "@R14\n"
            "M=D\n"
        )
        result += (             # *ARG = pop()
            "@SP\n"
            "A=M-1\n"
            "D=M\n"
            "@SP\n"
            "M=M-1\n"
            "@ARG\n"
            "A=M\n"
            "M=D\n"
        )
        result += (             # SP = ARG + 1
            "@ARG\n"
            "D=M+1\n"
            "@SP\n"
            "M=D\n"
        )
        i = 1
        for pointer in ["THAT", "THIS", "ARG", "LCL"]:      
            result += (         # pointer = *(frame-i)
                "@R13\n"
                "D=M\n"
                f"@{i}\n"
                "A=D-A\n"
                "D=M\n"
                f"@{pointer}\n"
                "M=D\n"
            )
            i += 1
        result += (             # goto return_address
            "@R14\n"
            "A=M\n"
            "0;JMP\n"
        )

        self.output_stream.write(result)
