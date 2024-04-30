import numpy as np
from scipy.signal import lfilter, tf2zpk
import matplotlib.pyplot as plt
import sounddevice as sd

# Define constants
SAMPLE_RATE = 44100
DECAY_RATE = 0.9998555
BASE_FREQ = 220 // 4  # Frequency of Note A
HARMONIC_RANGE = range(3, 27)

# Define the range for y-axis
Y_MIN, Y_MAX = -4.0, 4.0


def generate_tone(harmonic):
    """Generate a decaying tone for a given harmonic, and return the filtered signal, zeros, and poles."""
    freq = BASE_FREQ * 2 ** (harmonic / 12)
    theta = freq * np.pi / (SAMPLE_RATE / 2)

    # Filter coefficients
    b = np.array([1])
    a = np.array([1, -2 * DECAY_RATE * np.cos(theta), DECAY_RATE**2])

    # Number of samples => 1-second signal
    num_samples = SAMPLE_RATE
    x = np.zeros(num_samples)
    x[0] = 1  # Input signal

    # Filter the input signal
    y = lfilter(b, a, x)

    # Calculate the zeros and poles
    zeros, poles, _ = tf2zpk(b, a)

    return y, zeros, poles


def plot_tone(tone, harmonic, zeros, poles):
    """Plot the given tone with appropriate labels, title, and zeros/poles."""
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(tone / 30)
    plt.ylim(Y_MIN, Y_MAX)
    plt.xlabel("Time (samples)")
    plt.ylabel("Amplitude")
    plt.title(f"Plot for k={harmonic}, R={DECAY_RATE:.7f}")

    plt.subplot(2, 1, 2)
    plt.xlabel("Real Part")
    plt.ylabel("Imaginary Part")
    plt.title("Zeros and Poles")
    plt.scatter(np.real(zeros), np.imag(zeros), marker="o", label="Zeros")
    plt.scatter(np.real(poles), np.imag(poles), marker="x", label="Poles")
    plt.legend()

    plt.tight_layout()
    plt.savefig(f"plot-k-{harmonic}-r-{DECAY_RATE:.7f}.png")


def main():
    """Generate, play, and plot decaying tones for the given harmonic range."""
    for harmonic in HARMONIC_RANGE:
        tone, zeros, poles = generate_tone(harmonic)
        sd.play(tone / 30, SAMPLE_RATE)
        sd.wait()
        plot_tone(tone, harmonic, zeros, poles)


if __name__ == "__main__":
    main()
