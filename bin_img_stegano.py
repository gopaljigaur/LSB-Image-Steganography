import cv2 as cv
import numpy as np

delimiter = "#$#$#$#"

def toBinary(msg):
    if type(msg)==str:
        word = ''
        for char in msg:
            asci = ord(char)
            binary = format(asci,"08b")
            word+=binary
        return word
    if type(msg)==list or type(msg)==np.ndarray or type(msg)==bytes:
        words = [0]*len(msg)
        i = 0
        for val in msg:
            binary = format(val, "08b")
            words[i]=binary
            i+=1
        return words
    if type(msg)==int:
        word = format(msg,"08b")
        return word

def toAsci(msg_arr):
    int_lis = [int(i,2) for i in msg_arr]
    char_lis = [chr(i) for i in int_lis]
    string = ''.join([i for i in char_lis])
    return string
    
def embed_message(msg, img):
    available = img.shape[0]*img.shape[1]*3
    print("Maximum characters that can be encoded : "+str(available - len(delimiter)))
    print("Length of current message : "+str(len(msg)))
    msg+=delimiter # delimiter for message
    msg_bin= toBinary(msg)
    mes_len = len(msg_bin)
    if(mes_len>available):
        print("Image is too small for this message.")
        return False
    else:
        cnt = 0
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                rgb = toBinary(img[i][j])
                col = 0
                for color in rgb:
                    img[i][j][col] = int(color[:-1]+msg_bin[cnt],2)
                    col+=1
                    cnt+=1
                    if(cnt>=mes_len):
                        return img
        return False

def decode_message(img):
    bits = ''
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            rgb = toBinary(img[i][j])
            for color in rgb:
                bits+=color[-1]
                
    split = [bits[w:w+8] for w in range(0,len(bits),8)]
    converted = toAsci(split)
    decoded = ''
    for char in converted:
        if(decoded[-len(delimiter):]==delimiter):
            return decoded[:-len(delimiter)]
        else:
            decoded+=char
    return False
                
msg="dev gaur is a fool"

img = cv.imread('test_image.png')
cv.imshow('Original',img)

print("Message to embed : "+msg)
img_enc = embed_message(msg, img)

if type(img_enc)==np.ndarray:
    cv.imshow('Embedded', img_enc)
else:
    print("Could not embed message")
cv.waitKey(0)
cv.destroyAllWindows()

decoded = decode_message(img_enc)

if type(decoded)==str:
    print("Decoded message : "+decoded)
else:
    print("Unable to decode message")
    