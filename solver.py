import morse
import recog_windows as rcg

if __name__ == '__main__':

    morse_sequence = rcg.import_figures('images')

    print("====窓の開閉====")
    print(morse_sequence)

    mrs = morse.Morse()
    encoded = mrs.decode(morse_sequence)
    print("===key===")
    print(encoded)
