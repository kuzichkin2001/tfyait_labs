from first_laba.lexical_analyze import Lexics
from second_laba.syntax_analyzer import SyntaxAnalyzer


def main():
    lexics_analyzer = Lexics(filepath='./first_laba/code.pasha')
    result = lexics_analyzer.start()
    lexemes = lexics_analyzer.lexemes

    for lexeme in lexemes:
        print(lexeme)

    syntax_analyzer = SyntaxAnalyzer(lexemes)

    if syntax_analyzer.start():
        print('Синтаксический анализ прошел успешно, ошибок не найдено.')
    else:
        print('Синтаксический анализ завершен с ошибками: ', syntax_analyzer.errors)


if __name__ == '__main__':
    main()