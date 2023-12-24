import datetime

from termcolor import colored
from termcolor._types import Color

colors: dict[str, Color] = {
    'LOG': 'green',
    'WRN': 'yellow',
    'ERR': 'red',
}


def indent_lines(lines, indent, indent_first=0):
    return [
        ' ' * (indent_first if i == 0 else indent) + line
        for i, line in enumerate(lines)
    ]


def log(*args: str, level='LOG', indent=False):
    if level not in colors:
        level = 'LOG'
    date_str = datetime.datetime.now().strftime('%m/%d %H:%M:%S')

    prefix = colored(date_str, 'grey', attrs=['bold']) + ' '
    prefix += colored(level.ljust(5), colors[level])

    length = len(date_str) + 1 + 5

    if indent:
        length += 2

    print(prefix + '\n'.join(indent_lines(args, indent=length, indent_first=0)))


def lprint(*args):
    log(*args)


def eprint(*args):
    log(*args, level='ERR')


def wprint(*args):
    log(*args, level='WRN')


# def lprint(*args):
#     segments = [
#         datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#         ' ',
#         colored('LOG', 'green'),
#         ' ' * 6,
#     ]

#     prefix = colored(segments[0], 'grey', attrs=['bold'])
#     prefix += segments[1]
#     prefix += colored('LOG', 'green')
#     prefix += segments[3]

#     indent = len(re.findall(r'\w|-|:', prefix))

#     # print(prefix + '\n'.join(indent_lines(args, indent=indent)))
#     print(prefix.encode())


# def eprint(*args):
#     segments = [
#         datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#         ' ',
#         'ERROR',
#         ' ' * 4,
#     ]

#     prefix = colored(segments[0], 'grey', attrs=['bold'])
#     prefix += segments[1]
#     prefix += colored('LOG', 'green')
#     prefix += segments[3]
#     prefix = f"{colored(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'grey', attrs=['bold'])} {colored('ERROR', 'red')}    "
#     indent = len(list(filter(lambda c: c.isprintable(),  prefix)))
#     print(prefix + '\n'.join(indent_lines(args, indent=indent)))
