from typing import Any, Callable

from fsgenlib.colored_output import Color


class UserInteraction:
    @staticmethod
    def ask(_prompt: str, check_func: Callable[[str], bool], reason: str = "Invaild respdonse", convert_func: Callable[[str], Any] = str) -> Any:
        while(1):
            _input = input(_prompt + ": ")
            if check_func(_input):
                return convert_func(_input)
            else:
                print(reason)

    def print_err(_msg: str, exit: bool) -> None:
        print(Color.red("[err]") + " {}\n".format(_msg))
        if exit: raise SystemExit("Aborted")

    def print_warn(_msg: str) -> None:
        print(Color.yellow("[warn]") + " {}".format(_msg))