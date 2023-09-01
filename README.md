# 74xx Series Checker
汎用ロジックIC（以降74シリーズ）の刻印が見えづらくて、どの74シリーズか判別がつかなくなることがある。  
場合によっては、配線ミスや足の欠落などにより動作しない場合もある。  
（※コレはこれで、動作不良部位を見出す訓練にもなるが、初期ではシナリオ通りの動作であった方が良い）  
それらのトラブルを回避し、刻印を読むことを目的とせず、実習を通じて論理的思考に意識を寄せたい。  

そこで、74シリーズの判定と稼働状態を表示するガジェットを作製した。  
正しくは、以前ArduinoMicroPro(以下動作時の様子動画)で作成していた。  
しかし、Arduino系は、コスト高・ソースコードの管理がメンドい（こういうところで管理すればいいだけだが、作った勢いで満足してしまう悪いクセがある）ため、**RP2040**系に移植することにした。  
また、今回使用したマイコンの端子は、**USB Type-C**であることから、将来的なケーブル問題の懸念も解消しやすいと思う。


過去に作成したArduino版であるが、動作している動画を示しておく。

https://github.com/T-zakisan/74xx_Series_Cheker/assets/43605763/89aa2501-7571-49c8-97e4-ecc775599b73





## 判定に対応しているロジックIC
ここで対応する74シリーズは、以下とものとしている。  
また、14ピンに限る。
| 型番 | ロジック名 |
|:----:|----|
| 7400 | NAND |
| 7402 | NOR |
| 7404 | NOT |
| 7408 | AND |
| 7432 | OR |
| 7486 | Ex-OR |


## 表示の意味
液晶ディスプレイに以下の内容を表示する
1. 型番下２桁（74xx）
2. ロジック名
3. 稼働しているビット
   - **12x4__** : 数字→稼働ビット　/　x→不良ビット　/　_→隙間埋め
   - **/n** : ＩＣ内のビット数（分母）

# 作成方法

## パーツリスト
| パーツ名 | 備考 |
|:----|:----|
| [RP2040マイコンボードキット](https://akizukidenshi.com/catalog/g/gK-17542/) | [CirCuitPythonのファームウェアを書き込むこと](https://circuitpython.org/board/raspberry_pi_pico/) |
| [ゼロプレッシャーＩＣソケット 14P](https://akizukidenshi.com/catalog/g/gP-12073/) ||
| [Ｉ２Ｃ接続小型ＬＣＤモジュール（8×2行）ピッチ変換キット](https://akizukidenshi.com/catalog/g/gK-06795/) ||
| [角型ランド両面スルーホールガラスコンポジット・ユニバーサル基板 Cタイプ(72×47mm)](https://akizukidenshi.com/catalog/g/gP-09747/) ||
| [ネジ　M3xN20mm]() | 4 |
| [ナット　M3]() | 4 |
| [ネジ　M2x10mm]() | 2 |
| [ナット　M2]() | 2 |



## アサイン
配線の取り回しの関係からGPIOでGNDやVccを取得している

| マイコン端子 | パーツ端子 | 備考|
|:----:|:----|:----|
| 0 | LCD (Vcc) |  |
| 1 | LCD (GND) |  |
| 2 | 74シリーズ (4) | In / Output |
| 3 | 74シリーズ (1) | In / Output |
| 4 | 74シリーズ (2) | In / Output |
| 5 | 74シリーズ (3) | In / Output |
| 6 | 74シリーズ (14) | Vcc |
| 7 | 74シリーズ (13) | In / Output |
| 8 | 74シリーズ (12) | In / Output |
| 9 | 74シリーズ (11) | In / Output |
| 10 | 74シリーズ (10) | In / Output |
| 11 | 74シリーズ (9) | In / Output |
| 12 | 74シリーズ (8) | In / Output |
| 13 | 74シリーズ (5) | In / Output |
| 14 | 74シリーズ (6) | In / Output |
| 15 | 74シリーズ (7) | GND |
| 26 | LCD (SDA) |  |
| 27 | LCD (SCL) |  |


## 必須ライブラリ
| ライブラリ名 | 備考|
|:----|:----|
| st7032i.py | [LCDで使用](https://gist.github.com/boochow/6ffd0c939abbcc1a9c62bf6ab6b60cef#file-st7032i-py) |



## プログラム
上記の **code.py** をマイコンに保存



# 使用方法
1. ＩＣソケットのバーを上げる
2. ＩＣソケットに７４シリーズを装着
   - ＩＣソケットのバーがある方が**ロジックＩＣの欠け**がある向きにすること！
3. ボタンを押す　　以上




