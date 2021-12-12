import colorama

colorama.init()

class Color:
    @staticmethod
    def red(_msg: str) -> str:
        return "{}{}{}".format(colorama.Fore.RED, _msg, colorama.Fore.RESET)
    
    @staticmethod
    def yellow(_msg: str) -> str:
        return "{}{}{}".format(colorama.Fore.YELLOW, _msg, colorama.Fore.RESET)

    @staticmethod
    def green(_msg: str) -> str:
        return "{}{}{}".format(colorama.Fore.GREEN, _msg, colorama.Fore.RESET)
    
    @staticmethod
    def cyan(_msg: str) -> str:
        return "{}{}{}".format(colorama.Fore.CYAN, _msg, colorama.Fore.RESET)