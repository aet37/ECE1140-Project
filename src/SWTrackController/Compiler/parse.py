"""Classes used during the parsing process"""

import logging
from src.SWTrackController.Compiler.lexer import TokenType, CompilationError

logger = logging.getLogger(__name__)

TAG_CHARACTER_LIMIT = 7

class Parser:
    """Class used to parse source code"""
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.tags = set()
        self.routines = set()
        self.jumps = set()
        self.events = set()
        self.emitted_events = set()
        self.stack = []
        self.main_flag = False

        self.previous_token = None
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
        self.previous_token = self.current_token
        self.current_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def abort(self, message):
        """Exits the program and prints the message.

        :param str message: Message to be printed prior to exiting

        """
        raise CompilationError("Parsing error line #{} : {}".format(self.lexer.line_number - 1, message))

    def program(self, program_name=''):
        """Production step for program ::= {statement}

        :param str program_name: Name of the program
        """
        logger.info("PROGRAM")

        if program_name == '':
            self.emitter.emit_line("START_DOWNLOAD")
        else:
            self.emitter.emit_line("START_DOWNLOAD " + program_name)

        # Parse all of the statements
        while not self.check_token(TokenType.EOF):
            self.statement()

        # Check to ensure all statements have ends
        if len(self.stack) != 0:
            self.abort("Missing end statements")

        # Check that all emitted events correspond to actual events
        for event in self.emitted_events:
            if event not in self.events:
                self.abort("Emitted event {} does not correspond to a task".format(event))

        # Check that all JSR instructions jump to valid routines
        for jump in self.jumps:
            if jump not in self.routines:
                self.abort("Routine {} does not exist".format(jump))

        self.emitter.emit_line("END_DOWNLOAD")

        # Write to the file and return it
        self.emitter.write_file()

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
            self.task()
        elif self.check_token(TokenType.ROUTINE):
            logger.info("STATEMENT-ROUTINE")
            self.next_token()
            self.routine()
        elif self.check_token(TokenType.RUNG):
            logger.info("STATEMENT-RUNG")
            self.next_token()
            self.rung()
        elif (self.check_token(TokenType.XIC) |
              self.check_token(TokenType.XIO) |
              self.check_token(TokenType.OTE) |
              self.check_token(TokenType.OTL) |
              self.check_token(TokenType.OTU) |
              self.check_token(TokenType.JSR) |
              self.check_token(TokenType.RET) |
              self.check_token(TokenType.EMIT)):
            logger.info("STATEMENT-INSTRUCTION")
            self.next_token()
            self.instruction()
        elif self.check_token(TokenType.ENDRUNG):
            logger.info("STATEMENT-ENDRUNG")
            self.next_token()
            self.end_rung()
        elif self.check_token(TokenType.ENDROUTINE):
            logger.info("STATEMENT-ENDROUTINE")
            self.next_token()
            self.end_routine()
        elif self.check_token(TokenType.ENDTASK):
            logger.info("STATEMENT-ENDTASK")
            self.next_token()
            self.end_task()
        elif self.check_token(TokenType.TAG):
            logger.info("STATEMENT-TAG")
            self.next_token()
            self.tag()
        else:
            self.abort("Invalid statement at {} ({})".format(self.current_token.text,
                                                             self.current_token.type.name))

        # All statements end in nl
        self.new_line()

    def task(self):
        """Production step for "TASK" taskType identifier"""
        # Verify we are at the outter most level
        if len(self.stack) != 0:
            self.abort("Tasks may not be inside of other structures")
        else:
            self.stack.append(self.previous_token.type.name)
        self.emitter.emit("CREATE_TASK ")

        self.task_type()
        self.match(TokenType.IDENTIFIER)
        self.emitter.emit_line(" " + self.previous_token.text)

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
        self.emitter.emit(self.previous_token.type.name + " ")
        self.match(TokenType.EQ)
        self.match(TokenType.NUMBER)
        self.emitter.emit(self.previous_token.text)

        PERIOD_LIMIT = 20
        if (int(self.previous_token.text) < PERIOD_LIMIT):
            self.abort("Period below allowable limit {}".format(PERIOD_LIMIT))

    def event_type(self):
        """Production step for eventType ::= 'EVENT' '=' identifier"""
        logger.info("EVENTTYPE")

        # Require the following tokens
        self.match(TokenType.EVENT)
        self.emitter.emit(self.previous_token.type.name + " ")
        self.match(TokenType.EQ)
        self.match(TokenType.IDENTIFIER)
        self.emitter.emit(self.previous_token.text)

        # Add the event to the list
        self.events.add(self.previous_token.text)

    def routine(self):
        """Production step for "ROUTINE" identifier"""
        # Ensure we are inside of a task
        if (len(self.stack) == 0) or (self.stack[-1] != 'TASK'):
            self.abort("Routines must be defined inside of a task")
        else:
            self.stack.append(self.previous_token.type.name)

        self.emitter.emit("CREATE_ROUTINE ")
        self.match(TokenType.IDENTIFIER)
        self.emitter.emit_line(self.previous_token.text)

        # Determine whether this is a Main routine or not
        if self.previous_token.text == 'Main':
            if self.main_flag:
                self.abort("There can only be one Main routine")
            else:
                self.main_flag = True

    def rung(self):
        """Production step for "RUNG" identifier and "RUNG"""
        # Ensure we are inside of a routine
        if (len(self.stack) == 0) or (self.stack[-1] != 'ROUTINE'):
            self.abort("Rungs must be defined inside of a routine")
        else:
            self.stack.append(self.previous_token.type.name)

        self.emitter.emit("CREATE_RUNG")
        if self.check_token(TokenType.IDENTIFIER):
            logger.info("STATEMENT-NAMED-RUNG")
            self.next_token()
            self.emitter.emit_line(" " + self.previous_token.text)
        else:
            self.emitter.emit_line('')

    def instruction(self):
        """Production step for instruction"""
        instruction_type = self.previous_token.type.name
        self.emitter.emit("CREATE_INSTRUCTION " + self.previous_token.type.name)

        if instruction_type == 'RET':
            self.emitter.emit_line('')
            return
        else:
            self.match(TokenType.IDENTIFIER)

        if instruction_type == 'JSR':
            # Add the routine name to a list to be verified later
            # during compilation
            self.jumps.add(self.previous_token.text)
        elif instruction_type == 'EMIT':
            # Add the event name to a list to be verified later
            # during compilation
            self.emitted_events.add(self.previous_token.text)
        else:
            # Verify that the tag exists
            if self.previous_token.text not in self.tags:
                self.abort("Referencing tag {} before assignment".format(self.previous_token.text))
            else:
                self.emitter.emit_line(" " + self.previous_token.text)

    def end_rung(self):
        """Production step for "ENDRUNG"""
        if self.stack.pop() != 'RUNG':
            self.abort("Missing matching RUNG")

    def end_routine(self):
        """Production step for "ENDROUTINE"""
        if self.stack.pop() != 'ROUTINE':
            self.abort("Missing matching ENDRUNG")

    def end_task(self):
        """Production step for "ENDTASK"""
        if len(self.stack) == 0:
            self.abort("Too many end statements")

        if self.stack.pop() != 'TASK':
            self.abort("Missing matching ENDROUTINE")

        if not self.main_flag:
            self.abort("There must be a single Main routine")
        else:
            self.main_flag = False

    def tag(self):
        """Production step for "TAG" identifier "=" (true | false)"""
        self.match(TokenType.IDENTIFIER)
        self.emitter.emit("CREATE_TAG " + self.previous_token.text)

        # Enforce a character limit on tag names
        if len(self.previous_token.text) > TAG_CHARACTER_LIMIT:
            self.abort("Tag name {} too long. The limit is {} characters".format(self.previous_token.text,
                                                                                 TAG_CHARACTER_LIMIT))

        self.tags.add(self.previous_token.text)
        self.match(TokenType.EQ)

        # Either true or false is acceptable
        if self.check_token(TokenType.TRUE):
            self.match(TokenType.TRUE)
        else:
            self.match(TokenType.FALSE)

        self.emitter.emit_line(" " + self.previous_token.type.name)

    def new_line(self):
        """Production step for nl ::= '\n'+"""
        logger.info("NEWLINE")

        # Require one new line, but allow multiple
        self.match(TokenType.NEWLINE)
        while self.check_token(TokenType.NEWLINE):
            self.next_token()
