from first_laba.lexical_analyze import ELexType, ELexClass, Lexeme


class SyntaxAnalyzer:
    def __init__(self, lexemes):
        self.lexemes = lexemes
        self.errors = []
        self.pos = 0

    def start(self):
        self.pos = 0
        self.errors = []

        return self.until_statement()

    def until_statement(self) -> bool:
        print(self.lexemes[self.pos].val, self.lexemes[self.pos].type, self.pos)
        if self.lexemes[self.pos].type != ELexType.DO:
            error = {
                'error_text': 'Ожидается ключевое слово do.',
                'pos': self.pos,
            }
            print(f'{error["error_text"]} {error["pos"]}')
            self.errors.append(error)
            return False
        self.pos += 1

        print(self.lexemes[self.pos].val, self.lexemes[self.pos].type, self.pos)
        if self.lexemes[self.pos].type != ELexType.UNTIL:
            error = {
                'error_text': 'Ожидается ключевое слово until.',
                'pos': self.pos,
            }
            print(f'{error["error_text"]} {error["pos"]}')
            self.errors.append(error)
            return False
        self.pos += 1

        if not self.condition():
            return False

        if not self.statement():
            return False

        print(self.lexemes[self.pos].val, self.lexemes[self.pos].type, self.pos)
        if self.lexemes[self.pos].type != ELexType.LOOP:
            error = {
                'error_text': 'Ожидается ключевое слово loop.',
                'pos': self.pos,
            }
            print(f'{error["error_text"]} {error["pos"]}')
            self.errors.append(error)
            return False
        self.pos += 1

        return True

    def condition(self) -> bool:
        if not self.log_expr():
            return False
        while self.lexemes[self.pos].type == ELexType.OR:
            print(self.lexemes[self.pos].val, self.lexemes[self.pos].type, self.pos)
            self.pos += 1
            if not self.log_expr():
                return False

        return True

    def log_expr(self) -> bool:
        if not self.rel_expr():
            return False
        while self.lexemes[self.pos].type == ELexType.AND or self.lexemes[self.pos].type == ELexType.OR:
            print(self.lexemes[self.pos].val, self.lexemes[self.pos].type, self.pos)
            self.pos += 1
            if not self.rel_expr():
                return False

        return True

    def rel_expr(self) -> bool:
        if not self.arith_expr():
            return False
        if self.lexemes[self.pos].type == ELexType.RELATION:
            print(self.lexemes[self.pos].val, self.lexemes[self.pos].type, self.pos)
            self.pos += 1
            if not self.arith_expr():
                return False

        return True

    def operand(self) -> bool:
        print(self.lexemes[self.pos].val, self.lexemes[self.pos].type, self.pos)
        if self.lexemes[self.pos].type != ELexType.UNDEFINED:
            error = {
                'error_text': 'Ожидается переменная или константа.',
                'pos': self.pos,
            }
            print(f'{error["error_text"]} {error["pos"]}')
            self.errors.append(error)
            return False
        self.pos += 1
        return True

    def logical_op(self) -> bool:
        if self.lexemes[self.pos].type != ELexType.AND and self.lexemes[self.pos].type != ELexType.OR:
            error = {
                'error_text': 'Ожидается логическая операция.',
                'pos': self.pos,
            }
            print(f'{error["error_text"]} {error["pos"]}')
            self.errors.append(error)
            return False
        self.pos += 1
        return True

    def statement(self) -> bool:
        if self.lexemes[self.pos].type != ELexType.UNDEFINED and self.lexemes[self.pos].type != ELexClass.IDENTIFIER:
            error = {
                'error_text': 'Ожидается переменная.',
                'pos': self.pos,
            }
            print(f'{error["error_text"]} {error["pos"]}')
            self.errors.append(error)
            return False
        self.pos += 1

        print(self.lexemes[self.pos].val, self.lexemes[self.pos].type, self.pos)
        if self.lexemes[self.pos].type != ELexType.ASSIGNMENT:
            error = {
                'error_text': 'Ожидается присваивание.',
                'pos': self.pos,
            }
            print(f'{error["error_text"]} {error["pos"]}')
            self.errors.append(error)
            return False
        self.pos += 1
        if not self.arith_expr():
            return False

        return True

    def arith_expr(self) -> bool:
        if not self.operand():
            return False
        while self.lexemes[self.pos].type == ELexType.ARITHMETIC_OPERATION:
            print(self.lexemes[self.pos].val, self.lexemes[self.pos].type, self.pos)
            self.pos += 1
            if not self.operand():
                return False

        return True
