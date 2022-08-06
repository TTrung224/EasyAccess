# import matplotlib.pyplot as plt
import numpy as np
import cv2
#Hellooo
img = cv2.imread("images/amber-heard.png")
# plt.figure(figsize=(6, 6))
print(img.shape)

cv2.putText(
    img=img,
    text=f"opencv version: {cv2.__version__}",
    org=(30, 40),
    fontFace=cv2.FONT_HERSHEY_PLAIN,
    fontScale=1.5,
    color=(0, 255, 0),
    thickness=2,
    lineType=cv2.LINE_AA,
)
# , cmap="gray", interpolation="bicubic"
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
