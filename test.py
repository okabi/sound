import sys
sys.path.append('modules')
import matplotlib.pyplot as plt
from mywave import WaveReader, WaveWriter
from player import Player
from generator import Generator


def waveRead():
    """ WAVE ファイルの読み込みテスト """
    print('waveRead')
    w = WaveReader('data/440Hz_44100Hz_16bit_05sec.wav')
    w.play()


def createSineWaveChord(showFigure=False, *, path=''):
    """ 正弦波の C メジャーコード生成テスト """
    print('createSineWaveChord')
    fs = 44100
    generator = Generator(fs)
    generator.addSineWave(0.3, 262, 3)
    generator.addSineWave(0.3, 330, 3)
    generator.addSineWave(0.3, 392, 3)
    data = generator.getData()

    if showFigure:
        # 波形の一部を表示
        plt.plot(data[:2000])
        plt.show()

    if path != '':
        # 外部出力
        ww = WaveWriter(path)
        ww.setWaveInfo(sampwidth=2, rate=fs)
        ww.save(data / (2**16 // 2 - 1))
    else:
        # 再生
        player = Player(2, 1, fs, generator.readframes)
        player.play()


def createTriangleWaveChord(showFigure=False, *, path=''):
    """ 三角波の C メジャーコード生成テスト """
    print('createTriangleWaveChord')
    fs = 44100
    generator = Generator(fs)
    generator.addTriangleWave(0.3, 262, 3)
    generator.addTriangleWave(0.3, 330, 3)
    generator.addTriangleWave(0.3, 392, 3)
    data = generator.getData()

    if showFigure:
        # 波形の一部を表示
        plt.plot(data[:2000])
        plt.show()

    if path != '':
        # 外部出力
        ww = WaveWriter(path)
        ww.setWaveInfo(sampwidth=2, rate=fs)
        ww.save(data / (2**16 // 2 - 1))
    else:
        # 再生
        player = Player(2, 1, fs, generator.readframes)
        player.play()


def createSquareWaveChord(showFigure=False, *, path=''):
    """ 矩形波の C メジャーコード生成テスト """
    print('createSquareWaveChord')
    fs = 44100
    generator = Generator(fs)
    generator.addSquareWave(0.3, 262, 3)
    generator.addSquareWave(0.3, 330, 3)
    generator.addSquareWave(0.3, 392, 3)
    data = generator.getData()

    if showFigure:
        # 波形の一部を表示
        plt.plot(data[:2000])
        plt.show()

    if path != '':
        # 外部出力
        ww = WaveWriter(path)
        ww.setWaveInfo(sampwidth=2, rate=fs)
        ww.save(data / (2**16 // 2 - 1))
    else:
        # 再生
        player = Player(2, 1, fs, generator.readframes)
        player.play()


def createSawtoothWaveChord(showFigure=False, *, path=''):
    """ のこぎり波の C メジャーコード生成テスト """
    print('createSawtoothWaveChord')
    fs = 44100
    generator = Generator(fs)
    generator.addSawtoothWave(0.3, 262, 3)
    generator.addSawtoothWave(0.3, 330, 3)
    generator.addSawtoothWave(0.3, 392, 3)
    data = generator.getData()

    if showFigure:
        # 波形の一部を表示
        plt.plot(data[:2000])
        plt.show()

    if path != '':
        # 外部出力
        ww = WaveWriter(path)
        ww.setWaveInfo(sampwidth=2, rate=fs)
        ww.save(data / (2**16 // 2 - 1))
    else:
        # 再生
        player = Player(2, 1, fs, generator.readframes)
        player.play()


if __name__ == '__main__':
    # waveRead()
    createSineWaveChord(path='result/sine.wav')
    createTriangleWaveChord(path='result/triangle.wav')
    createSquareWaveChord(path='result/square.wav')
    createSawtoothWaveChord(path='result/sawtooth.wav')
