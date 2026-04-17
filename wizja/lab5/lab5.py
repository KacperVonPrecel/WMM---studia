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
    )  # normalizacja histogramu -> rozkład prawdopodobieństwa; UWAGA: niebezpieczeństwo '/0' dla 'zerowego' histogramu!!!
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
    ]  # ze względu na filtrację górnoprzepustową -> wartości ujemne, dlatego wynik 16-bitowy ze znakiem
    bandHL = cv2.sepFilter2D(img, cv2.CV_16S, maskH, maskL)[::2, ::2]
    bandHH = cv2.sepFilter2D(img, cv2.CV_16S, maskH, maskH)[::2, ::2]

    return bandLL, bandLH, bandHL, bandHH


""" Wyznaczanie charakterystyki R-D """


def calc_mse_psnr(img1, img2):
    """Funkcja obliczająca MSE i PSNR dla różnicy podanych obrazów, zakładana wartość pikseli z przedziału [0, 255]."""

    imax = 255.0**2  # maksymalna wartość sygnału -> 255
    """
    W różnicy obrazów istotne są wartości ujemne, dlatego img1 konwertowany jest do typu np.float64 (liczby rzeczywiste)
    aby nie ograniczać wyniku do przedziału [0, 255].
    """
    mse = (
        ((img1.astype(np.float64) - img2) ** 2).sum() / img1.size
    )
    psnr = 10.0 * np.log10(imax / mse)
    return (mse, psnr)


""" GŁÓWNY PROGRAM """

""" OBRAZ MONOCHROMATYCZNY """

images_dir = "images/"


