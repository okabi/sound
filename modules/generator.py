import struct
import numpy as np

class Generator:
    """ パラメータを用いて音声データを生成するクラスです。 """
    def __init__(self, fs, nbit=16):
        """ 音声データ生成器を初期化します。
        Parameters:
            fs -- サンプリング周波数。
            nbit -- 量子化ビット数。
        """
        self.fs = fs
        self.nbit = nbit
        self.__data = None
        self.__pos = 0


    def getData(self):
        """ 作成した音声データを取得します。
        Returns:
            作成した音声データ（整数列）。
        """
        if self.nbit == 16:
            return np.frombuffer(self.__data, dtype='int16')


    def createSineWave(self, A, f0, length):
        """ 正弦波を作成します。
        Parameters:
            A -- 振幅。
            f0 -- 基本周波数。
            length -- 長さ（秒）。
        """
        wave = A * np.sin(2 * np.pi * f0 * np.arange(self.fs * length) / self.fs)
        self.__create_wave(wave)


    def addSineWave(self, A, f0, length, alpha=0):
        """ 現在作成されている音声データに正弦波を加えます。
        Parameters:
            A -- 振幅。
            f0 -- 基本周波数。
            length -- 長さ（秒）。
            alpha -- 位相。
        """
        wave = A * np.sin(2 * np.pi * f0 * np.arange(self.fs * length) / self.fs + alpha)
        self.__add_wave(wave)


    def readframes(self, chunk):
        """ 作成した音声データから chunk バイト分データを読み込んで返します。
        Parameters:
            chunk -- 読み込むバイト数。
        Returns:
            読み込んだ、最大 chunk バイト分のバイナリ列。
        """
        ret = self.__data[self.__pos:(self.__pos+chunk)]
        self.__pos += chunk
        return ret


    def __set_data(self, wave):
        """ 整数列をバイナリデータに変換して保持します。
        Parameters:
            wave -- 音声データを表す整数リスト。
        """
        if self.nbit == 16:
            wave = wave.astype(np.int16)
            self.__data = struct.pack('h' * len(wave), *wave)
            self.__pos = 0


    def __create_wave(self, wave):
        """ [-1, 1]の音声データを元にしてバイナリ列を保持します。
        Parameters:
            wave -- [-1, 1]の数値リスト。
        """
        mx = 2 ** self.nbit // 2 - 1
        filt = np.vectorize(lambda x: min(mx, max(-mx, x)))
        wave = filt(mx * wave)
        self.__set_data(wave)


    def __add_wave(self, wave):
        """ [-1, 1]の音声データを、現在保持しているデータに加えます。
        Parameters:
            wave -- [-1, 1]の数値リスト。
        """
        data = self.getData()
        l = len(data) / self.fs
        mx = 2 ** self.nbit // 2 - 1
        filt = np.vectorize(lambda x: min(mx, max(-mx, x)))
        wave = filt(data + mx * wave[:len(data)])
        self.__set_data(wave)
