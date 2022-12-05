import cv2
import os

PATH = "dataset"

def remove_background(path):
    colored_image = cv2.imread(path)
    grey_image = cv2.cvtColor(colored_image, cv2.COLOR_RGB2GRAY)
    for _ in range(3):
        grey_image = cv2.GaussianBlur(grey_image, (51, 51), 0)
    _, thresh = cv2.threshold(grey_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Apply mask to colored_image
    colored_image = cv2.bitwise_or(colored_image, colored_image, mask=cv2.bitwise_not(thresh))
    new_path = path.split('/')
    new_path[0] = 'noBg_' + new_path[0]
    # Create path if not exist
    for i in range(1, len(new_path)):
        if not os.path.exists('/'.join(new_path[:i])):
            os.mkdir('/'.join(new_path[:i]))
    # Save image
    cv2.imwrite('/'.join(new_path), colored_image)
    

if __name__ == '__main__':
    # Create a new directory
    for root, dirs, files in os.walk(PATH):
        for file in files:
            if file.endswith(".jpg"):
                if "Train" in root.split('/') and 'resized' not in root.split('/'):
                    remove_background(os.path.join(root, file))
                elif "Test" in root.split('/') and 'resized' not in root.split('/'):
                    remove_background(os.path.join(root, file))
                else :
                    print(os.path.join(root, file) + ' Found')