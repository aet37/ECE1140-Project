"""Module containing classes relevant to the lexing stage"""

import enum
import logging
logger = logging.getLogger(__name__)

class Lexer:
    """Class used to perform lexing on an input string"""
    def __init__(self, input_string):

        # Append a \n to simplify lexing
        self.source_code = input_string + '\n'

        self.line_number = 1
        self.current_character = ''
        self.current_position = -1
        self.next_character()

    def next_character(self):
        """Processes the next character"""
        if self.current_character == '\n':
            self.line_number += 1

        self.current_position += 1
        if self.current_position >= len(self.source_code):
            self.current_character = '\0'
        else:
            self.current_character = self.source_code[self.current_position]

        logger.debug("self.current_character set to %s", self.current_character)

    def peek(self):
        """Returns the next character that will be read

        :return: Next character that will be read
        :rtype: str
        """
        if self.current_position + 1 >= len(self.source_code):
            return '\0'
        return self.source_code[self.current_position + 1]

    def abort(self, message):
        """Exits the program and prints the message.

        :param str message: Message to be printed prior to exiting

        """
        raise CompilationError("Lexing error line #{} : {}".format(self.line_number, message))

    def skip_whitespace(self):
        """Skips over whitespace characters"""
        while ((self.current_character == ' ') or
               (self.current_character == '\t') or
               (self.current_character == '\r')):
            self.next_character()

    def skip_comment(self):
        """Skips over comments"""
        if self.current_character == '#':
            while self.current_character != '\n':
                self.next_character()

    # pylint: disable=too-many-branches
    def get_token(self):
        """Retrieves the next token

        :return: Next token in the input string
        :rtype: Token
        """
        self.skip_whitespace()
        self.skip_comment()
        token = None

        if self.current_character == '=':
            token = Token(self.current_character, TokenType.EQ)
        elif self.current_character == '<':
            token = Token(self.current_character, TokenType.OPEN_ANGLE)
        elif self.current_character == '>':
            token = Token(self.current_character, TokenType.CLOSE_ANGLE)
        elif self.current_character.isdigit():
            # Token is a number, so get all the next digits
            start_position = self.current_position
            while self.peek().isdigit():
                self.next_character()

            # It could have a decimal point
            if self.peek() == '.':
                self.next_character()

                # We need to have at least one digit after a decimal point
                if not self.peek().isdigit():
                    self.abort("Illegal character in number")

                # Get all the digits after the decimal point
                while self.peek().isdigit():
                    self.next_character()

            # Construct the substring and token
            number = self.source_code[start_position : self.current_position + 1]
            token = Token(number, TokenType.NUMBER)
        elif self.current_character.isalpha():
            # Token is either a keyword or identifier, so get all the next characters
            start_position = self.current_position
            while (self.peek().isalpha()) or (self.peek().isdigit()):
                self.next_character()

            # Construct the substring and check it it's a keyword
            word = self.source_code[start_position : self.current_position + 1]
            keyword = Token.is_keyword(word)

            if keyword is None:
                token = Token(word, TokenType.IDENTIFIER)
            else:
                token = Token(word, keyword)
        elif self.current_character == '\n':
            token = Token(self.current_character, TokenType.NEWLINE)
        elif self.current_character == '\0':
            token = Token('', TokenType.EOF)
        else:
            # Unknown token so abort
            self.abort("Unknown token: " + self.current_character)

        self.next_character()
        return token

# pylint: disable=too-few-public-methods
class Token:
    """Class used to represent a single token"""
    def __init__(self, token_text, token_type):
        self.text = token_text
        self.type = token_type

    @staticmethod
    def is_keyword(token_text):
        """Determines whether the given text is a keyword

        :param str token_text: Text to be checked
        :return: Keyword that the text is or None if it's not a keyword
        :rtype: TokenType
        :note: This method relies on all keywords being greater than 100 in the enum

        """
        for token_type in TokenType:
            if (token_type.name == token_text) and (token_type.value >= 100):
                return token_type
        return None

class TokenType(enum.Enum):
    """Enum to represent types of tokens"""
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENTIFIER = 2
    STRING = 3

    TAG = 101
    TASK = 102
    ENDTASK = 103
    PERIOD = 104
    EVENT = 105
    ROUTINE = 106
    ENDROUTINE = 107
    RUNG = 108
    ENDRUNG = 109
    FALSE = 110
    TRUE = 111
    XIC = 112
    XIO = 113
    OTE = 114
    OTL = 115
    OTU = 116
    JSR = 117
    RET = 118
    EMIT = 119

    EQ = 201
    OPEN_ANGLE = 202
    CLOSE_ANGLE = 203

class CompilationError(Exception):
    """Class to represent a general compilation error"""
