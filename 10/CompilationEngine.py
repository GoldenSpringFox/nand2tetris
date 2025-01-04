"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer, TOKEN_TYPE

TOKEN_TYPE_XML = {
    "KEYWORD": "keyword", 
    "SYMBOL": "symbol", 
    "IDENTIFIER": "identifier", 
    "INT_CONST": "integerConstant", 
    "STRING_CONST": "stringConstant"
}


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: JackTokenizer, output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world!\n")
        self.tokenizer = input_stream
        self.output_stream = output_stream
        self.tab_depth = 0

        self.tokenizer.advance()
    
    def eat(self, word: str = None, types: list[TOKEN_TYPE] = typing.get_args(TOKEN_TYPE)):
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
        
        if word is not None and token != word:
            raise Exception(f"Expected {word}. Found {token}")
        
        self.output_stream.write(f"{'\t' * self.tab_depth}<{TOKEN_TYPE_XML[token_type]}> {token} </{TOKEN_TYPE_XML[token_type]}>")
        self.tokenizer.advance()

    def matches_keyword(self, *words: str) -> bool:
        return self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword().lower() in words

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.output_stream("<class>")
        self.eat(word="class")
        self.eat(types=["IDENTIFIER"])
        self.eat(word="{")

        while self.matches_keyword('static', 'field'):
            self.compile_class_var_dec()
        while self.matches_keyword('constructor', 'function', 'method'):
            self.compile_subroutine()
        self.eat("}")
        self.output_stream("</class>")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        pass

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        pass

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        pass

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        pass

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        pass

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        pass

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        pass

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        pass

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        pass

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        pass

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        pass

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
        # Your code goes here!
        pass

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        pass
