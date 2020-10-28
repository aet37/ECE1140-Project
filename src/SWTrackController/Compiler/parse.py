"""Classes used during the parsing process"""

import sys
import logging
from lexer import TokenType
from emitter import Emitter

logger = logging.getLogger(__name__)

class Parser:
    """Class used to parse source code"""
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set()

        self.current_token = None
        self.peek_token = None

        # Call next token twice to initialize current and peek
        self.next_token()
        self.next_token()

    def check_token(self, token_type):
        """Compares the current token with the given kind

        :param TokenType token_type: Type of token to compare with
        :return: Whether the current token is the same kind
        :rtype: bool

        """
        return token_type == self.current_token.type

    def check_peek(self, token_type):
        """Compares the peek token with the given kind

        :param TokenType token_type: Type of token to compare with
        :return: Whether the current token is the same kind
        :rtype: bool

        """
        return token_type == self.peek_token.type

    def match(self, token_type):
        """Tries to match the current token with the given type

        :param TokenType token_type: Type of token to try matching with

        """
        if not self.check_token(token_type):
            self.abort("Expected {}, but found {}".format(token_type.name, self.current_token.text))
        self.next_token()

    def next_token(self):
        """Uses the lexer to get the next token"""
        self.current_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    @staticmethod
    def abort(message):
        """Exits the program and prints the message.

        :param str message: Message to be printed prior to exiting

        """
        sys.exit("Parsing error : " + message)

    def program(self):
        """Production step for program ::= {statement}"""
        logger.info("PROGRAM")

        # Parse all of the statements
        while not self.check_token(TokenType.EOF):
            self.statement()

    # pylint: disable=too-many-branches
    def statement(self):
        """Production step for:
        statement ::= "TASK" taskType identifier nl |
                      "ROUTINE" identifier nl |
                      "RUNG" identifier nl |
                      "RUNG" nl |
                      instruction nl |
                      "ENDRUNG" nl |
                      "ENDROUTINE" nl |
                      "ENDTASK" nl |
                      "TAG" identifier "=" (true | false) nl

        """
        logger.info("STATEMENT")

        if self.check_token(TokenType.TASK):
            logger.info("STATEMENT-TASK")
            self.next_token()
            self.task_type()
            self.match(TokenType.IDENTIFIER)
        elif self.check_token(TokenType.ROUTINE):
            logger.info("STATEMENT-ROUTINE")
            self.next_token()
            self.match(TokenType.IDENTIFIER)
        elif self.check_token(TokenType.RUNG):
            logger.info("STATEMENT-RUNG")
            self.next_token()
            if self.check_token(TokenType.IDENTIFIER):
                logger.info("STATEMENT-NAMED-RUNG")
                self.next_token()
        elif (self.check_token(TokenType.XIC) |
              self.check_token(TokenType.XIO) |
              self.check_token(TokenType.OTE) |
              self.check_token(TokenType.OTL) |
              self.check_token(TokenType.OTU) |
              self.check_token(TokenType.JSR) |
              self.check_token(TokenType.EMIT)):
            logger.info("STATEMENT-INSTRUCTION")
            self.next_token()
            self.match(TokenType.IDENTIFIER)
        elif self.check_token(TokenType.RET):
            logger.info("STATEMENT-RET")
            self.next_token()
        elif self.check_token(TokenType.ENDRUNG):
            logger.info("STATEMENT-ENDRUNG")
            self.next_token()
        elif self.check_token(TokenType.ENDROUTINE):
            logger.info("STATEMENT-ENDROUTINE")
            self.next_token()
        elif self.check_token(TokenType.ENDTASK):
            logger.info("STATEMENT-ENDTASK")
            self.next_token()
        elif self.check_token(TokenType.TAG):
            logger.info("STATEMENT-TAG")
            self.next_token()
            self.match(TokenType.IDENTIFIER)
            self.match(TokenType.EQ)

            # Either true or false is acceptable
            if self.check_token(TokenType.TRUE):
                self.match(TokenType.TRUE)
            else:
                self.match(TokenType.FALSE)
        else:
            self.abort("Invalid statement at {} ({})".format(self.current_token.text,
                                                             self.current_token.type.name))

        # All statements end in nl
        self.new_line()

    def task_type(self):
        """Production step for taskType ::= "<" (periodType | eventType) ">"""
        logger.info("TASKTYPE")

        # Require an open bracket
        self.match(TokenType.OPEN_ANGLE)

        # Determine whether it's periodic or event driven
        if self.check_token(TokenType.PERIOD):
            self.period_type()
        elif self.check_token(TokenType.EVENT):
            self.event_type()
        else:
            self.abort("Invalid task type {}".format(self.current_token.text))

        # Require a closing bracket
        self.match(TokenType.CLOSE_ANGLE)

    def period_type(self):
        """Production step for periodType ::= 'PERIOD' '=' number"""
        logger.info("PERIODTYPE")

        # Require the following tokens
        self.match(TokenType.PERIOD)
        self.match(TokenType.EQ)
        self.match(TokenType.NUMBER)

    def event_type(self):
        """Production step for eventType ::= 'EVENT' '=' identifier"""
        logger.info("EVENTTYPE")

        # Require the following tokens
        self.match(TokenType.EVENT)
        self.match(TokenType.EQ)
        self.match(TokenType.IDENTIFIER)

    def new_line(self):
        """Production step for nl ::= '\n'+"""
        logger.info("NEWLINE")

        # Require one new line, but allow multiple
        self.match(TokenType.NEWLINE)
        while self.check_token(TokenType.NEWLINE):
            self.next_token()
