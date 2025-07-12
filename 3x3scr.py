from random import choice, randint
from typing import List
from os import system as sys


def randbool() -> bool:
    return bool(randint(0, 1))


class MainMenu:
    def __init__(self, min_moves=16, max_moves=32, n_columns=6):
        self.min_moves: int = min_moves
        self.max_moves: int = max_moves
        self.n_columns = n_columns
        self.commands: dict[str: callable] = {'M': self.__set_minmax__,
                                              '#': self.__set_n_columns__,
                                              'S': self.scramble,
                                              'E': self.__ex__}
        self.OPTIONS: str = ('>[S]cramble\n'
                             '>Edit [M]in/max\n'
                             '>Edit [#] of columns\n'
                             '>[E]xit\n')

    def __set_n_columns__(self) -> int:
        print("Modifying number of columns per row (resets after restart).")
        new_n_cols = input('NCOLS = ')

        if not new_n_cols.isdecimal():
            return 95

        self.n_columns = int(new_n_cols)
        sys('cls')
        return 0

    def __set_minmax__(self) -> int:
        print("Modifying minimums and maximums (resets after restart).\n")
        new_min = input('MIN = ')
        new_max = input('MAX = ')
        parse: List[bool] = [new_min.isdecimal(), new_max.isdecimal()]

        if not all(parse):
            return 95

        self.min_moves = int(new_min)
        self.max_moves = int(new_max)
        sys('cls')
        return 0

    def display_options(self) -> str:
        return self.OPTIONS

    @staticmethod
    def __ex__() -> int:
        return 100

    @staticmethod
    def pretty_print(parsed_list, n_columns) -> int:
        for i, v in enumerate(parsed_list):
            end_of_row: bool = (i + 1) % n_columns == 0

            if not end_of_row:
                print(str(v), end=' - ')
            else:
                print(v)
        print('\n')

        return 0

    def parse_command(self, command) -> int:
        sys('cls')
        command = command.upper()
        if command not in self.commands:
            return 95

        parsed = self.commands[command]()

        if type(parsed) == list:
            parsed = self.pretty_print(parsed, self.n_columns)

        return parsed

    def scramble(self) -> List[str]:
        moves: int = randint(self.min_moves, self.max_moves)
        sides: List[str] = ["U", "D", "L", "R", "F", "B"]
        concatenate: List[str] = []
        modifiers: dict[str: bool] = {"'": bool, '2': bool}

        for move in range(moves):
            concatenate_temp: List[str] = []
            modifiers = {mod: randbool() for mod in modifiers}

            concatenate_temp.append(str(choice(sides)))

            for mod in modifiers:
                if modifiers[mod]:
                    concatenate_temp.append(mod)
                else:
                    continue

            concatenate.append(''.join(concatenate_temp))

        del concatenate_temp

        return concatenate


def main() -> None:
    main_menu_obj = MainMenu()
    ERROR_LUT: dict[int: str] = {418: 'CUSTOM_ERROR_DEBUG',
                                 100: 'CUSTOM_EXIT',
                                 95: 'CUSTOM_ERROR_INVALIDTX'}
    custom_error_code: int = 0
    user_input: str

    while custom_error_code != 100:
        user_input = str(input(main_menu_obj.display_options()))
        custom_error_code = main_menu_obj.parse_command(user_input)

        if custom_error_code != 0:
            sys('cls')
            print(str(ERROR_LUT[custom_error_code] + ' - Enter to dismiss\n'))


if __name__ == '__main__':
    main()
