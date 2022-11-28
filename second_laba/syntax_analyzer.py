from first_laba.lexical_analyze import ELexType, ELexClass, Lexeme
from third_laba.entry import Entry
from third_laba.entry_type import EEntryType
from third_laba.cmd import ECmd


class SyntaxAnalyzer:
    def __init__(self, lexemes):
        self.lexemes = lexemes
        self.errors = []
        self.pos = 0
        self.entries_list = []

    def start(self):
        self.pos = 0
        self.errors = []
        self.entries_list = []

        result = self.until_statement()

        if result:
            return True, self.entries_list
        return False, []

    def until_statement(self) -> bool:
        idx_first = len(self.entries_list)
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

        idx_jmp_exit = self.write_cmd_ptr(-1)
        self.write_cmd(ECmd.JZ)

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

        self.write_cmd_ptr(idx_first)
        idx_last = self.write_cmd(ECmd.JMP)
        self.set_cmd_ptr(idx_jmp_exit, idx_last + 1)

        return True

    def condition(self) -> bool:
        if not self.log_expr():
            return False
        while self.lexemes[self.pos].type == ELexType.OR:
            print(self.lexemes[self.pos].val, self.lexemes[self.pos].type, self.pos)
            self.pos += 1
            if not self.log_expr():
                return False

            self.write_cmd(ECmd.OR)

        return True

    def log_expr(self) -> bool:
        if not self.rel_expr():
            return False

        return True

    def rel_expr(self) -> bool:
        if not self.arith_expr():
            return False
        if self.lexemes[self.pos].type == ELexType.RELATION:
            print(self.lexemes[self.pos].val, self.lexemes[self.pos].type, self.pos)
            cmd = None
            match self.lexemes[self.pos].val:
                case '<':
                    cmd = ECmd.CMPL
                case '<=':
                    cmd = ECmd.CMPLE
                case '>':
                    cmd = ECmd.CMPG
                case '>=':
                    cmd = ECmd.CMPGE
                case '==':
                    cmd = ECmd.CMPE
                case '<>':
                    cmd = ECmd.CMPNE
            self.pos += 1
            if not self.arith_expr():
                return False

            self.write_cmd(cmd)

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
        if self.lexemes[self.pos].cls == ELexClass.IDENTIFIER:
            self.write_var(self.pos)
        elif self.lexemes[self.pos].cls == ELexClass.CONSTANT:
            self.write_const(self.pos)
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
        self.write_var(self.pos)
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

        self.write_cmd(ECmd.SET)

        return True

    def arith_expr(self) -> bool:
        if not self.operand():
            return False
        while self.lexemes[self.pos].type == ELexType.ARITHMETIC_OPERATION:
            print(self.lexemes[self.pos].val, self.lexemes[self.pos].type, self.pos)
            cmd = None
            match self.lexemes[self.pos].val:
                case '+':
                    cmd = ECmd.ADD
                case '-':
                    cmd = ECmd.SUB
                case '*':
                    cmd = ECmd.MUL
                case '/':
                    cmd = ECmd.DIV
            self.pos += 1
            if not self.operand():
                return False

            self.write_cmd(cmd)

        return True

    def write_cmd(self, cmd: ECmd):
        command = Entry(entry_type=EEntryType.CMD, cmd=cmd)

        self.entries_list.append(command)

        return len(self.entries_list) - 1

    def write_var(self, idx: int):
        variable = Entry(entry_type=EEntryType.VAR, value=self.lexemes[idx].val)

        self.entries_list.append(variable)

        return len(self.entries_list) - 1

    def write_const(self, idx: int):
        constant = Entry(entry_type=EEntryType.CONST, value=self.lexemes[idx].val)

        self.entries_list.append(constant)

        return len(self.entries_list) - 1

    def write_cmd_ptr(self, ptr):
        cmd_ptr = Entry(entry_type=EEntryType.CMD_PTR, cmd_ptr=ptr)

        self.entries_list.append(cmd_ptr)

        return len(self.entries_list) - 1

    def set_cmd_ptr(self, idx: int, ptr: int):
        self.entries_list[idx].cmd_ptr = ptr
