import argparse
import subprocess


class TerminalUtils:

    @staticmethod
    def createTerminalArgs(
            args: list[str],
            types: list | str = str,
            helpInfo: list = None,
            isRequired: list[bool] = False,
            defaultValue: list = None,
            consts: list = None, description='GetTerminalArgs'
    ):
        """ create terminal args """
        parser = argparse.ArgumentParser(description=description)
        length = len(args)
        __args = args
        _args = [arg[:1] for arg in __args]
        types = types if type(types) is list else [str] * length
        helpInfo = helpInfo if helpInfo is not None else [None] * length
        defaultValue = defaultValue if defaultValue is not None else [None] * length
        isRequired = isRequired if isRequired else [False] * length
        consts = consts if consts is not None else [None] * length
        for _, __, tp, info, value, required, const in zip(_args, __args, types, helpInfo,
                                                           defaultValue, isRequired, consts):
            if tp is list:
                parser.add_argument(f'-{_}', f'--{__}', nargs='+',
                                    help=info, default=value, required=required)
            elif const is not None:
                parser.add_argument(f'-{_}', f'--{__}', nargs='?',
                                    const=const, help=info, default=value, required=required)
            else:
                parser.add_argument(f'-{_}', f'--{__}', help=info,
                                    default=value, required=required)
        return parser.parse_args()

    @staticmethod
    def runTerminalCommand(element, asynchronous=False):
        """ run terminal command """
        if asynchronous:
            processes = []
            proc = subprocess.Popen(element)
            processes.append(proc)
            for proc in processes:
                proc.wait()
        else:
            return subprocess.run(element)
