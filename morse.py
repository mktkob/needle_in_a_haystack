class Morse:
    def __init__(self):
        self.digit_dict = self.make_digit_dict()
        self.swp_digit_dict = self.make_swap_digit_dict(self.digit_dict)

    def make_digit_dict(self):
        normal_dict = {'A': 'sl', 'B': 'lsss', 'C': 'lsls', 'D': 'lss',
                       'E': 's', 'F': 'ssls', 'G': 'lls', 'H': 'ssss',
                       'I': 'ss', 'J': 'slll', 'K': 'lsl', 'L': 'slss',
                       'M': 'll', 'N': 'ls', 'O': 'lll', 'P': 'slls',
                       'Q': 'llsl', 'R': 'sls', 'S': 'sss', 'T': 'l',
                       'U': 'ssl', 'V': 'sssl', 'W': 'sll', 'X': 'lssl',
                       'Y': 'lsll', 'Z': 'llss', '1': 'sllll', '2': 'sslll',
                       '3': 'sssll', '4': 'ssssl', '5': 'sssss', '6': 'lssss',
                       '7': 'llsss', '8': 'lllss', '9': 'lllls', '10': 'lllll',
                       '.': 'slslsl', ',': 'llssll', '?': 'ssllss',
                       '!': 'lslsll', '-': 'lssssl', '/': 'lssls',
                       '@': 'sllsls', '(': 'lslls', ')': 'lsllsl'}

        def ls_to_digit(ls_value):
            digit_value = ''
            for letter in ls_value:
                if letter == 's':
                    digit_value = digit_value + '10'
                elif letter == 'l':
                    digit_value = digit_value + '1110'
            return digit_value
        for key in normal_dict:
            normal_dict[key] = ls_to_digit(normal_dict[key])
        return normal_dict

    def make_swap_digit_dict(self, d):
        return {v: k for k, v in d.items()}

    def encode(self, word):
        word = word.upper()
        morse = ''
        for letter in word:
            morse = morse + self.digit_dict[letter] + '00'
        return morse

    def decode(self, morse_digits):
        morse_digits = morse_digits.strip("0")
        morse_digits = morse_digits.split("000")
        word = ''
        for digit in morse_digits:
            digit = digit + '0'
            if digit in self.swp_digit_dict:
                word = word + self.swp_digit_dict[digit]
            else:
                word = word + '"'
                word = word + digit
                word = word + '"'
        return word


if __name__ == '__main__':
    morse = Morse()
    osaka_morse = morse.encode('osaka')
    print(osaka_morse)
    print(morse.decode(osaka_morse))
