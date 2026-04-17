import os

import cv2
import numpy as np
import matplotlib.pyplot as plt


""" ==== FUNKCJE POMOCNICZE ==== """


def printi(img, img_title="image"):
    """Pomocnicza funkcja do wypisania informacji o obrazie."""
    print(f"{img_title}, wymiary: {img.shape}, typ danych: {img.dtype}, wartości: {img.min()} - {img.max()}")


def cv_imshow(img, img_title="image"):
    """
    Funkcja do wyświetlania obrazu w wykorzystaniem okna OpenCV.
    Wykonywane jest przeskalowanie obrazu z rzeczywistymi lub 16-bitowymi całkowitoliczbowymi wartościami pikseli,
    żeby jedną funkcją wywietlać obrazy różnych typów.
    """

    if (img.dtype == np.float32) or (img.dtype == np.float64):
        img_ = img / 255
    elif img.dtype == np.int16:
        img_ = img * 128
    else:
        img_ = img
    cv2.imshow(img_title, img_)
    cv2.waitKey(0)


"""
Obliczanie entropii
"""


def calc_entropy(hist):
    pdf = (
        hist / hist.sum()
    )  ### normalizacja histogramu -> rozkład prawdopodobieństwa; UWAGA: niebezpieczeństwo '/0' dla 'zerowego' histogramu!!!
    # entropy = -(pdf*np.log2(pdf)).sum() ### zapis na tablicach, ale problem z '/0'
    entropy = -sum([x * np.log2(x) for x in pdf if x != 0])
    return entropy


"""
Transformacja falkowa obrazu
"""


def dwt(img):
    """
    Bardzo prosta i podstawowa implementacja, nie uwzględniająca efektywnych metod obliczania DWT
    i dopuszczająca pewne niedokładności.
    """
    maskL = np.array(
        [
            0.02674875741080976,
            -0.01686411844287795,
            -0.07822326652898785,
            0.2668641184428723,
            0.6029490182363579,
            0.2668641184428723,
            -0.07822326652898785,
            -0.01686411844287795,
            0.02674875741080976,
        ]
    )
    maskH = np.array(
        [
            0.09127176311424948,
            -0.05754352622849957,
            -0.5912717631142470,
            1.115087052456994,
            -0.5912717631142470,
            -0.05754352622849957,
            0.09127176311424948,
        ]
    )

    bandLL = cv2.sepFilter2D(img, -1, maskL, maskL)[::2, ::2]
    bandLH = cv2.sepFilter2D(img, cv2.CV_16S, maskL, maskH)[
        ::2, ::2
    ]  ### ze względu na filtrację górnoprzepustową -> wartości ujemne, dlatego wynik 16-bitowy ze znakiem
    bandHL = cv2.sepFilter2D(img, cv2.CV_16S, maskH, maskL)[::2, ::2]
    bandHH = cv2.sepFilter2D(img, cv2.CV_16S, maskH, maskH)[::2, ::2]

    return bandLL, bandLH, bandHL, bandHH


""" Wyznaczanie charakterystyki R-D """


def calc_mse_psnr(img1, img2):
    """Funkcja obliczająca MSE i PSNR dla różnicy podanych obrazów, zakładana wartość pikseli z przedziału [0, 255]."""

    imax = 255.0**2  ### maksymalna wartość sygnału -> 255
    """
    W różnicy obrazów istotne są wartości ujemne, dlatego img1 konwertowany jest do typu np.float64 (liczby rzeczywiste)
    aby nie ograniczać wyniku do przedziału [0, 255].
    """
    mse = (
        ((img1.astype(np.float64) - img2) ** 2).sum() / img1.size
    )  ###img1.size - liczba elementów w img1, ==img1.shape[0]*img1.shape[1] dla obrazów mono, ==img1.shape[0]*img1.shape[1]*img1.shape[2] dla obrazów barwnych
    psnr = 10.0 * np.log10(imax / mse)
    return (mse, psnr)


""" GŁÓWNY PROGRAM """

images_dir = "images/"


def main():
    image_mono = cv2.imread(images_dir + "wyspa_mono.png", cv2.IMREAD_UNCHANGED)
    image_col = cv2.imread(images_dir + "wyspa_col.png", cv2.IMREAD_UNCHANGED)

    printi(image_mono)
    printi(image_col)

    bitrate_mono = 8 * os.stat(images_dir + "wyspa_mono.png").st_size / (image_mono.shape[0] * image_mono.shape[1])

    """ ==== ZADANIE 1 ==== """

    hist_mono_img = cv2.calcHist([image_mono], [0], None, [256], [0, 256]).flatten()
    hist_mono_norm = hist_mono_img / hist_mono_img.sum()

    entropy_mono = calc_entropy(hist_mono_img)
    print(f"Mono bitrate: {bitrate_mono:.4f}")

    """ Obraz różnicowy """

    img_tmp1 = image_mono[:, 1:]  ### wszystkie wiersze (':'), kolumny od 'pierwszej' do ostatniej ('1:')
    img_tmp2 = image_mono[:, :-1]  ### wszystkie wiersze, kolumny od 'zerowej' do przedostatniej (':-1')

    image_hdiff = cv2.addWeighted(img_tmp1, 1, img_tmp2, -1, 0, dtype=cv2.CV_16S)
    printi(image_hdiff, "image_hdiff")

    image_hdiff_0 = cv2.addWeighted(image_mono[:, 0], 1, 0, 0, -127, dtype=cv2.CV_16S) ### od 'zerowej' kolumny obrazu oryginalnego odejmowana stała wartość '127'
    printi(image_hdiff_0, "image_hdiff_0")
    image_hdiff = np.hstack((image_hdiff_0, image_hdiff)) ### połączenie tablic w kierunku poziomym, czyli 'kolumna za kolumną'
    printi(image_hdiff, "image_hdiff")

    cv_imshow(image_hdiff, "image_hdiff")

    hdiff_tmp = (image_hdiff + 255).astype(np.uint16)
    hist_hdiff = cv2.calcHist([hdiff_tmp], [0], None, [511], [0, 511]).flatten()
    hist_hdiff_norm = hist_hdiff / hist_hdiff.sum()

    entropy_hdiff = calc_entropy(hist_hdiff)

    """ Wyświetlenie histogramów oryginału i różnicowego """

    x1 = np.arange(256)
    x2 = np.arange(-255, 256, 1)

    plt.figure()
    plt.plot(x1, hist_mono_norm, color="blue")
    plt.title("Znormalizowany histogram mono")
    plt.grid(True)
    plt.savefig("hist_mono.png")

    plt.figure()
    plt.plot(x2, hist_hdiff_norm, color="red")
    plt.title("Znormalizowany histogram różnicowy")
    plt.grid(True)
    plt.savefig("hist_hdiff.png")

    plt.figure(figsize=(10, 5))
    plt.plot(x1, hist_mono_norm, color="blue", label="Oryginał", linewidth=2)
    plt.plot(x2, hist_hdiff_norm, color="red", label="Różnicowy", linewidth=2)
    plt.title("Porównanie znormalizowanych histogramów")
    plt.xlabel("Wartość")
    plt.ylabel("Prawdopodobieństwo")
    plt.grid(True)
    plt.legend()
    plt.savefig("compare_hist_mono.png")
    plt.show()

    print(f"Entropia mono = {entropy_mono:.4f}")
    print(f"Entropia różnicowego = {entropy_hdiff:.4f}")

if __name__ == "__main__":
    main()
