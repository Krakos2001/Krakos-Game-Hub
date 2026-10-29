from msvcrt import getwch

AZERTY_ROW = ["&", "é", '"', "'", "(", "-", "è", "_", "ç", "à"]   # keys 1 to 9, then 0
WIDTH = 49
RESET = "\033[0m"
NORMAL = "\033[48;2;58;58;60m\033[1;97m"                 # dark gray, white bold text
HIGHLIGHT = "\033[48;2;200;200;200m\033[1m\033[38;2;30;30;30m"  # light gray, dark bold text

def print_row(text, color=NORMAL):
    print(f"{color}{text:<{WIDTH}}{RESET}")

def draw_menu(title, options, selected, subtitle="Available Games :"):
    print_row(title)
    print_row(subtitle)
    last = len(options) - 1
    for i, option in enumerate(options):
        if i == last:
            print_row("")                  # empty row before QUIT
            label = f"0. {option}"
        else:
            label = f"{i + 1}. {option}"
        color = HIGHLIGHT if i == selected else NORMAL
        print_row(label, color)
    print_row("-" * WIDTH)

def read_key():
    key = getwch()
    if key in ("\x00", "\xe0"):          # arrow/function key: read its second character
        second = getwch()
        if second == "H":
            return "UP"
        if second == "P":
            return "DOWN"
        return ""                        # other special keys are ignored
    if key in AZERTY_ROW:
        return str((AZERTY_ROW.index(key) + 1) % 10)
    return key

def run_menu(title, options, subtitle=None, selected=0):

    print("\033[2J\033[H", end="", flush=True) 
    draw_menu(title, options, selected, subtitle)

    menu_height = len(options) + 4

    while True:
        previous = selected
        key = read_key()

        if key == "UP":
            selected = (selected - 1) % len(options)
        elif key == "DOWN":
            selected = (selected + 1) % len(options)
        elif key == "\r":                       # Enter (next step)
            if selected == len(options) - 1:
                return None
            else:
                return selected
            
        elif key == "\x03" or key == "\x1b":    # Ctrl+C or Esc
            return
        elif key.isascii() and key.isdecimal():
            value = int(key)
            if value == 0:
                selected = len(options) - 1     # 0 = QUIT, the last row
            elif value <= len(options) - 1:
                selected = value - 1

        if selected != previous:
            print(f"\033[{menu_height}A", end="", flush=True)
            draw_menu(title, options, selected, subtitle)