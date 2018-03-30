import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
from mywave import WaveReader
from player import Player
from generator import Generator

if __name__ == '__main__':
    # w = WaveReader('440Hz_44100Hz_16bit_05sec.wav')
    # w.play()

    freqList = [262, 294, 330, 349, 392, 440, 494, 523]  # ドレミファソラシド
    fs = 44100
    generator = Generator(fs)
    generator.createSineWave(0.3, freqList[0], 3)
    generator.addSineWave(0.3, freqList[2], np.pi)
    generator.addSineWave(0.3, freqList[4])
    data = generator.getData()

    player = Player(2, 1, fs, generator.readframes)
    player.play()
    plt.plot(data[:2000])
    plt.show()
