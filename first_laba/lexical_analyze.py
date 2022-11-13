from enum import Enum


class EState(Enum):
    START = 0
    IDENTIFIER = 1
    CONSTANT = 2
    ERROR = 3
    FINAL = 4
    COMPARISON = 5
    REVERSE_COMPARISON = 6
    ARITHMETIC_OPERATION = 7
    ASSIGNMENT = 8


class ELexType(Enum):
    DO = 0
    UNTIL = 1
    LOOP = 2
    RELATION = 3
    AND = 4
    OR = 5
    ARITHMETIC_OPERATION = 6
    ASSIGNMENT = 7
    UNDEFINED = 8


class ELexClass(Enum):
    KEYWORD = 0
    IDENTIFIER = 1
    CONSTANT = 2
    SPECIAL_SYMBOLS = 3
    UNDEFINED = 4


class Lexeme:
    def __init__(self, _type, _cls, _val):
        self.type = _type
        self.cls = _cls
        self.val = _val

    def __str__(self):
        return f'type: {self.type.name}, class: {self.cls.name}, value: {self.val}'


class Lexics:
    def __init__(self, filepath: str):
        self.lexemes = []
        self.filepath = filepath

    def start(self):
        with open(self.filepath, 'r', encoding='utf-8') as code_reader:
            code = code_reader.read().replace('\n', ' ').lower().split(' ')
            print(code)

            state = EState.START
            prev_state = None
            addable = None
            lexeme_index = 0

            while state != EState.ERROR and state != EState.FINAL:
                prev_state = state
                addable = True

                if lexeme_index == len(code) and state != EState.ERROR:
                    state = EState.FINAL
                    break

                if lexeme_index == len(code):
                    break

                symbol = code[lexeme_index]

                match state:
                    case EState.START:
                        if symbol.isdigit():
                            state = EState.CONSTANT
                        elif symbol.isalpha():
                            state = EState.IDENTIFIER
                        elif symbol == '>' or symbol == '>=':
                            state = EState.COMPARISON
                        elif symbol == '<' or symbol == '<=':
                            state = EState.REVERSE_COMPARISON
                        elif symbol in ['+', '-', '*', '/']:
                            state = EState.ARITHMETIC_OPERATION
                        elif symbol == '=':
                            state = EState.ASSIGNMENT
                        else:
                            state = EState.ERROR
                            addable = False
                    case EState.IDENTIFIER:
                        if symbol == ' ':
                            state = EState.START
                        elif symbol.isdigit():
                            state = EState.CONSTANT
                        elif symbol.isalnum():
                            state = EState.IDENTIFIER
                        elif symbol == '<':
                            state = EState.REVERSE_COMPARISON
                        elif symbol == '>':
                            state = EState.COMPARISON
                        elif symbol == '=':
                            state = EState.ASSIGNMENT
                        elif symbol in ['+', '-', '*', '/']:
                            state = EState.ARITHMETIC_OPERATION
                        elif symbol == ':':
                            state = EState.ASSIGNMENT
                        else:
                            state = EState.ERROR
                            addable = False
                    case EState.CONSTANT:
                        if symbol == ' ':
                            state = EState.START
                        elif symbol.isdigit():
                            state = EState.CONSTANT
                        elif symbol.isalpha():
                            state = EState.IDENTIFIER
                        elif symbol == '<':
                            state = EState.REVERSE_COMPARISON
                        elif symbol == '>':
                            state = EState.COMPARISON
                        elif symbol == '=':
                            state = EState.ASSIGNMENT
                        elif symbol in ['+', '-', '/', '*']:
                            state = EState.ARITHMETIC_OPERATION
                        else:
                            state = EState.ERROR
                            addable = False
                    case EState.ERROR:
                        pass
                    case EState.FINAL:
                        pass
                    case EState.COMPARISON:
                        if symbol == ' ':
                            state = EState.START
                        elif symbol.isdigit():
                            state = EState.CONSTANT
                        elif symbol == '=':
                            state = EState.START
                        elif symbol.isalpha():
                            state = EState.IDENTIFIER
                        else:
                            state = EState.ERROR
                            addable = False
                    case EState.REVERSE_COMPARISON:
                        if symbol == ' ':
                            state = EState.START
                        elif symbol == '>':
                            state = EState.START
                        elif symbol == '=':
                            state = EState.START
                        elif symbol.isalpha():
                            state = EState.IDENTIFIER
                        elif symbol.isdigit():
                            state = EState.CONSTANT
                        else:
                            state = EState.ERROR
                            addable = False
                    case EState.ARITHMETIC_OPERATION:
                        if symbol == ' ':
                            state = EState.START
                        elif symbol.isdigit():
                            state = EState.CONSTANT
                        elif symbol.isalpha():
                            state = EState.IDENTIFIER
                        elif symbol in ['+', '-', '*', '/']:
                            state = EState.ARITHMETIC_OPERATION
                        else:
                            state = EState.ERROR
                            addable = False
                    case EState.ASSIGNMENT:
                        if symbol == '=':
                            state = EState.COMPARISON
                        elif symbol.isdigit():
                            state = EState.CONSTANT
                        elif symbol.isalpha():
                            state = EState.IDENTIFIER
                        else:
                            state = EState.ERROR
                            addable = False

                if addable:
                    self.add_lexeme(state, code[lexeme_index])
                lexeme_index += 1

            return state == EState.FINAL

    def add_lexeme(self, prev_state, value):
        lex_type = ELexType.UNDEFINED
        lex_class = ELexClass.UNDEFINED

        if prev_state == EState.ARITHMETIC_OPERATION:
            lex_type = ELexType.ARITHMETIC_OPERATION
            lex_class = ELexClass.SPECIAL_SYMBOLS
        elif prev_state == EState.ASSIGNMENT:
            lex_class = ELexClass.SPECIAL_SYMBOLS
            if value == '==':
                lex_type = ELexType.RELATION
            else:
                lex_type = ELexType.ASSIGNMENT
        elif prev_state == EState.CONSTANT:
            lex_type = ELexType.UNDEFINED
            lex_class = ELexClass.CONSTANT
        elif prev_state == EState.REVERSE_COMPARISON or prev_state == EState.COMPARISON:
            lex_type = ELexType.RELATION
            lex_class = ELexClass.SPECIAL_SYMBOLS
        elif prev_state == EState.IDENTIFIER:
            is_keyword = True
            if value == 'or':
                lex_type = ELexType.OR
            elif value == 'and':
                lex_type = ELexType.AND
            elif value == 'do':
                lex_type = ELexType.DO
            elif value == 'until':
                lex_type = ELexType.UNTIL
            elif value == 'loop':
                lex_type = ELexType.LOOP
            else:
                lex_type = ELexType.UNDEFINED
                is_keyword = False

            if is_keyword:
                lex_class = ELexClass.KEYWORD
            else:
                lex_class = ELexClass.IDENTIFIER

        lexeme = Lexeme(lex_type, lex_class, value)

        self.lexemes.append(lexeme)
