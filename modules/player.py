import pyaudio
import numpy as np

class Player:
    """ PyAudio を利用して音声データの再生を制御するクラスです。 """
    def __init__(self, sampwidth, nchannels, rate, read_func):
        """ プレイヤーを初期化します。
        Parameters:
            format -- 量子化バイト数。
            nchannels -- チャンネル数。
            rate -- サンプリング周波数。
            read_func -- 音声データにおいて、次のバイナリ列を読み込む関数。
                         チャンク（整数）を引数に取るものを指定する。
        """
        self.__pyaudio = pyaudio.PyAudio()
        self.__player = self.__pyaudio.open(
            format=self.__pyaudio.get_format_from_width(sampwidth),
            channels=nchannels,
            rate=rate,
            output=True)
        self.__read_func = read_func


    def __del__(self):
        if self.__player is not None:
            self.__player.close()
        self.__pyaudio.terminate()


    def play(self):
        """ 音声データを同期的に再生します。 """
        chunk = 1024
        data = self.__read_func(chunk)
        while data != b'':
            self.__player.write(data)
            data = self.__read_func(chunk)
        self.__player.close()
        self.__player = None
