"""Class used to lex an input string"""


import logging
logger = logging.getLogger(__name__)

class Lexer:
    def __init__(self, input):

        # Append a \n to simplify lexing
        self.source_code = input + '\n'

        self.current_character = ''
        self.current_position = -1
        self.next_character()

    def next_character(self):
        """Processes the next character"""
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

    