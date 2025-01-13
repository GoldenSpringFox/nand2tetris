"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer, TOKEN_TYPE
from SymbolTable import SymbolTable
from VMWriter import VMWriter

TOKEN_TYPE_XML = {
    "KEYWORD": "keyword",
    "SYMBOL": "symbol",
    "IDENTIFIER": "identifier",
    "INT_CONST": "integerConstant",
    "STRING_CONST": "stringConstant"
}
OPERATORS = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
OPERATOR_TO_VM_DICT = {
    '+': "ADD", 
    '-': "SUB", 
    '&': "AND", 
    '|': "OR", 
    '<': "LT",
    '>': "GT", 
    '=': "EQ"
}
UNARY_OPERATORS = ['-', '~', '^', '#']
UNARY_OPERATOR_TO_VM_DICT = {
    '-': "NEG",
    '~': "NOT",
    '^': "SHIFTLEFT",
    '#': "SHIFTRIGHT"
}
KEYWORD_CONSTANTS = ["true", "false", "null", "this"]


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: JackTokenizer, symbol_table: SymbolTable, vmwriter: VMWriter) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.while_counter = 0
        self.subroutine_name = None
        self.if_counter = 0
        self.class_name = None
        self.tokenizer = input_stream
        self.symbol_table = symbol_table
        self.vmwriter = vmwriter

        self.tokenizer.advance()

    def eat(self, words: str | list[str] = None,
            types: TOKEN_TYPE | list[TOKEN_TYPE] = ("KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST")) -> None | str:
        if isinstance(words, str):
            words = [words]

        if isinstance(types, str):
            types = [types]

        token_type = self.tokenizer.token_type()
        token = None

        if token_type not in types:
            raise Exception(f"Expected one of {types} types. Found {token_type}")

        if token_type == "KEYWORD":
            token = self.tokenizer.keyword().lower()  # :(
        elif token_type == "IDENTIFIER":
            token = self.tokenizer.identifier()
        elif token_type == "INT_CONST":
            token = self.tokenizer.int_val()
        elif token_type == "STRING_CONST":
            token = self.tokenizer.string_val()
        elif token_type == "SYMBOL":
            token = self.tokenizer.symbol()

        if words is not None and token not in words:
            raise Exception(f"Expected {words}. Found {token}")

        self.tokenizer.advance()
        return token

    def open_tag(self, tag: str):
        ...

    def close_tag(self, tag: str):
        ...

    def matches_keyword(self, *words: str) -> bool:
        return self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword().lower() in words

    def matches_symbol(self, *words: str) -> bool:
        return self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.keyword() in words

    def compile_type(self):
        if self.matches_keyword("int", "char", "boolean"):
            return self.eat(types="KEYWORD")
        else:
            return self.eat(types="IDENTIFIER")

    def check_if_type(self):
        return self.matches_keyword("int", "char", "boolean") or self.tokenizer.token_type() == "IDENTIFIER"

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.eat("class")
        self.class_name = self.eat(types=["IDENTIFIER"])
        self.eat("{")

        while self.matches_keyword('static', 'field'):
            self.compile_class_var_dec()
        while self.matches_keyword('constructor', 'function', 'method'):
            self.compile_subroutine()
        self.eat("}")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        variable_kind = self.eat(words=["static", "field"]).upper()
        variable_type = self.compile_type()
        variable_name = self.eat(types="IDENTIFIER")

        self.symbol_table.define(variable_name, variable_type, variable_kind)

        while self.matches_symbol(","):
            self.eat(",")
            variable_name = self.eat(types="IDENTIFIER")
            self.symbol_table.define(variable_name, variable_type, variable_kind)

        self.eat(";")

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        function_type = self.eat(words=["constructor", "function", "method"])

        if self.matches_keyword("void"):
            self.eat()
        else:
            self.compile_type()

        function_name = self.eat(types="IDENTIFIER")
        self.subroutine_name = function_name

        self.eat("(")
        arg_count = self.compile_parameter_list()
        self.eat(")")

        if function_type == "method":
            arg_count += 1

        self.vmwriter.write_function(f"{self.class_name}.{function_name}", arg_count)

        if function_type == "constructor":  # ? "and self.symbol_table.var_count("FIELD") > 0"
            self.vmwriter.write_push("CONST", self.symbol_table.var_count("FIELD"))
            self.vmwriter.write_call("Memory.alloc", 1)
        elif function_type == "method":
            self.vmwriter.write_push("ARG", 0)
            self.vmwriter.write_pop("POINTER", 0)

        self.compile_subroutine_body()

    def compile_parameter_list(self) -> int:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        argument_count = 0
        variable_kind = "ARG"

        if self.check_if_type():
            argument_count += 1
            variable_type = self.compile_type()
            variable_name = self.eat(types="IDENTIFIER")
            self.symbol_table.define(variable_name, variable_type, variable_kind)

            while self.matches_symbol(","):
                argument_count += 1
                self.eat(",")
                variable_type = self.compile_type()
                variable_name = self.eat(types="IDENTIFIER")
                self.symbol_table.define(variable_name, variable_type, variable_kind)

        return argument_count

    def compile_subroutine_body(self) -> None:
        self.eat("{")

        while self.matches_keyword("var"):
            self.compile_var_dec()

        self.compile_statements()

        self.eat("}")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        variable_kind = self.eat("var").upper()
        variable_type = self.compile_type()
        variable_name = self.eat(types="IDENTIFIER")

        self.symbol_table.define(variable_name, variable_type, variable_kind)

        while self.matches_symbol(","):
            self.eat(",")
            variable_name = self.eat(types="IDENTIFIER")
            self.symbol_table.define(variable_name, variable_type, variable_kind)

        self.eat(";")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        while self.matches_keyword("let", "if", "while", "do", "return"):
            keyword = self.tokenizer.keyword().lower()
            if keyword == "let":
                self.compile_let()
            elif keyword == "if":
                self.compile_if()
            elif keyword == "while":
                self.compile_while()
            elif keyword == "do":
                self.compile_do()
            elif keyword == "return":
                self.compile_return()

        self.close_tag("statements")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.eat("let")
        variable_name = self.eat(types="IDENTIFIER")
        is_variable_array_element = False
        if self.matches_symbol("["):
            is_variable_array_element = True
            self.vmwriter.write_push(self.symbol_table.kind_of(variable_name),
                                     self.symbol_table.index_of(variable_name))
            self.eat("[")
            self.compile_expression()
            self.vmwriter.write_arithmetic("ADD")

            self.eat("]")

        self.eat("=")

        self.compile_expression()
        if is_variable_array_element:
            self.vmwriter.write_pop("TEMP", 0)
            self.vmwriter.write_pop("POINTER", 1)
            self.vmwriter.write_push("TEMP", 0)
            self.vmwriter.write_push("THAT", 0)
        else:
            self.vmwriter.write_pop(self.symbol_table.kind_of(variable_name), self.symbol_table.index_of(variable_name))
        self.eat(";")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.eat("if")

        self.eat("(")
        self.compile_expression()
        self.eat(")")

        self.vmwriter.write_arithmetic("NEG")
        self.vmwriter.write_if(f"IF_FALSE_{self.class_name}.{self.subroutine_name}.{self.if_counter}")

        self.eat("{")
        self.compile_statements()
        self.eat("}")

        self.vmwriter.write_goto(f"IF_END_{self.class_name}.{self.subroutine_name}.{self.if_counter}")
        self.vmwriter.write_label(f"IF_FALSE_{self.class_name}.{self.subroutine_name}.{self.if_counter}")

        if self.matches_keyword("else"):
            self.eat("else")
            self.eat("{")
            self.compile_statements()
            self.eat("}")

        self.vmwriter.write_label(f"IF_END_{self.class_name}.{self.subroutine_name}.{self.if_counter}")
        self.if_counter += 1

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.vmwriter.write_label(f"WHILE_{self.class_name}.{self.subroutine_name}.{self.while_counter}")

        self.eat("while")
        self.eat("(")
        self.compile_expression()
        self.eat(")")

        self.vmwriter.write_arithmetic("NEG")
        self.vmwriter.write_if(f"WHILE_END_{self.class_name}.{self.subroutine_name}.{self.while_counter}")

        self.eat("{")
        self.compile_statements()
        self.eat("}")

        self.vmwriter.write_goto(f"WHILE_{self.class_name}.{self.subroutine_name}.{self.while_counter}")
        self.vmwriter.write_label(f"WHILE_END_{self.class_name}.{self.subroutine_name}.{self.while_counter}")
        self.while_counter += 1

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.eat("do")
        identifier = self.eat(types="IDENTIFIER")

        if not self.matches_symbol("("):
            self.eat(".")
            identifier += "." + self.eat(types="IDENTIFIER")
        
        self.eat("(")
        num_of_params = self.compile_expression_list()
        self.eat(")")

        self.vmwriter.write_call(identifier, num_of_params)
        self.vmwriter.write_pop("TEMP", 0)
        
        self.eat(";")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.eat("return")
        
        if self.matches_symbol(";"):
            self.vmwriter.write_push("CONST", 0)
        else:
            self.compile_expression()
        
        self.vmwriter.write_return()

        self.eat(";")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        operator_stack: list = []
        
        self.compile_term()

        while self.matches_symbol(*OPERATORS):
            operator = self.eat(types="SYMBOL")
            operator_stack.append(operator)

            self.compile_term()
        
        while len(operator_stack) > 0:
            operator = operator_stack.pop()
            self.handle_operator(operator)

    def handle_operator(self, operator: None | str) -> None:
        # '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
        if operator == '*':
            self.vmwriter.write_call("Math.multiply", 2)
        elif operator == '/':
            self.vmwriter.write_call("Math.divide", 2)
        else:
            self.vmwriter.write_arithmetic(OPERATOR_TO_VM_DICT[operator])

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        token_type: TOKEN_TYPE = self.tokenizer.token_type()

        if token_type in ["INT_CONST", "STRING_CONST"] or self.matches_keyword(*KEYWORD_CONSTANTS):
            token = self.eat(types=["INT_CONST", "STRING_CONST", "KEYWORD"])

            if token_type == "INT_CONST":
                self.vmwriter.write_push("CONST", int(token))
            elif token_type == "STRING_CONST":
                self.write_string(token)
                # self.vmwriter.write_call("String.dispose", 1)
            elif token in ["false", "null"]:
                self.vmwriter.write_push("CONST", 0)
            elif token == "true":
                self.vmwriter.write_push("CONST", 1)
                self.vmwriter.write_arithmetic("NEG")
            elif token == "this":
                self.vmwriter.write_push("POINTER", 0)
            return

        if self.matches_symbol(*UNARY_OPERATORS):
            unary_operator = self.eat()
            
            self.compile_term()
            
            self.vmwriter.write_arithmetic(UNARY_OPERATOR_TO_VM_DICT[unary_operator])
            return

        if self.matches_symbol("("):
            self.eat("(")
            self.compile_expression()
            self.eat(")")
            return

        identifier = self.eat(types="IDENTIFIER")

        if self.matches_symbol("["):
            self.vmwriter.write_push(self.symbol_table.kind_of(identifier), self.symbol_table.index_of(identifier))
            
            self.eat("[")
            self.compile_expression()
            self.eat("]")

            self.vmwriter.write_arithmetic("ADD")
            self.vmwriter.write_pop("POINTER", 1)
            self.vmwriter.write_push("THAT", 0)

        elif self.matches_symbol("(", "."):    
            if self.matches_symbol("."):
                identifier += self.eat(".")
                identifier += self.eat(types="IDENTIFIER")
        
            self.eat("(")
            arg_count = self.compile_expression_list()
            self.eat(")")

            self.vmwriter.write_call(identifier, arg_count)

    def write_string(self, string: str) -> None:
        self.vmwriter.write_push("constant", len(string))
        self.vmwriter.write_call("String.new", 1)

        for c in string:
            self.vmwriter.write_push("constant", ord(c))
            self.vmwriter.write_call("String.appendChar", 2)

    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        num_of_params = 0
        if self.matches_symbol(")"):
            return num_of_params

        self.compile_expression()
        num_of_params += 1

        while self.matches_symbol(","):
            self.eat(",")
            self.compile_expression()
            num_of_params += 1

        return num_of_params
