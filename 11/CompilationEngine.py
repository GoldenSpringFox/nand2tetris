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
OPERANDS = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
UNARY_OPERANDS = ['-', '~', '^', '#']
KEYWORD_CONSTANTS = ["true", "false", "null", "this"]


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: JackTokenizer, symbol_table : SymbolTable, vmwriter : VMWriter) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.tokenizer = input_stream
        self.symbol_table = symbol_table
        self.vmwriter = vmwriter

        self.tokenizer.advance()
    
    def eat(self, words: str | list[str] = None,
            types: TOKEN_TYPE | list[TOKEN_TYPE] = ("KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST")):
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

        token = (str(token).replace("&", "&amp;").replace(">", "&gt;")
                 .replace("<", "&lt;").replace('"', "&quot;"))
        self.output_stream.write(f"<{TOKEN_TYPE_XML[token_type]}>"
                                 f" {token} </{TOKEN_TYPE_XML[token_type]}>\n")
        self.tokenizer.advance()

    def open_tag(self, tag: str):
        self.output_stream.write(f"<{tag}>\n")

    def close_tag(self, tag: str):
        self.output_stream.write(f"</{tag}>\n")

    def matches_keyword(self, *words: str) -> bool:
        return self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword().lower() in words
    
    def matches_symbol(self, *words: str) -> bool:
        return self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.keyword() in words

    def compile_type(self):
        if self.matches_keyword("int", "char", "boolean"):
            self.eat(types="KEYWORD")
        else:
            self.eat(types="IDENTIFIER")
    
    def check_if_type(self):
        return self.matches_keyword("int", "char", "boolean") or self.tokenizer.token_type() == "IDENTIFIER"

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.open_tag("class")

        self.eat("class")
        self.eat(types=["IDENTIFIER"])
        self.eat("{")

        while self.matches_keyword('static', 'field'):
            self.compile_class_var_dec()
        while self.matches_keyword('constructor', 'function', 'method'):
            self.compile_subroutine()
        self.eat("}")

        self.close_tag("class")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self.open_tag("classVarDec")
        
        self.eat(words=["static", "field"])
        
        self.compile_type()
        
        self.eat(types="IDENTIFIER")
        while self.matches_symbol(","):
            self.eat(types="SYMBOL")
            self.eat(types="IDENTIFIER")

        self.eat(";")

        self.close_tag("classVarDec")

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.open_tag("subroutineDec")

        self.eat(words=["constructor", "function", "method"])
        if self.matches_keyword("void"):
            self.eat()
        else:
            self.compile_type()

        self.eat(types="IDENTIFIER")

        self.eat("(")
        self.compile_parameter_list()
        self.eat(")")

        self.compile_subroutine_body()

        self.close_tag("subroutineDec")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        self.open_tag("parameterList")

        if self.check_if_type():
            self.compile_type()
            self.eat(types="IDENTIFIER")

            while self.matches_symbol(","):
                self.eat(types="SYMBOL")
                self.compile_type()
                self.eat(types="IDENTIFIER")
        
        self.close_tag("parameterList")

    def compile_subroutine_body(self) -> None:
        self.open_tag("subroutineBody")

        self.eat("{")

        while self.matches_keyword("var"):
            self.compile_var_dec()
        
        self.compile_statements()

        self.eat("}")

        self.close_tag("subroutineBody")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.open_tag("varDec")

        self.eat("var")

        self.compile_type()

        self.eat(types="IDENTIFIER")

        while self.matches_symbol(","):
            self.eat(",")
            self.eat(types="IDENTIFIER")

        self.eat(";")

        self.close_tag("varDec")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        self.open_tag("statements")

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
        self.open_tag("letStatement")

        self.eat("let")
        self.eat(types="IDENTIFIER")

        if self.matches_symbol("["):
            self.eat("[")
            self.compile_expression()
            self.eat("]")

        self.eat("=")

        self.compile_expression()

        self.eat(";")

        self.close_tag("letStatement")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.open_tag("ifStatement")

        self.eat("if")

        self.eat("(")
        self.compile_expression()
        self.eat(")")
        
        self.eat("{")
        self.compile_statements()
        self.eat("}")

        if self.matches_keyword("else"):
            self.eat("else")
            self.eat("{")
            self.compile_statements()
            self.eat("}")
        
        self.close_tag("ifStatement")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.open_tag("whileStatement")

        self.eat("while")
        
        self.eat("(")
        self.compile_expression()
        self.eat(")")
        
        self.eat("{")
        self.compile_statements()
        self.eat("}")
        
        self.close_tag("whileStatement")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.open_tag("doStatement")

        self.eat("do")
        self.compile_subroutine_call()

        self.eat(";")
        
        self.close_tag("doStatement")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.open_tag("returnStatement")

        self.eat("return")
        if self.matches_symbol(";"):
            self.eat(";")
        else:
            self.compile_expression()
            self.eat(";")
        
        self.close_tag("returnStatement")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.open_tag("expression")
        
        self.compile_term()

        while self.matches_symbol(*OPERANDS):
            self.eat(types="SYMBOL")
            self.compile_term()
        
        self.close_tag("expression")

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
        self.open_tag("term")
        
        token_type: TOKEN_TYPE = self.tokenizer.token_type()

        if (token_type in ["INT_CONST", "STRING_CONST"] or 
                self.matches_keyword(*KEYWORD_CONSTANTS)):
            self.eat(types=["INT_CONST", "STRING_CONST", "KEYWORD"])
            self.close_tag("term")
            return
        
        if self.matches_symbol(*UNARY_OPERANDS):
            self.eat()
            self.compile_term()
            self.close_tag("term")
            return

        if self.matches_symbol("("):
            self.eat("(")
            self.compile_expression()
            self.eat(")")
            self.close_tag("term")
            return


        self.eat(types="IDENTIFIER")
        
        if self.matches_symbol("["):
            self.eat("[")
            self.compile_expression()
            self.eat("]")
        
        elif self.matches_symbol("(", "."):
            self.compile_subroutine_call(True)
        
        self.close_tag("term")
            
    def compile_subroutine_call(self, ignore_first_element: bool = False) -> None:
        if not ignore_first_element:
            self.eat(types="IDENTIFIER")
        
        if not self.matches_symbol("("):
            self.eat(".")
            self.eat(types="IDENTIFIER")
            
        self.eat("(")
        self.compile_expression_list()
        self.eat(")")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.open_tag("expressionList")
        
        if self.matches_symbol(")"):
            self.close_tag("expressionList")
            return
        
        self.compile_expression()

        while self.matches_symbol(","):
            self.eat(",")
            self.compile_expression()        
        
        self.close_tag("expressionList")
        