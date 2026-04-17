import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data_dir = "./"


def cv_imshow(img, img_title="image"):
    # cv2.namedWindow(img_title, cv2.WINDOW_AUTOSIZE)  # cv2.WINDOW_NORMAL

    # przeskalowanie obrazu z rzeczywistymi wartościami pikseli, żeby jedną funkcją wywietlać obrazy różnych typów
    if (img.dtype == np.float32) or (img.dtype == np.float64):
        img_ = img / 255
    else:
        img_ = img
    cv2.imshow(img_title, img_)
    cv2.waitKey(1)


def printi(img, img_title="image"):
    print(f"{img_title}, wymiary: {img.shape}, typ danych: {img.dtype}, wartości: {img.min()} - {img.max()}")


def calcPSNR(img1, img2):
    imax = 255.**2  # zakładana wartość pikseli z przedziału [0, 255]
    # w różnicy obrazów istotne są wartości ujemne, dlatego img1 konwertowany do typu np.float64 (liczby rzeczywiste) aby nie ograniczać wyniku do przedziału [0, 255]
    mse = ((img1.astype(np.float64) - img2)**2).sum() / img1.size  # img1.size - liczba elementów w img1, ==img1.shape[0]*img1.shape[1] dla obrazów mono, ==img1.shape[0]*img1.shape[1]*img1.shape[2] dla obrazów barwnych
    return 10.0 * np.log10(imax / mse)


# Zadanie 1 - filtracja barwna obrazu cyfrowego

image = cv2.imread(data_dir + "color/wyspa_col.png", cv2.IMREAD_UNCHANGED)

# Szumy impulsowe

inoise_image = cv2.imread(data_dir + "color_inoise1/wyspa_col_inoise.png", cv2.IMREAD_UNCHANGED)

gblur_imgi_3 = cv2.GaussianBlur(inoise_image, (3, 3), 0)
blur_imgi_3 = cv2.medianBlur(inoise_image, 3)

gblur_imgi_5 = cv2.GaussianBlur(inoise_image, (5, 5), 0)
blur_imgi_5 = cv2.medianBlur(inoise_image, 5)

gblur_imgi_7 = cv2.GaussianBlur(inoise_image, (7, 7), 0)
blur_imgi_7 = cv2.medianBlur(inoise_image, 7)

# Szumy gaussowskie

noise_image = cv2.imread(data_dir + "color_noise/wyspa_col_noise.png", cv2.IMREAD_UNCHANGED)

gblur_img_3 = cv2.GaussianBlur(noise_image, (3, 3), 0)
blur_img_3 = cv2.medianBlur(noise_image, 3)

gblur_img_5 = cv2.GaussianBlur(noise_image, (5, 5), 0)
blur_img_5 = cv2.medianBlur(noise_image, 5)

gblur_img_7 = cv2.GaussianBlur(noise_image, (7, 7), 0)
blur_img_7 = cv2.medianBlur(noise_image, 7)


cv2.imwrite(data_dir + "gblur_imgi_3.png", gblur_imgi_3)
cv2.imwrite(data_dir + "gblur_imgi_5.png", gblur_imgi_5)
cv2.imwrite(data_dir + "gblur_imgi_7.png", gblur_imgi_7)
cv2.imwrite(data_dir + "blur_imgi_3.png", blur_imgi_3)
cv2.imwrite(data_dir + "blur_imgi_5.png", blur_imgi_5)
cv2.imwrite(data_dir + "blur_imgi_7.png", blur_imgi_7)


cv2.imwrite(data_dir + "gblur_img_3.png", gblur_img_3)
cv2.imwrite(data_dir + "gblur_img_5.png", gblur_img_5)
cv2.imwrite(data_dir + "gblur_img_7.png", gblur_img_7)
cv2.imwrite(data_dir + "blur_img_3.png", gblur_img_3)
cv2.imwrite(data_dir + "blur_img_5.png", gblur_img_5)
cv2.imwrite(data_dir + "blur_img_7.png", gblur_img_7)

# Liczenie PSNR

psnr_results = np.array([
    [calcPSNR(image, gblur_img_3), calcPSNR(image, blur_img_3), calcPSNR(image, gblur_imgi_3), calcPSNR(image, blur_imgi_3)],
    [calcPSNR(image, gblur_img_5), calcPSNR(image, blur_img_5), calcPSNR(image, gblur_imgi_5), calcPSNR(image, blur_imgi_5)],
    [calcPSNR(image, gblur_img_7), calcPSNR(image, blur_img_7), calcPSNR(image, gblur_imgi_7), calcPSNR(image, blur_imgi_7)]
], np.float64)

headers = pd.MultiIndex.from_product([['Szum Gaussa', 'Szum impulsowy'], ['Filtr Gaussa', 'Filtr medianowy']])
rows = ['3x3', '5x5', '7x7']

table = pd.DataFrame(psnr_results, index=rows, columns=headers, )
table.index.name = "Maska"

print("\n                   --- WYNIKI PSNR [dB] ---")
print(table)


# Zadanie 2 - przesunięcie histogramu


image = cv2.imread(data_dir + "color/wyspa_col.png", cv2.IMREAD_UNCHANGED)

image_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
y, cr, cb = cv2.split(image_yuv)
y_eq = cv2.equalizeHist(y)
image_yuv_eq = cv2.merge([y_eq, cr, cb])
image_eq = cv2.cvtColor(image_yuv_eq, cv2.COLOR_YCrCb2BGR)

cv2.imwrite(data_dir + "equalized_image.png", image_eq)

plt.figure(figsize=(12, 8))

# Oryginalny obraz (konwersja BGR do RGB dla prawidłowego wyświetlenia w Matplotlib)
plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Oryginał")
plt.axis('off')

# Obraz po wyrównaniu histogramu
plt.subplot(2, 2, 2)
plt.imshow(cv2.cvtColor(image_eq, cv2.COLOR_BGR2RGB))
plt.title("Po wyrównaniu histogramu (tylko Y)")
plt.axis('off')

# Histogram oryginalnego kanału Y
plt.subplot(2, 2, 3)
plt.hist(y.flatten(), 256, [0, 256], color='r')
plt.title("Histogram jasności (Oryginał)")
plt.xlim([0, 256])

# Histogram wyrównanego kanału Y
plt.subplot(2, 2, 4)
plt.hist(y_eq.flatten(), 256, [0, 256], color='g')
plt.title("Histogram jasności (Wyrównany)")
plt.xlim([0, 256])

plt.tight_layout()
plt.show()


# Zadanie 3 - wyostrzanie obrazu

image = cv2.imread(data_dir + "color/wyspa_col.png", cv2.IMREAD_UNCHANGED)
cv2.imshow("Oryginal BGR", image)
cv2.waitKey(0)

image_ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

y, cr, cb = cv2.split(image_ycrcb)

y_blur = cv2.GaussianBlur(y, (3, 3), 0)

y_laplace = cv2.Laplacian(y_blur, cv2.CV_64F)

y_64f = np.float64(y)

WEIGHTS = [-1, -2, -3, -4]

for w in WEIGHTS:
    y_sharp = cv2.addWeighted(y_64f, 1.0, y_laplace, w, 0, dtype=cv2.CV_8U)
    image_ycrcb_sharp = cv2.merge([y_sharp, cr, cb])
    image_sharp = cv2.cvtColor(image_ycrcb_sharp, cv2.COLOR_YCrCb2BGR)
    cv2.imshow(f"Wyostrzony obraz (waga: {w})", image_sharp)
    cv2.imwrite(f"laplac_weight_{w}.png", image_sharp)
    cv2.waitKey(0)
