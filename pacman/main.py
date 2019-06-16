import os
import sys
import curses

def get_pacman_infos(key, pos_x, pos_y, matriz):
    pacman = ""
    pacman_right = lambda x: "ᗧ" if x % 2 == 0 else "⚇"
    pacman_left = lambda x: "ᗤ" if x % 2 == 0 else "⚇"
    pacman_down = lambda x: "ᗣ" if x % 2 == 0 else "⚇"
    pacman_up = lambda x: "ᗢ" if x % 2 == 0 else "⚇"

    if key == "s":
        pos_y += 1
        pacman = pacman_down(pos_y)
    elif key == "w":
        pos_y -= 1
        pacman = pacman_up(pos_y)
    if key == "d":
        pos_x += 1
        pacman = pacman_right(pos_x)
    elif key == "a":
        pos_x -= 1
        pacman = pacman_left(pos_x)

    # restrictions/fixbugs
    if pos_y >= len(matriz):
        pos_y = len(matriz) - 1

    if pos_y <= 0:
        pos_y = 0

    if pos_x >= len(matriz[pos_y]):
        pos_x = len(matriz[pos_y]) - 1    
    
    if pos_x <= 0:
        pos_x = 0

    return pos_x, pos_y, pacman


def draw_pacman(pacman, pos_x, pos_y, matriz):
    poop = "-"
    # draw pacman in line
    _line = list(matriz[pos_y])
    _line[pos_x] = pacman
    matriz[pos_y] = ''.join(_line)
    
    aux = "\n".join(matriz)

    # change pacman for poop
    _line = list(matriz[pos_y])
    _line[pos_x] = poop

    matriz[pos_y] = ''.join(_line)

    return matriz, aux


def main(win):
    pos_x = 0
    pos_y = 0

    def wellcome_tips():
        win.addstr("Wellcome to simple PACMAN simulator\n")
        win.addstr('"a" - left\n"d" - right\n')
        win.addstr('"w" - up\n"s" - down\n')
        win.addstr("CTRL+C - quit\n\n")


    win.nodelay(True)
    key = ""
    win.clear()
    wellcome_tips()
    win.addstr("Press any key to start\n\n")
    matriz = TEXT
    while 1:
        try:
            key = win.getkey()
            if not key in "asdw":
                continue

            win.clear()

            pos_x, pos_y, pacman = get_pacman_infos(key, pos_x, pos_y, matriz)
            
            # show tips message every on the top
            wellcome_tips()
            
            matriz, aux = draw_pacman(pacman, pos_x, pos_y, matriz)
            win.addstr(aux+'\n')
                
        except curses.error:
            # No input
            pass
        except KeyboardInterrupt:
            sys.exit()


def normalize_text(text: list):
    # clear breaklines in array of linetexts
    text = [i.replace('\n', '') for i in text]
    max_line_length = max([len(i) for i in text])
    for index, value in enumerate(text):
        _len = len(value)
        if _len < max_line_length:
            text[index] += " " * int(max_line_length - _len)  
    return text


if __name__ == '__main__':
    line = "+++++++++++++++++"
    text_default = [line for _ in range(5)]
    try:
        path = sys.argv[1]
        if not os.path.isfile(path):
            print("File not found")
            sys.exit()

        with open(path, 'r') as _file:
            TEXT = normalize_text(_file.readlines())
            
    except IndexError:
        TEXT = text_default
    curses.initscr()
    curses.start_color()
    curses.wrapper(main)
