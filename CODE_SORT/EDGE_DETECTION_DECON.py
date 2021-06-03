import cv2
from matplotlib import pyplot as plt
import numpy as np


img_CYT = cv2.imread("D:\\Master's Project data - IMG\\wetransfer-46b599\\2020.08.18\\Atg5 KO - receptor localisation\\Stained 11.08.20\\TAX1BP1\\SH-SY5Y - Atg5 KO - 2 h AO - TAX1BP1 (488) Cyt c (568) 63x 4\\Pos0\\img_000000001_Default_000.tif", 0) # load an image

#Output is a 2D complex array. 1st channel real and 2nd imaginary
#For fft in opencv input image needs to be converted to float32
dft_CYT = cv2.dft(np.float32(img_CYT), flags=cv2.DFT_COMPLEX_OUTPUT)
#Rearranges a Fourier transform X by shifting the zero-frequency
#component to the center of the array.
#Otherwise it starts at the tope left corenr of the image (array)
dft_shift_CYT = np.fft.fftshift(dft_CYT)

#For values that are 0 we may end up with indeterminate values for log.
#So we can add 1 to the array to avoid seeing a warning.
magnitude_spectrum_CYT = 20 * np.log(cv2.magnitude(dft_shift_CYT[:, :, 0], dft_shift_CYT[:, :, 1]))


# Circular HPF mask, center circle is 0, remaining all ones
#Can be used for edge detection because low frequencies at center are blocked
#and only high frequencies are allowed. Edges are high frequency components.
#Amplifies noise.

rows_CYT, cols_CYT = img_CYT.shape
crow_CYT, ccol_CYT = int(rows_CYT / 2), int(cols_CYT / 2)


mask_CYT = np.ones((rows_CYT, cols_CYT, 2), np.uint8)

r = 40
center_CYT = [crow_CYT, ccol_CYT]

x_CYT, y_CYT = np.ogrid[:rows_CYT, :cols_CYT]

mask_area_CYT = (x_CYT - center_CYT[0]) ** 2 + (y_CYT - center_CYT[1]) ** 2 <= r*r
mask_CYT[mask_area_CYT] = 0


# Circular LPF mask, center circle is 1, remaining all zeros
# Only allows low frequency components - smooth regions
#Can smooth out noise but blurs edges.
#
"""
rows_CYT, cols_CYT = img_CYT.shape
crow_CYT, ccol_CYT = int(rows_CYT / 2), int(cols_CYT / 2)
mask_CYT = np.zeros((rows_CYT, cols_CYT, 2), np.uint8)
r = 400
center_CYT = [crow_CYT, ccol_CYT]
x_CYT, y_CYT = np.ogrid[:rows_CYT, :cols_CYT]
mask_area_CYT = (x_CYT - center_CYT[0]) ** 2 + (y_CYT - center_CYT[1]) ** 2 <= r*r
mask_CYT[mask_area_CYT] = 1

# Band Pass Filter - Concentric circle mask, only the points living in concentric circle are ones
"""
"""
rows_CYT, cols_CYT = img_CYT.shape
crow_CYT, ccol_CYT = int(rows_CYT / 2), int(cols_CYT / 2)
mask_CYT = np.zeros((rows_CYT, cols_CYT, 2), np.uint8)
r_out = 100
r_in = 100
center_CYT = [crow_CYT, ccol_CYT]
x_CYT, y_CYT = np.ogrid[:rows_CYT, :cols_CYT]
mask_area_CYT = np.logical_and(((x_CYT - center_CYT[0]) ** 2 + (y_CYT - center_CYT[1]) ** 2 >= r_in ** 2),
                           ((x_CYT - center_CYT[0]) ** 2 + (y_CYT - center_CYT[1]) ** 2 <= r_out ** 2))
mask_CYT[mask_area_CYT] = 1
"""

# apply mask and inverse DFT: Multiply fourier transformed image (values)
#with the mask values.
fshift_CYT = dft_shift_CYT * mask_CYT

#Get the magnitude spectrum (only for plotting purposes)
fshift_mask_mag_CYT = 20 * np.log(cv2.magnitude(fshift_CYT[:, :, 0], fshift_CYT[:, :, 1]))

#Inverse shift to shift origin back to top left.
f_ishift_CYT = np.fft.ifftshift(fshift_CYT)

#Inverse DFT to convert back to image domain from the frequency domain.
#Will be complex numbers
img_back_CYT = cv2.idft(f_ishift_CYT)

#Magnitude spectrum of the image domain
img_back_CYT = cv2.magnitude(img_back_CYT[:, :, 0], img_back_CYT[:, :, 1])

fig = plt.figure(figsize=(12, 12))
ax1 = fig.add_subplot(2,2,1)
ax1.imshow(img_CYT, cmap='gray')
ax1.title.set_text('Input Image')
ax2 = fig.add_subplot(2,2,2)
ax2.imshow(magnitude_spectrum_CYT, cmap='gray')
ax2.title.set_text('FFT of image')
ax3 = fig.add_subplot(2,2,3)
ax3.imshow(fshift_mask_mag_CYT, cmap='gray')
ax3.title.set_text('FFT + Mask')
ax4 = fig.add_subplot(2,2,4)
ax4.imshow(img_back_CYT, cmap='gray')
ax4.title.set_text('After inverse FFT')
plt.show()
