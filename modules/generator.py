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
        # 正弦波の作成
        wave = A * np.sin(2 * np.pi * f0 * np.arange(self.fs * length) / self.fs)
        mx = 2 ** self.nbit // 2 - 1
        filt = np.vectorize(lambda x: min(mx, max(-mx, x)))
        wave = filt(mx * wave)

        # バイナリ列への変換
        self.__set_data(wave)


    def addSineWave(self, A, f0, alpha=0):
        """ 現在作成されている音声データに正弦波を加えます。
        Parameters:
            A -- 振幅。
            f0 -- 基本周波数。
            alpha -- 位相。
        """
        # 既存データの数値列への変換
        data = self.getData()

        # 正弦波を加算
        l = len(data) / self.fs
        wave = A * np.sin(2 * np.pi * f0 * np.arange(self.fs * l) / self.fs + alpha)
        mx = 2 ** self.nbit // 2 - 1
        filt = np.vectorize(lambda x: min(mx, max(-mx, x)))
        wave = filt(data + mx * wave)

        # バイナリ列への変換
        self.__set_data(wave)


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
