import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
import glob

def DoG(fn):
    fn_no_ext = fn.split('\\')[1]
    output="DoG\\"+fn_no_ext
    #read the input file
    img = cv2.imread(str(fn))

    #run a 5x5 gaussian blur then a 3x3 gaussian blr
    blur5 = cv2.GaussianBlur(img,(5,5),0)
    blur3 = cv2.GaussianBlur(img,(3,3),0)

    #write the results of the previous step to new files
#    cv2.imwrite(fn_no_ext+'3x3.jpg', blur3)
#    cv2.imwrite(fn_no_ext+'5x5.jpg', blur5)

    DoGim = blur5 - blur3
    cv2.imwrite(output, DoGim)
    return DoGim

def get_pixel(img, center, x, y):
    new_value = 0
    try:
        if img[x][y] >= center:
            new_value = 1
    except:
        pass
    return new_value


def lbp_calculated_pixel(img, x, y):
    
    '''
     64 | 128 |   1
    ----------------
     32 |   0 |   2
    ----------------
     16 |   8 |   4    
    '''    

    center = img[x][y]
    val_ar = []
    val_ar.append(get_pixel(img, center, x-1, y+1))     # top_right
    val_ar.append(get_pixel(img, center, x, y+1))       # right
    val_ar.append(get_pixel(img, center, x+1, y+1))     # bottom_right
    val_ar.append(get_pixel(img, center, x+1, y))       # bottom
    val_ar.append(get_pixel(img, center, x+1, y-1))     # bottom_left
    val_ar.append(get_pixel(img, center, x, y-1))       # left
    val_ar.append(get_pixel(img, center, x-1, y-1))     # top_left
    val_ar.append(get_pixel(img, center, x-1, y))       # top

    power_val = [1, 2, 4, 8, 16, 32, 64, 128]
    val = 0
    for i in range(len(val_ar)):
        val += val_ar[i] * power_val[i]
        if(x==0 and y==0):
            print(val)
    return val    


def main():
    images=glob.glob("images\\*.jpg")
    output = open("index.csv", "w")
    print("hello")
    for image_file in images:
        img_bgr = cv2.imread(image_file)
        height, width, channel = img_bgr.shape
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        
        k=img.shape[0]
        l=img.shape[1]

        original = np.zeros((height, width,3), np.uint8)
        encrypted = np.zeros((height, width,3), np.uint8)
#        decrypted = np.zeros((height, width,3), np.uint8)
#        img_lbp = np.zeros((height, width,3), np.uint8)
#        enc_img_lbp = np.zeros((height, width,3), np.uint8)
        random = np.zeros((height, width,3), np.uint8)
        randomnumber={}
        for i in range (k):#traverses through height of the image
            for j in range (l): #traverses through width of the image
#                original[i,j]=img[i,j]
                randomnumber[i,j]=np.random.randint(0,255)
                random[i,j]=randomnumber[i,j]
#                img_lbp[i, j] = lbp_calculated_pixel(img, i, j)
                
                # Encryption

                if(((randomnumber[i,j]>=128) and (img[i,j]>=128))):
                    encrypted[i,j]=img[i,j]-128
                    temp=img[i,j]-128
                elif(((randomnumber[i,j]<128) and (img[i,j]<128))):
                    encrypted[i,j]=img[i,j]
                    temp=img[i,j]
                elif(((randomnumber[i,j]>=128) and (img[i,j]<128))):
                    encrypted[i,j]=img[i,j]+128
                    temp=img[i,j]+128
                else:
                    encrypted[i,j]=img[i,j]
                    temp=img[i,j]

#                enc_img_lbp[i, j] = lbp_calculated_pixel(img, i, j)
                
    
        DoG(image_file)
        key=cv2.imread('DoG\\'+image_file.split('\\')[1])
        img1 = cv2.cvtColor(key, cv2.COLOR_BGR2GRAY)
        height, width, channel = key.shape
        k1=img1.shape[0]
        l1=img1.shape[1]
        key_lbp = np.zeros((height, width,3), np.uint8)
        for i in range (k1):#traverses through height of the image
            for j in range (l1):
                key_lbp[i, j] = lbp_calculated_pixel(img1, i, j)
        hist_lbp = cv2.calcHist([key_lbp], [0], None, [256], [0, 256])
        features = [str(i)[1:-2] for i in hist_lbp ]

        #saving encrypted image
        #print(image_file);
       
        cv2.imwrite("encryptedimages\\"+image_file.split('\\')[1].split('.')[0]+".bmp",encrypted)
        cv2.imwrite("random\\"+image_file.split('\\')[1].split('.')[0]+".bmp",random)
        output.write("%s,%s\n" % (image_file.split('\\')[1],",".join(features)))
        

    output.close()
    # caluclate histogram and plot it

    # hist_lbp = cv2.calcHist([img_lbp], [0], None, [256], [0, 256])
    # enc_hist_lbp = cv2.calcHist([enc_img_lbp], [0], None, [256], [0, 256])

if __name__ == '__main__':
    main()
