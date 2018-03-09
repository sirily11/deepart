import socket
import cv2
import numpy as np
class Image_transfer:
    def __init__(self,image_name,ip_address,port=5555):
        self.image_name = image_name
        self.host = ip_address
        self.port = port
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.s.bind((self.host,self.port))
        except Exception as e:
            print(e)
        self.s.listen(5)

    def recive_image(self):
        print("Reciving img")
        conn, addr = self.s.accept()
        length = self.__recvall__(conn,16)
        img_str = self.__recvall__(conn,int(length))
        img = np.fromstring(img_str,dtype='uint8')
        print("Finished reciving image")
        self.s.close()
        return img

    def send_image(self):
        conn,addr = self.s.accept()
        print("Start sending image")
        img = cv2.imread(self.image_name)
        cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        _, img_encode = cv2.imencode('.jpg', img, encode_param)
        img_arr = np.array(img_encode)
        img_str = img_arr.tostring()
        size = len(img_str)
        conn.send(str.encode(str(size)))
        conn.send(img_str)
        print("Finished sending image")
        return True

    def saveImg(self,img,img_name):
        cv2.imwrite(img_name,img)


    def __recvall__(sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf
s = Image_transfer('chicago.jpg',ip_address="10.26.42.38")
s.send_image()
