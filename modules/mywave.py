import wave
import pyaudio
import struct
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


    def __del__(self):
        self.__wf.close()


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


class WaveWriter:
    """ WAVE 書き込みに利用するクラス。 """
    def __init__(self, path):
        """ WAVE ファイルの書き込み準備を行います。
        Parameters:
            path -- WAVE のパス。
        """
        self.__wf = wave.open(path, mode='wb')
        self.setWaveInfo()


    def __del__(self):
        self.__wf.close()


    def setWaveInfo(self, *, nchannels=1, sampwidth=2, rate=44100):
        """ WAVE ファイルの情報を設定します。
        Parameters:
            nchannels -- チャンネル数（デフォルト: 1）。
            sampwidth -- 量子化バイト数（デフォルト: 2）。
            rate -- サンプリング周波数（デフォルト: 44100）。
        """
        self.__wf.setnchannels(nchannels)
        self.__wf.setsampwidth(sampwidth)
        self.__wf.setframerate(rate)


    def save(self, wave):
        """ WAVE ファイルを書き込みます。
        Parameters:
            wave -- [-1, 1]の数値リスト。
        """
        mx = 2 ** (self.__wf.getsampwidth() * 8) // 2 - 1
        filt = np.vectorize(lambda x: min(mx, max(-mx, x)))
        data = filt(mx * wave)

        if self.__wf.getsampwidth() == 2:
            data = data.astype(np.int16)
            binary = struct.pack('h' * len(data), *data)

        self.__wf.writeframes(binary)
