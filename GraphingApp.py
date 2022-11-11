import sympy
import math
from sympy import sympify
import numpy
import matplotlib.pyplot as plt
import japanize_matplotlib
import csv
import PySimpleGUI as sg
import io

#初期用
#これ消したら表示バグります
fig = plt.figure(figsize=(15,12))
ax = fig.add_subplot(111)

#ラベルのフォントサイズ
font_size=20

#ぼやけるのを防ぐ
def make_dpi_aware():
  import ctypes
  import platform
  if int(platform.release()) >= 8:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
make_dpi_aware()

#ファイルが存在するかチェック　開けてみてエラーならFalse、開いたら閉じてTrue返す
#file_name:チェックするファイル名
def checkfile(file_name):
    try:
        f=open(file_name)
    except OSError:
        return False
    else:
        f.close()
        return True

# 文字列をnumpyで扱える関数に変換
# 変換できない場合、Falseを返す
#
# input  s:関数を示す文字列
# output 成功時: numpyで扱える関数
#        失敗時: False
def ReadFunc(s):
    if s=="":
        return False
    l=["1","2","3","4","5","6","7","8","9","0"]
    k=s[0]
    for i in range(len(s)-1):
        if s[i+1]=="x":
            if s[i] in l:
                k=k+"*"
        k=k+s[i+1]
            
    x=sympy.Symbol('x')
    try:
        y=sympify(k)
    except:
        return False
    if type(y.subs(x,8).evalf())==type(sympy.sin(6).evalf()):
        args=(x)
        return sympy.lambdify(args,y,"numpy")
    else:
        return False

# 文字列から関数に変換した上でplot用のデータセットを生成
# 失敗した場合、Falseを返す
#
# input mn:プロット範囲の最小値
#       mx:プロット範囲の最大値
#       f:関数を示す文字列
#output 成功時:l[0]がx、l[1]がyのnumpyリストを格納しているリスト。
#       失敗時:False
def mkFuncPlot(f,mn,mx):
    x=sympy.Symbol("x")
    y=ReadFunc(f)
    if y==False:
        return False
    xl=numpy.linspace(mn,mx)
    yl=y(xl)
    return [xl,yl]

# 指定のcsvファイルからplot用データセットの作成
# 一列目をx、二列目をyとして読み込み
#
# input s:csvファイル名
# output l[0]がx、l[1]がyのnumpyリストを格納しているリスト。l[2]はcsvからのplotを示すため"c"
def mkCsvPlot(s):
    xl=[]
    yl=[]
    try:
        with open(s) as f:
            reader=csv.reader(f)

            for i in reader:
                if len(i)>=2:
                    xl.append(float(i[0]))
                    yl.append(float(i[1]))
            return [xl,yl,"c"]
    except:
        return []


# リストに格納された全てのデータセットを画像に出力
# 関数からのデータは折れ線・csvからのデータは散布図として表示
# 
# input ax:グラフの場所
#       l:データセットの入ったリスト
# output 無し
def AllPlot(ax,l,mn,mx):
    for i in l:
        if len(i)==1:
            f=mkFuncPlot(i[0],mn,mx)
            ax.plot(f[0],f[1])
        else:
            ax.scatter(i[0],i[1])
    fig_bytes=draw_plot_image(fig)
    return fig_bytes

#グラフを画像化
#
#input グラフ
#output 画像データ
def draw_plot_image(fig):
    item = io.BytesIO()
    plt.savefig(item, format='png')
    plt.clf()
    return item.getvalue()


