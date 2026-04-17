import numpy as np
import matplotlib.pyplot as plt
import timeit

# zadanie 1:
# a) widmo amplitudowe, fazowe oraz twierdzenie Parsevala

N = 8
freq_sampling = 8
T = 1 / freq_sampling
time = np.arange(0, 1, T)

signal = np.sin(2 * np.pi * time)

# Liczenie FFT
fft_values = np.fft.fft(signal)
freq = np.fft.fftfreq(N, T)

magnitude = np.abs(fft_values) / (N / 2)

phase = np.angle(fft_values)
phase[magnitude < 1e-10] = 0

plt.figure(figsize=(10, 8))

# Pobrane próbki
plt.subplot(3, 1, 1)
plt.stem(time, signal)
plt.title('Sygnał w domenie czasu (N=8 próbek)')
plt.xlabel('Czas [s]')
plt.ylabel('Amplituda')
plt.grid(True)

# Widmo amplitudowe
plt.subplot(3, 1, 2)
plt.stem(freq[:N // 2], magnitude[:N // 2])
plt.title('Domena częstotliwości (widmo amplitudowe)')
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Amplituda')
plt.grid(True)

# Widmo fazowe
plt.subplot(3, 1, 3)
plt.stem(freq[:N // 2], phase[:N // 2])
plt.title('Widmo fazowe')
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Faza [rad]')
plt.grid(True)

plt.tight_layout()
plt.savefig('exercise1_part_a.png')
plt.show()
plt.close()

# Twierdzenie Parsevala

energy_time = np.sum(signal**2)
energy_freq = np.sum(magnitude**2) / N

print("--- Weryfikacja Twierdzenia Parsevala ---")
print(f"Energia w dziedzinie czasu: {energy_time}")
print(f"Energia w dziedzinie częstotliwości: {energy_freq}")
if np.isclose(energy_time, energy_freq):
    print("Twierdzenie Parsevala zostało zweryfikowane pomyślnie!")

# b) wydajność czasowa FFT

NUMBER_OF_SAMPLES = [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]
time_data = []

def fft_calc(signal):
    return np.fft.fft(signal)


for s_num in NUMBER_OF_SAMPLES:
    freq_sampling = s_num
    T = 1 / freq_sampling
    time = np.arange(0, 1, T)
    signal = np.sin(2 * np.pi * time)

    times = timeit.repeat(lambda: fft_calc(signal), number=100, repeat=10)
    avg_exec_time_sec = min(times) / 100
    avg_exec_time_micros = avg_exec_time_sec * 1_000_000
    print(f"Liczba próbek (N) = {s_num:4d} | Czas: {avg_exec_time_micros:.2f} mikrosekund")
    time_data.append(avg_exec_time_micros)

plt.figure(figsize=(8, 5))
plt.plot(NUMBER_OF_SAMPLES, time_data, marker='o', linestyle='-', color='b')
plt.title('Czas wykonywania FFT w zależności od liczby próbek (N)')
plt.xlabel('Liczba próbek (N)')
plt.ylabel('Czas wykonania [\u03bcs]')
plt.grid(True)
plt.tight_layout()
plt.savefig('exercise1_part_b.png')
plt.show()


# zadanie 2:

N = 88
A = 2
n = np.arange(N)
n0_values = [0, N // 4, N // 2, 3 * N // 4]

plt.figure(figsize=(12, 12))

for i, n0 in enumerate(n0_values):
    signal_shifted = A * np.sin(2 * np.pi * (n - n0) / N)

    fft_values = np.fft.fft(signal_shifted)
    k = np.arange(N // 2)

    magnitude = np.abs(fft_values) / (N / 2)
    phase = np.angle(fft_values)
    phase[np.abs(fft_values) < 1e-10] = 0

    plt.subplot(4, 2, 2 * i + 1)
    plt.stem(k[:10], magnitude[:10])
    plt.title(f'Widmo amplitudowe (przesunięcie n0 = {n0})')
    plt.xlabel('Indeks częstotliwości (k)')
    plt.ylabel('Amplituda')
    plt.ylim(0, 2.5)
    plt.grid(True, alpha=0.3)

    # Kolumna 2: Widmo fazowe
    plt.subplot(4, 2, 2 * i + 2)
    plt.stem(k[:10], phase[:10])
    plt.title(f'Widmo fazowe (przesunięcie n0 = {n0})')
    plt.xlabel('Indeks częstotliwości (k)')
    plt.ylabel('Faza [rad]')
    plt.ylim(-np.pi, np.pi)
    plt.yticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi], ['$-\pi$', '$-\pi/2$', '0', '$\pi/2$', '$\pi$'])
    plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('exercise2.png')
plt.show()
