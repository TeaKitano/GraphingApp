# GraphingApp
関数のグラフ描画とCSVからのプロット描画に対応した、グラフ描画ソフトウェアです。

 
 
# Features
 
CSVファイルは以下の形式で、全て数値である必要があります。それ以外の行は無視されます。</br>
x1,y1</br>
x2,y2</br>
  ...</br>
  ...</br>
 
関数で使える文字はxのみです。その他関数として、exp(),cos(),sin(),tan(),log()などが使えます。</br>
描画範囲は空欄の場合xy共に-10～10の範囲に設定されます。
 
# Requirement
python 3.11.0</br>
PySimpleGUI 4.60.4</br>
matplotlib 3.6.1</br>
sympy 1.11.1</br>

※pyhton3.9環境でも動くことを確認しています。
 
# Installation
```bash
pip install PySimpleGUI
pip install matplotlib
pip install sympy
```
 
# Usage
CSVの場合はCSV追加のボタンを、関数を追加する場合は関数追加のボタンを押してください。</br>
描画設定の変更を適用したい場合には更新ボタンを押してください。</br>
クリアボタンは全てのデータを消します。復元できませんので気を付けてください。</br>
画像を保存したい場合には、保存ボタンの右のテキストボックスにファイル名を指定してください。</br>

 

# Author

* Tea Kitano
* E-mail chacha_musics@yahoo.co.jp
* twitter https://twitter.com/ChachaLepracaun
 
# License
このソフトウェアは[LGPL](https://www.gnu.org/licenses/lgpl-3.0.html)に基づいています。
