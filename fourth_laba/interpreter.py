from third_laba.entry import Entry
from third_laba.entry_type import EEntryType
from third_laba.cmd import ECmd


class Interpreter:
    def __init__(
        self,
        syntax_result,
        syntax_response,
        entry_list: list[Entry] = [],
        stack: list = [],
        logs: list[str] = [],
    ):
        self.entry_list = entry_list
        self.stack = stack
        self.logs = logs
        self.syntax_result = syntax_result
        self.syntax_response = syntax_response

    @staticmethod
    def format_out(s):
        print(f'{s}')

    def start(self) -> bool:
        self.logs = []
        self.entry_list = self.syntax_response.copy()
        self.stack = []

        if self.syntax_result:
            self.enter_variable_values()
            print('Результат: ')
            self.interpret()
            print('------------------------------')

            for log in self.logs:
                print(log)

    def interpret(self):
        temp = None
        pos: int = 0
        self.log(pos)

        while pos < len(self.entry_list):
            if self.entry_list[pos].entry_type == EEntryType.CMD:
                cmd = self.entry_list[pos].cmd
                if cmd == ECmd.JMP:
                    pos = self.pop_val()
                elif cmd == ECmd.JZ:
                    temp = self.pop_val()

                    if self.pop_val() == 0:
                        pos += 1
                    else:
                        pos = temp
                elif cmd == ECmd.SET:
                    self.set_var_and_pop(self.pop_val())
                    pos += 1
                elif cmd == ECmd.ADD:
                    self.push_val(self.pop_val() + self.pop_val())
                    pos += 1
                elif cmd == ECmd.SUB:
                    self.push_val(-self.pop_val() + self.pop_val())
                    pos += 1
                elif cmd == ECmd.MUL:
                    self.push_val(self.pop_val() * self.pop_val())
                    pos += 1
                elif cmd == ECmd.DIV:
                    self.push_val(int(1.0 / self.pop_val() * self.pop_val()))
                    pos += 1
                elif cmd == ECmd.AND:
                    self.push_val(self.pop_val() != 0 and (1 if self.pop_val() != 0 else 0))
                    pos += 1
                elif cmd == ECmd.OR:
                    self.push_val(self.pop_val() != 0 or (1 if self.pop_val() != 0 else 0))
                    pos += 1
                elif cmd == ECmd.CMPE:
                    self.push_val(1 if self.pop_val() == self.pop_val() else 0)
                    pos += 1
                elif cmd == ECmd.CMPNE:
                    self.push_val(1 if self.pop_val() != self.pop_val() else 0)
                    pos += 1
                elif cmd == ECmd.CMPL:
                    self.push_val(1 if self.pop_val() > self.pop_val() else 0)
                    pos += 1
                elif cmd == ECmd.CMPLE:
                    self.push_val(1 if self.pop_val() >= self.pop_val() else 0)
                    pos += 1
                elif cmd == ECmd.CMPG:
                    self.push_val(1 if self.pop_val() < self.pop_val() else 0)
                    pos += 1
                elif cmd == ECmd.CMPGE:
                    self.push_val(1 if self.pop_val() <= self.pop_val() else 0)
                    pos += 1
                else:
                    print(':(')
            else:
                self.push_elem(self.entry_list[pos])
                pos += 1

            if pos < len(self.entry_list):
                self.log(pos)

        return True

    def log(self, pos: int) -> None:
        self.logs.append(f'Позиция: {pos} | '
                         f'Элемент: {self.get_entry_string(self.entry_list[pos])} | '
                         f'Значения переменных: {self.get_var_values()} | '
                         f'Стек: {self.get_stack_state()}')

    def pop_val(self) -> int:
        if len(self.stack) != 0:
            obj: Entry = self.stack.pop()

            match obj.entry_type:
                case EEntryType.VAR:
                    return obj.current_value
                case EEntryType.CONST:
                    return int(obj.value)
                case EEntryType.CMD:
                    return obj.cmd.value
                case EEntryType.CMD_PTR:
                    return obj.cmd_ptr
                case _:
                    raise Exception(';)')
        else:
            return 0

    def push_val(self, val: int) -> None:
        entry: Entry = Entry(entry_type=EEntryType.CONST, value=str(val))

        self.stack.append(entry)

    def push_elem(self, entry: Entry) -> None:
        if entry.entry_type == EEntryType.CMD:
            raise Exception('EntryType')

        self.stack.append(entry)

    def set_var_and_pop(self, val: int) -> None:
        variable: Entry = self.stack.pop()

        if variable.entry_type != EEntryType.VAR:
            raise Exception('EntryType')

        self.set_values_to_variables(variable.value, val)

    def get_entry_string(self, entry: Entry) -> str:
        if entry.entry_type == EEntryType.VAR:
            return entry.value
        elif entry.entry_type == EEntryType.CONST:
            return entry.value
        elif entry.entry_type == EEntryType.CMD:
            return str(entry.cmd)
        elif entry.entry_type == EEntryType.CMD_PTR:
            return str(entry.cmd_ptr)

        raise Exception('PostfixEntry')

    def get_stack_state(self) -> str:
        entries: list[Entry] = self.stack.copy()
        sb = ''

        for entry in entries:
            sb += f'{self.get_entry_string(entry)} '

        return sb

    def get_var_values(self) -> str:
        sb = ''

        entries = []
        for entry in self.entry_list:
            if entry.entry_type == EEntryType.VAR:
                entries.append({
                    'value': entry.value,
                    'current_value': entry.current_value
                })

        entries = list(map(dict, set(tuple(sorted(e.items())) for e in entries)))

        for e in entries:
            sb += f'{e["value"]} = {e["current_value"]} '

        return sb

    def get_variables(self) -> list[Entry]:
        return list(filter(lambda e: e.entry_type == EEntryType.VAR, self.entry_list))

    def set_values_to_variables(self, name: str, value: int) -> None:
        variables = list(filter(lambda v: v.value == name, self.get_variables()))

        for v in variables:
            v.current_value = value

    def enter_variable_values(self):
        try:
            print('Введите значений переменных:')

            variables = set(map(lambda v: v.value, self.get_variables()))

            for variable in variables:
                print(f'{variable} =', end=' ')
                value = int(input())

                self.set_values_to_variables(variable, value)
        except Exception as err:
            print(err)
