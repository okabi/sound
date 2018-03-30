import wave
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from player import Player


class WaveReader:
    """ WAVE を読み込んで扱うクラス。 """
    def __init__(self, path):
        """ WAVE ファイルを読み込みます。
        Parameters:
            path -- WAVE のパス。
        """
        self.__wf = wave.open(path, mode='rb')


    def printWaveInfo(self):
        """ WAVE ファイルの情報を表示します。 """
        print('チャンネル数: {:}'.format(self.__wf.getnchannels()))
        print('サンプル幅: {:}'.format(self.__wf.getsampwidth()))
        print('サンプリング周波数: {:}'.format(self.__wf.getframerate()))
        print('フレーム数: {:}'.format(self.__wf.getnframes()))
        print('パラメータ: {:}'.format(self.__wf.getparams()))
        print('長さ（秒）: {:}'.format(self.__wf.getnframes() / self.__wf.getframerate()))


    def play(self):
        """ WAVE ファイルを再生します。 """
        player = Player(self.__wf.getsampwidth(),
                        self.__wf.getnchannels(),
                        self.__wf.getframerate(),
                        self.__wf.readframes)
        player.play()


    def display(self):
        """ WAVE ファイルの波形を表示します。 """
        # データの読み込み
        buffer = self.__wf.readframes(self.__wf.getnframes())

        # バイナリデータをバイトデータに変換
        width = self.__wf.getsampwidth()
        if width == 2:
            data = np.frombuffer(buffer, dtype='int16')

        # 波形表示（一部）
        plt.plot(data[:1000])
        plt.show()