def mkGUI():
    l=[]
    #メインのGUI設計
    layout=[[sg.Text("描画範囲"),sg.Text("  x最小値:"),sg.Input(size=(4,1)),sg.Text("  x最大値:"), sg.Input(size=(4,1)),sg.Text("  y最小値:"),
    [sg.Button("CSV追加",key="-csv-"),sg.Button("関数追加",key="-func-")],
    sg.Input(size=(4,1)),sg.Text("  y最大値:"), sg.Input(size=(4,1))],
    [sg.Text("ラベル   タイトル"),sg.Input(size=(10,1)),sg.Text("x軸"),sg.Input(size=(10,1)),sg.Text("y軸"),sg.Input(size=(10,1))],
    [sg.Image(key="-image-")],
    [sg.Button("更新",size=(15,1))],
    [sg.Button("ダウンロード",size=(15,1)),sg.Text("ファイル名:"),sg.Input(size=(20,1))],
    [sg.Button("クリア",size=(15,1))],
    [sg.Button("終了",size=(15,1))]
    ]

    window=sg.Window("GraphingApp",layout,finalize=True)
    
    while True:
        func=""
        event,values=window.read()

        try:#xの最小値・最大値が共にあれば採用
            xmin=int(values[0])
            xmax=int(values[1])
        except:#初期値
            xmin=-10
            xmax=10
        try:#xの最小値・最大値が共にあれば採用
            ymin=int(values[2])
            ymax=int(values[3])
        except:#初期値
            ymin=-10
            ymax=10
        if event==sg.WIN_CLOSED or event=="終了":
            break

        #グラフ初期化
        elif event=="クリア":
            l=[]
            fig_bytes=AllPlot(ax,l,xmin,xmax)
            window['-image-'].update(data=fig_bytes)

        #関数読み込み
        elif event=="-func-":
            fig = plt.figure(figsize=(15,12))
            ax = fig.add_subplot(111)
            ax.set_xlim([xmin,xmax])
            ax.set_ylim([ymin,ymax])
            ax.set_title(values[4],{'fontsize':font_size})
            ax.set_xlabel(values[5],{'fontsize':font_size})
            ax.set_ylabel(values[6],{'fontsize':font_size})

            #サブ画面 入力が関数変換できるかチェック
            func_window=sg.Window("関数入力",[[sg.Text("プロットしたい関数を入力してください")],[sg.Text("y="),sg.Input()],[sg.Button("挿入")]])

            while True:
                event,values=func_window.read()
                if event==sg.WIN_CLOSED or event=="キャンセル":
                    break
                elif event=="挿入":
                    if ReadFunc(str(values[0]))==False:
                        sg.popup("無効な文字列です。")
                    else:
                        func=str(values[0])
                    func_window.close()
                    break

            if func!="":
                l.append([func])
                fig_bytes=AllPlot(ax,l,xmin,xmax)
                window['-image-'].update(data=fig_bytes)

        #csv読み込み
        elif event=="-csv-":
            fig = plt.figure(figsize=(15,12))
            ax = fig.add_subplot(111)
            ax.set_xlim([xmin,xmax])
            ax.set_ylim([ymin,ymax])
            ax.set_title(values[4],{'fontsize':font_size})
            ax.set_xlabel(values[5],{'fontsize':font_size})
            ax.set_ylabel(values[6],{'fontsize':font_size})

            filename=""
            filename = sg.popup_get_file("描画するCSVファイルを入力してください",file_types=(("Text Files", ".csv"),))
            if str(filename)!="None":
                l.append(mkCsvPlot(filename))
                if l[-1]==[]:
                    l.remove([])
                fig_bytes=AllPlot(ax,l,xmin,xmax)
                window['-image-'].update(data=fig_bytes)

        #再描画 範囲の変更を想定
        elif event=="更新":
            fig = plt.figure(figsize=(15,12))
            ax = fig.add_subplot(111)
            ax.set_xlim([xmin,xmax])
            ax.set_ylim([ymin,ymax])
            ax.set_title(values[4],{'fontsize':font_size})
            ax.set_xlabel(values[5],{'fontsize':font_size})
            ax.set_ylabel(values[6],{'fontsize':font_size})

            fig_bytes=AllPlot(ax,l,xmin,xmax)
            window['-image-'].update(data=fig_bytes)
        
        #画像のダウンロード ファイル名無ければエラー
        elif event=="ダウンロード":
            if values[7]=="":
                sg.popup("ファイル名を入力してください。")
            else:
                if checkfile(values[7]+".png"):
                    sg.popup("同じ名前のファイルが存在します。ファイル名を変えてください。")
                else:
                    with open(values[7]+".png",mode="wb") as pic:
                        pic.write(fig_bytes)                    


    window.close()

if __name__=="__main__":
    mkGUI()