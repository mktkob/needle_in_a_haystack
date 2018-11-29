# Needle in a Haystack Write-up
これは大会の後，解いた記録である．

## 問題
https://www.youtube.com/watch?v=sTKP2btHSBQ
へのリンクが張られている．

## 解答の流れ
ホテルの窓がモールス信号になっているという事前知識をwrite-up等を見た友人から得ている．
https://twitter.com/9SQ/status/1056439457535025152?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E1056439457535025152&ref_url=https%3A%2F%2Fqiita.com%2Fdeko2369%2Fitems%2F85c98d71d13f5d6e95f9

動画の速度を変更しながら再生する．
60倍速で再生したときに，
最初のところで"... . -.-. (SEC)"と成っている窓があることに気づく．

短点と長点の長さを確認すると，短点1分，長点3分になっていることがわかる．
つまり，1分が最小単位になることがわかる(補足のモールス符号の項目参照)．

そこで，以下の方法でFLAGが獲得出来そう．
1. 動画を1分ごとの画像に分割
2. 画像から窓の開閉状況を1(開く)0(閉じる)で表す．
3. "10"のモールス符号を文字列に変化する．

1, 3, 2の順番で実装して解答に挑む．

## 1. 動画を1分ごとの画像に分割

```
$ ffmpeg -i needle_in_a_haystack.mp4 -vcodec png -vf fps=1/60 images/image_%10d.png
```
\* 後から考えるとOpenCVで，画像分割も実現できたかもしれない．

## 3. "10"のモールス符号を文字列に変化する．
窓の開閉はモールス符号のキーの打鍵状態を1，打鍵していない状態を0として表したている．
"10"のモールス符号, e.g., `11101110111000101010001011100011101011100010111000` を，モールス符号, e.g., `- - -, ..., .-, -.-, ,-`,として解釈して，
文字列`OSAKA` に変換できるようにする．

まず，文字に対する短点・長点を表した辞書`normal_dict`を手書きで作成．
`normal_dict`を，文字に対する"01"辞書に変換`digit_dict`して，さらに辞書を逆引きに変換`swp_digit_dict`する．

以下に，`normal_dict`を示す．
sは短点，lは長点を表す．
例えば，Aはモールス符号で`.-`の短点1つと長点1つの組み合せなので，`sl`と表す．

```
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
```

実際にデコードするときには，"01"から文字に変換できる辞書`swp_digit_dict`のkeyでマッチングを行って，文字をデコードする．
例外処理として，マッチングが取れなかった場合は，マッチングが取れなかった"01"部分をそのまま出力するようにした．
これにより，人間デコードが可能である．


以下にコードの全体を示す．

``` morse.py
class Morse:
    def __init__(self):
        self.digitdict = self.make_digitdict()
        self.swp_digitdict = self.make_swap_digit_dict(self.digitdict)

    def make_digitdict(self):
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
            morse = morse + self.digitdict[letter] + '00'
        return morse

    def decode(self, morse_digits):
        morse_digits = morse_digits.strip("0")
        morse_digits = morse_digits.split("000")
        word = ''
        for digit in morse_digits:
            digit = digit + '0'
            if digit in self.swp_digitdict:
                word = word + self.swp_digitdict[digit]
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
```

## 2. 画像から窓の開閉状況を1(開く)0(閉じる)で表す
画像から窓の状況を判定するために，以下の操作を行う．
1. 画像を切り出して窓周辺画像を作成
2. 窓周辺画像から窓の開閉を判定

まず，画像を切り出す方補を示す．
Gimp等で，1分ごとの画像を確認すると，585-595, 1135-1150の画素の部分に窓があることがわかる．
そこで，OpenCVを用いて画像を読み出して，その配列中の当該画素だけに切り出す．

```
im = cv2.imread(file_name, 0)
dst = im[585:595, 1135:1150]
```

切り出した画像をpythonコード内で処理するため，
切り出した画像を保存する必要はない．
ただ，人間が動作を確認するため，以下の様に保存する．

```
cv2.imwrite('converted/' + file_name[7:], dst)
```

次に，窓周辺画像から窓の開閉状況を判別する．
窓が開いているときに，窓の中の明るさと周囲の明るさに差が大きくなることを利用する．
例えば，夜窓があいていると，窓の周囲に比べて窓の中が明るくなる．
具体的判別方法として，窓周辺画像内の最も明るい画素と最も暗い画素の明るさの違い(`np.max(dst) - np.min(dst)`)によって窓の開閉状況を判別する．

