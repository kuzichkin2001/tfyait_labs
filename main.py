from first_laba.lexical_analyze import Lexics
from second_laba.syntax_analyzer import SyntaxAnalyzer
from third_laba.entry_type import EEntryType
from fourth_laba.interpreter import Interpreter


def main():
    lexics_analyzer = Lexics(filepath='./first_laba/code.pasha')
    result = lexics_analyzer.start()
    lexemes = lexics_analyzer.lexemes

    for lexeme in lexemes:
        print(lexeme)

    syntax_analyzer = SyntaxAnalyzer(lexemes)

    ok, response = syntax_analyzer.start()
    if ok:
        for entry in response:
            if entry.entry_type == EEntryType.VAR or entry.entry_type == EEntryType.CONST:
                print(entry.value, end=' ')
            elif entry.entry_type == EEntryType.CMD:
                print(entry.cmd.name, end=' ')
            elif entry.entry_type == EEntryType.CMD_PTR:
                print(entry.cmd_ptr, end=' ')

        print("""
Interpretation.
--------------------------------------


        """)

        interpreter = Interpreter(syntax_result=ok, syntax_response=response)

        interpreter.start()
    else:
        print('Синтаксический анализ завершен с ошибками: ', syntax_analyzer.errors)


if __name__ == '__main__':
    main()