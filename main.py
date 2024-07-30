from Side import Side
from CVDataAnalysisi import AllPhonesSidesCVData


def plotimage(imei):
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt

    # Read the image from file in grayscale mode
    image_path = r'C:\Users\anachit\OneDrive - Communications Test Design, Inc\Documents\CTDI\EVO\ScratchesAnnotations\evo_images_CSV\all_annotated_images\\'+f"{imei}"  # Replace with your image file path

    bgr_image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Check if the image was successfully loaded
    if bgr_image is None:
        raise FileNotFoundError(f"Image file '{image_path}' not found")

    # Get the original dimensions of the image
    original_height, original_width = bgr_image.shape[:2]

    # Calculate the new dimensions (4 times larger)
    new_height = original_height * 4
    new_width = original_width * 4

    # Resize the image
    resized_image = cv2.resize(bgr_image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

    # Convert the BGR image to RGB
    rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

    # Plot the resized color image using Matplotlib
    plt.imshow(rgb_image)
    plt.title('Resized Color Image')
    plt.axis('off')  # Hide axes
    plt.show()


# # #init
a = AllPhonesSidesCVData()
# #
# # #get manual grades from csv to txt
a.createimeistxtfromcsv()
#
# # #merge data
a.mergeeachsidetoitscsvfile()
a.mergeelsdstocsvfile()
#
# #plot
# # a.plotareaallsidesmergeddata()
# # a.plotlightdeepscracthescountsallsidesbygrade()
#
# #save annotated images (flush manually)
a.saveannotatedimagesbygrade()
#
# plotimage(imei = "Housing_C_359646704867784 - 1.jpg")
# plotimage(imei = "Capture.png")






# print(a.H1H18REGIONS)





