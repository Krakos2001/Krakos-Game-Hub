from msvcrt import getwch

def draw_row(letters):
    tiles = ""
    for i in range(5):
        if i < len(letters):
            tiles += f"\033[48;2;86;87;88m\033[1;97m {letters[i].upper()} \033[0m"
        else:
            tiles += "\033[48;2;40;40;42m   \033[0m"
    print("\r" + tiles, end="", flush=True)

def read_word():
    letters = []
    message_shown = False
    draw_row(letters)
    while True:
        key = getwch()

        # clear the error message from the line below, if there is one
        if message_shown:
            print("\033[B\033[2K\033[A", end="", flush=True)
            message_shown = False

        if key == "\x03":                      # Ctrl+C
            raise KeyboardInterrupt
        elif key in ("\x00", "\xe0"):          # arrow/function key: skip its 2nd character
            getwch()
        elif key == "\x08":                    # Backspace
            if letters:
                letters.pop()
        elif key == "\r":                      # Enter (step D)
            if len(letters) == 5:
                word = "".join(letters)
                if is_valid(word):
                    return word
                print("\n\033[2KNot in word list", end="")
                print("\033[A", end="", flush=True)
                message_shown = True
        elif key.isascii() and key.isalpha():  # a letter
            if len(letters) < 5:
                letters.append(key.lower())

        draw_row(letters)