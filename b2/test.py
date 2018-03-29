import cv2

img = cv2.imread("saving.png")
print(img)
cv2.imwrite("saving.jpg",img)