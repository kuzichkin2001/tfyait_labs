from authomato.dfa import DFA
from authomato.nfa import NFA


def main():
    # d = DFA(is_file=True, path='dfa.txt')
    # if d.accept('aaabcc'):
    #     print('Цепочка распознана')
    # else:
    #     print('Цепочка не распознана')
    #
    # d.show_data()

    n = NFA(is_file=True, path='nfa.txt')
    n.show_data()

    print('-' * 30)

    n = n.removeEpsilonTransitions()
    n.show_data()

    print('-' * 30)

    n = n.getDFA()
    n.show_data()
    # if n.accept('bbaa'):
    #     print('Цепочка распознана')
    # else:
    #     print('Цепочка не распознана')

    # n = NFA(is_file=True, path='nfa.txt')
    # n.show_data()
    #
    # print('-' * 30)
    #
    # n_without_eps = n.removeEpsilonTransitions()
    # n_without_eps.show_data()
    #
    # new_d = n_without_eps.getDFA()
    # new_d.show_data()




if __name__ == '__main__':
    main()
