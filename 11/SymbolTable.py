"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from enum import Enum

class VARIABLE_KINDS(Enum): 
    STATIC = "STATIC"
    FIELD = "FIELD"
    ARG = "ARG"
    VAR = "VAR"

class DictionaryEntry:
    type : str
    kind : VARIABLE_KINDS
    index : int

    def __init__(self, type, kind, index):
        self.type = type
        self.kind = kind
        self.index = index

class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    static_count : int = 0
    field_count : int = 0
    arg_count : int = 0
    var_count : int = 0
    class_dictionary : dict[str, DictionaryEntry] = {}
    subroutine_dictionary : dict[str, DictionaryEntry] = {}

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        # Your code goes here!
        pass

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        self.subroutine_dictionary = {}
        self.arg_count = 0
        self.var_count = 0

    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        if kind in [VARIABLE_KINDS.STATIC, VARIABLE_KINDS.FIELD]:
            self.class_dictionary[name] = DictionaryEntry(type, kind, self.static_count if kind == VARIABLE_KINDS.STATIC else self.field_count)
        else:
            self.class_dictionary[name] = (type, kind, self.arg_count if kind == VARIABLE_KINDS.ARG else self.var_count)

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        match(kind):
            case VARIABLE_KINDS.STATIC.value:
                return self.static_count
            case VARIABLE_KINDS.FIELD.value:
                return self.field_count
            case VARIABLE_KINDS.ARG.value:
                return self.arg_count
            case VARIABLE_KINDS.VAR.value:
                return self.var_count
        return -1

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        value = self.subroutine_dictionary.get(name)
        if (value != None):
            return value[1]
        
        return self.class_dictionary.get(name)
        

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        # Your code goes here!
        pass

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        # Your code goes here!
        pass