def main():
    image_mono = cv2.imread(images_dir + "wyspa_mono.png", cv2.IMREAD_UNCHANGED)

    printi(image_mono)

    bitrate_mono = 8 * os.stat(images_dir + "wyspa_mono.png").st_size / (image_mono.shape[0] * image_mono.shape[1])

    """ ==== ZADANIE 1 ==== """

    hist_mono_img = cv2.calcHist([image_mono], [0], None, [256], [0, 256]).flatten()
    hist_mono_norm = hist_mono_img / hist_mono_img.sum()

    entropy_mono = calc_entropy(hist_mono_img)
    print(f"Mono bitrate: {bitrate_mono:.4f}")

    """ Obraz różnicowy """

    img_tmp1 = image_mono[:, 1:]  # wszystkie wiersze (':'), kolumny od 'pierwszej' do ostatniej ('1:')
    img_tmp2 = image_mono[:, :-1]  # wszystkie wiersze, kolumny od 'zerowej' do przedostatniej (':-1')

    image_hdiff = cv2.addWeighted(img_tmp1, 1, img_tmp2, -1, 0, dtype=cv2.CV_16S)
    printi(image_hdiff, "image_hdiff")

    image_hdiff_0 = cv2.addWeighted(image_mono[:, 0], 1, 0, 0, -127, dtype=cv2.CV_16S) # od 'zerowej' kolumny obrazu oryginalnego odejmowana stała wartość '127'
    printi(image_hdiff_0, "image_hdiff_0")
    image_hdiff = np.hstack((image_hdiff_0, image_hdiff)) # połączenie tablic w kierunku poziomym, czyli 'kolumna za kolumną'
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

    """ Wyliczanie współczynników DWT """

    ll, lh, hl, hh = dwt(image_mono)

    printi(ll, "LL")
    printi(lh, "LH")
    printi(hl, "HL")
    printi(hh, "HH")

    cv_imshow(ll, "LL2")
    cv_imshow(cv2.multiply(lh, 2), "LH2")
    cv_imshow(cv2.multiply(hl, 2), "HL2")
    cv_imshow(cv2.multiply(hh, 2), "HH2")

    hist_ll = cv2.calcHist([ll], [0], None, [256], [0, 256]).flatten()
    hist_lh = cv2.calcHist([(lh + 255).astype(np.uint16)], [0], None, [511], [0, 511]).flatten()
    hist_hl = cv2.calcHist([(hl + 255).astype(np.uint16)], [0], None, [511], [0, 511]).flatten()
    hist_hh = cv2.calcHist([(hh + 255).astype(np.uint16)], [0], None, [511], [0, 511]).flatten()
    H_ll = calc_entropy(hist_ll)
    H_lh = calc_entropy(hist_lh)
    H_hl = calc_entropy(hist_hl)
    H_hh = calc_entropy(hist_hh)

    print(f"Bitrate: {bitrate_mono:.4f}")
    print(f"H(obraz_mono) = {entropy_mono:.4f}")
    print(f"H(obraz_różnicowy) = {entropy_hdiff:.4f}")
    print(f"H(LL) = {H_ll:.4f} \nH(LH) = {H_lh:.4f} \nH(HL) = {H_hl:.4f} \nH(HH) = {H_hh:.4f} \nH_śr = {(H_ll+H_lh+H_hl+H_hh)/4:.4f}")

    fig = plt.figure()
    fig.set_figheight(fig.get_figheight() * 2)  # zwiększenie rozmiarów okna
    fig.set_figwidth(fig.get_figwidth() * 2)
    plt.title("Współczynniki DWT")
    plt.subplot(2, 2, 1)
    plt.plot(hist_ll, color="blue")
    plt.title("LL")
    plt.xlim([0, 255])
    plt.grid(True)
    plt.subplot(2, 2, 3)
    plt.plot(np.arange(-255, 256, 1), hist_lh, color="red")
    plt.title("LH")
    plt.xlim([-255, 255])
    plt.grid(True)
    plt.subplot(2, 2, 2)
    plt.plot(np.arange(-255, 256, 1), hist_hl, color="red")
    plt.title("HL")
    plt.xlim([-255, 255])
    plt.grid(True)
    plt.subplot(2, 2, 4)
    plt.plot(np.arange(-255, 256, 1), hist_hh, color="red")
    plt.title("HH")
    plt.xlim([-255, 255])
    plt.grid(True)

    plt.savefig("compare_hist_DWT.png")
    plt.close()

    """ OBRAZ BARWNY """

    image_col = cv2.imread(images_dir + "wyspa_col.png")
    printi(image_col)

    # cv2.imread wczytuje obraz kolorowy domyślnie jako BGR
    image_r = image_col[:, :, 2]
    image_g = image_col[:, :, 1]
    image_b = image_col[:, :, 0]

    hist_r = cv2.calcHist([image_r], [0], None, [256], [0, 256]).flatten()
    hist_g = cv2.calcHist([image_g], [0], None, [256], [0, 256]).flatten()
    hist_b = cv2.calcHist([image_b], [0], None, [256], [0, 256]).flatten()

    H_R = calc_entropy(hist_r)
    H_G = calc_entropy(hist_g)
    H_B = calc_entropy(hist_b)
    print(f"H(R) = {H_R:.4f} \nH(G) = {H_G:.4f} \nH(B) = {H_B:.4f} \nH_śr = {(H_R+H_G+H_B)/3:.4f}")

    cv_imshow(image_r, "R")
    cv_imshow(image_g, "G")
    cv_imshow(image_b, "B")
    plt.figure()
    plt.plot(hist_r, color="red", label="R")
    plt.plot(hist_g, color="green", label="G")
    plt.plot(hist_b, color="blue", label="B")
    plt.title("Histogram BGR")
    plt.xlim([0, 255])
    plt.grid(True)
    plt.legend()

    plt.savefig("hist_bgr.png")
    plt.show()

    image_YCrCb = cv2.cvtColor(image_col, cv2.COLOR_BGR2YCrCb)
    printi(image_YCrCb, "Image_YCrCb")

    hist_y = cv2.calcHist([image_YCrCb[:, :, 0]], [0], None, [256], [0, 256]).flatten()
    hist_cr = cv2.calcHist([image_YCrCb[:, :, 1]], [0], None, [256], [0, 256]).flatten()
    hist_cb = cv2.calcHist([image_YCrCb[:, :, 2]], [0], None, [256], [0, 256]).flatten()

    H_Y = calc_entropy(hist_y)
    H_Cr = calc_entropy(hist_cr)
    H_Cb = calc_entropy(hist_cb)
    print(f"H(Y) = {H_Y:.4f} \nH(Cr) = {H_Cr:.4f} \nH(Cb) = {H_Cb:.4f} \nH_śr = {(H_Y+H_Cr+H_Cb)/3:.4f}")

    cv_imshow(image_YCrCb[:, :, 0], "Y")
    cv_imshow(image_YCrCb[:, :, 1], "Cr")
    cv_imshow(image_YCrCb[:, :, 2], "Cb")
    plt.figure()
    plt.plot(hist_y, color="gray", label="Y")
    plt.plot(hist_cr, color="red", label="Cr")
    plt.plot(hist_cb, color="blue", label="Cb")
    plt.title("Histogram YCrCb")
    plt.xlim([0, 255])
    plt.grid(True)
    plt.legend()

    plt.savefig("hist_ycrcb.png")
    plt.show()

    xx = []
    ym = []
    yp = []

    for quality in [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 99]:
        out_file_name = f"out_image_q{quality:03d}.jpg"
        """ Zapis do pliku w formacie .jpg z ustaloną 'jakością' """
        cv2.imwrite(out_file_name, image_col, (cv2.IMWRITE_JPEG_QUALITY, quality))
        """ Odczyt skompresowanego obrazu, policzenie bitrate'u i PSNR """
        image_compressed = cv2.imread(out_file_name, cv2.IMREAD_UNCHANGED)
        bitrate = 8 * os.stat(out_file_name).st_size / (image_col.shape[0] * image_col.shape[1]) ### image.shape == image_compressed.shape
        mse, psnr = calc_mse_psnr(image_col, image_compressed)

        xx.append(bitrate)
        ym.append(mse)
        yp.append(psnr)

        """ Logi na terminal do łatwego podglądu """
        print(f"Quality={quality:2d}: Bitrate={bitrate:.4f}, MSE={mse:.4f}, PSNR={psnr:.4f} dB")

    fig = plt.figure()
    fig.set_figwidth(fig.get_figwidth() * 2)
    plt.suptitle("Charakterystyki R-D")
    plt.subplot(1, 2, 1)
    plt.plot(xx, ym, "-.")
    plt.title("MSE(R)")
    plt.xlabel("bitrate")
    plt.ylabel("MSE", labelpad=0)
    plt.subplot(1, 2, 2)
    plt.plot(xx, yp, "-o")
    plt.title("PSNR(R)")
    plt.xlabel("bitrate")
    plt.ylabel("PSNR [dB]", labelpad=0)

    plt.savefig("r-d_characteristics")
    plt.show()

    bitrate_png = 8 * os.stat(images_dir + "wyspa_col.png").st_size / (image_mono.shape[0] * image_mono.shape[1])
    print(f"Bitrate dla PNG: {bitrate_png:.4f}")


if __name__ == "__main__":
    main()
