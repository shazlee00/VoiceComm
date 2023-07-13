import matplotlib.pyplot as plt
import qrcode
import time

def show_qr_img(data):
    # Generate the QR code
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color='black', back_color='white')
    plt.show()
    plt.ion()  # Enable interactive mode
    plt.imshow(qr_image, cmap='gray')
    plt.axis('off')
    plt.draw()
    plt.pause(0.001)
# Display the QR code image



# qr_image=generate_qr_img("somedata")

 
# for i in range(10):
#     print('i updated')
#     time.sleep(1)
#     if i==5:
#         plt.close()
#         break


# time.sleep(4)
# print("closed")
