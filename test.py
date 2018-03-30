import sys
sys.path.append('modules')
import matplotlib.pyplot as plt
from mywave import WaveReader
from player import Player
from generator import Generator


def waveRead():
    """ WAVE ファイルの読み込みテスト """
    print('waveRead')
    w = WaveReader('data/440Hz_44100Hz_16bit_05sec.wav')
    w.play()


def createSineWaveChord(showFigure=False):
    """ 正弦波の C メジャーコード生成テスト """
    print('createSineWaveChord')
    fs = 44100
    generator = Generator(fs)
    generator.createSineWave(0.3, 262, 3)
    generator.addSineWave(0.3, 330)
    generator.addSineWave(0.3, 392)
    data = generator.getData()

    if showFigure:
        # 波形の一部を表示
        plt.plot(data[:2000])
        plt.show()

    # 再生
    player = Player(2, 1, fs, generator.readframes)
    player.play()


if __name__ == '__main__':
    waveRead()
    createSineWaveChord()