動画全体を通して一貫した閾値を設けて，判別する事ができれば簡単である．
しかしながら，本動画において夜・明け方・昼と3つの時間帯によって(`np.max(dst) - np.min(dst)`)の取る値の傾向が大きく異なる事が分かった．
そこで，閾値の異なる3つの判別関数，`binarize`, `binarize_dawn`, `binarize_daylight`を定義した．

以下に画像から窓の開閉状況を取得するpythonコード全体を示す．

``` recog_windows.py
import numpy as np
import glob
import cv2


def binarize(dst):
    if np.max(dst) - np.min(dst) > 80:
        return '1'
    else:
        return '0'


def binarize_dawn(dst):
    if np.max(dst) - np.min(dst) > 30:
        return '1'
    else:
        return '0'


def binarize_daylight(dst):
    if np.max(dst) - np.min(dst) > 90:
        return '1'
    else:
        return '0'


def import_figures(directory_name):
    file_list = sorted(glob.glob(directory_name + '/*.png'))
    morse_sequence = ''
    for file_name in file_list:
        im = cv2.imread(file_name, 0)
        dst = im[585:595, 1135:1150]
        if int(file_name[20:23]) < 400:
            degitized_sequence = binarize(dst)
        elif int(file_name[20:23]) < 427:
            degitized_sequence = binarize_dawn(dst)
        else:
            degitized_sequence = binarize_daylight(dst)
        morse_sequence = morse_sequence + degitized_sequence
        # print(file_name[20:])
        cv2.imwrite('converted/' + file_name[7:], dst)
        # For confirming the window recognition
    return morse_sequence
```

### 実行結果
以下のソルバーを実行する．

``` solver.py
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
```

以下に実行結果を示す．

```
Ubu18Vagrant575%python3 solver.py 
====窓の開閉====
0101010001000111010111010001110101110100011101110111000111010001110101110111010001010
1000111011101110001110111000100011100010100011101110001000101010001110101010101110001
0111000111010101010111000101010001000111010111010001011101000100011100011101010101011
1000111011100010001010100010101000101110001110111010001000111010101010111000111010101
0001011101000111011101110001011100011101010001110101110100010111000101010000110001010
1000111010101010111000111010101000111011101110001011101010001110101000101110101000111
01011101110001110101110111010111000
===key===
SECCON(SOMETIMES-A-SECRET-MESSAGE-BROADCAS"0110"S-BOLDLY)
```

残念ながら，
実行した結果，FLAGとして`SECCON(SOMETIMES-A-SECRET-MESSAGE-BROADCAS"0110"S-BOLDLY)`を取得した．
途中の`0110`の部分が窓開閉が判別できず復号できなかった．
短点または長点一つのEまたはTであると考えられる．
文意からTだろうと考えられる．

以上からFLAGは，
`SECCON(SOMETIMES-A-SECRET-MESSAGE-BROADCASTS-BOLDLY)`
である．(多分)


## 感想
+ モールス符号の電信になれていたら，動画を早送りで見るだけで脳内で復号できそう．
+ 窓の開閉状況を識別する方法として，OpenCVを利用したさらによい手法があると思う．
    + ただ，今回の窓判別手法で判別出来なかった箇所は目視でもよく分からなかった．


## 補足
### モールス符号
モールス符号の長さの比は，
+ 短点1
+ 長点3
+ 各点の間1
+ 文字館のスペースは3
+ 語と語の間は7
と決まっている．

アマチュア無線モールス符号試験を突破する為の豆知識:
以下の2分木と，CQだけ覚える．
選択式なので大体正解できる．
私はこの方法で3アマのモールス符号問題を完答しました．
2011年以降，1アマすら電気通信術の実技試験がないので，多分この方法で1アマのモールスも解けると思います．

短点と長点の2分木: 左が短点，右が長点．(例えばRは.-.)

```
E       T
I   A   N   M
S U R W D K G O
```

C: -.-.
Q: --.-

https://ja.wikipedia.org/wiki/モールス符号

### ffmpeg 使い方
+ https://qiita.com/livlea/items/a94df4667c0eb37d859f
+ https://qiita.com/ymotongpoo/items/eb9754b75606be117b70
+ http://tech.ckme.co.jp/ffmpeg_movtopics.shtml
### OpenCV
+ https://qiita.com/yori1029/items/a0ddd25c9571b28f3e1c

### 他の方のwrite-up
+ https://0xiso.hatenablog.com/entry/2018/10/28/222234
+ https://ctf-writeups.ru/2k18/seccon-2018-online-ctf/needle_in_a_haystack/
+ https://w0y.at/writeup/2018/10/27/seccon-2018-quals-needle-in-a-haystack.html
+ https://qiita.com/deko2369/items/85c98d71d13f5d6e95f9
