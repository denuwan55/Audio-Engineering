import numpy as np
from scipy.signal import lfilter
import matplotlib.pyplot as plt
import sounddevice as sd

# Define constants
SAMPLE_RATE = 44100
DECAY_RATE = 0.9998
DECAY_RATE_RANGE = [0.1, 0.5, 0.8, 0.9, 0.99, 0.999, 0.9998]
BASE_FREQ = 110  # Frequency of Note A
HARMONIC_RANGE = range(3, 27)

# Define the range for y-axis
Y_MIN, Y_MAX = -1.8, 1.8


def generate_tone(harmonic, decay_rate):
    """Generate a decaying tone for a given harmonic."""
    freq = BASE_FREQ * 2 ** (harmonic / 12)
    theta = freq * np.pi / (SAMPLE_RATE / 2)

    # Filter coefficients
    b = np.array([1])
    a = np.array([1, -2 * decay_rate * np.cos(theta), decay_rate**2])

    # Number of samples => 1-second signal
    num_samples = SAMPLE_RATE
    x = np.zeros(num_samples)
    x[0] = 1  # Input signal

    return lfilter(b, a, x)


def plot_tone(tone, harmonic, decay_rate):
    """Plot the given tone with appropriate labels and title."""
    plt.figure()
    plt.plot(tone / 30)
    plt.ylim(Y_MIN, Y_MAX)
    # plt.xlabel("Time (samples)")
    # plt.ylabel("Amplitude")
    # plt.title(f"Plot for k={harmonic}, R={decay_rate:.7f}")
    plt.title(f"R={decay_rate:.7f}")
    plt.tight_layout()
    plt.savefig(f"plot-k-{harmonic}-r-{decay_rate:.7f}.png")


def main():
    """Generate, play, and plot tones for the given decay and harmonic range."""
    harmonic = 4
    for decay_rate in DECAY_RATE_RANGE:
        tone = generate_tone(harmonic, decay_rate)
        sd.play(tone / 30, SAMPLE_RATE)
        sd.wait()
        plot_tone(tone, harmonic, decay_rate)

    # for harmonic in HARMONIC_RANGE:
    #     tone = generate_tone(harmonic, DECAY_RATE)
    #     sd.play(tone / 30, SAMPLE_RATE)
    #     sd.wait()
    #     plot_tone(tone, harmonic, DECAY_RATE)


if __name__ == "__main__":
    main()
