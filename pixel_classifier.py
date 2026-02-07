import cv2 
import os
import numpy as np
from random import randint

class Pixel_Classifier:
    def __init__(self,path):
        self.path = (path)
        self.files = os.listdir(self.path)
        self.window = 'window'
        self.index = 0
        self.index_cls = 0
        self.list = []
        self.n_cls = 0
        self.cls = []
        self.color = []
        self.classe = ''
        self.dict = {}

    def cls_creator(self):
        self.n_cls = int(input(print('quantas classes voce vai marcar?: ')))
        a = 0
        b = 255
        for i in range(self.n_cls):
            print(f'{i+1}º classe: ')
            name = str(input())
            self.cls.append(name)
            self.color.append((randint(a,b),randint(a,b),randint(a,b)))
            self.dict[name] = []
        self.classe = self.cls[0]
 

    def load_image(self):

        if self.index < 0:
            self.index = 0
        if self.index > len(self.files) -1 :
            self.index = len(self.files) - 1 

        self.complete_path = os.path.join(self.path,self.files[self.index])
        self.img = cv2.imread(self.complete_path)
        cv2.imshow(self.window,self.img)
        self.list = [] # zera a lista de pontos interminados ao mudar de img


    def draw_polygone(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.list.append([x,y])
            cv2.circle(self.img,(x,y),3,self.color[self.index_cls])
            cv2.imshow(self.window,self.img)

        elif event == cv2.EVENT_RBUTTONDOWN:
            self.pts = np.array(self.list,np.int32)
            self.pts.reshape((-1, 1, 2))
            self.getting_pixels(self.pts)
            cv2.polylines(self.img,[self.pts],True,self.color[self.index_cls])
            cv2.imshow(self.window,self.img)
            self.list = []
    

    def getting_pixels(self,pts): 
        self.mask = np.zeros(self.img.shape[:2],np.uint8)
        cv2.fillPoly(self.mask,[pts],255)
        self.indices_y,self.indices_x = np.where(self.mask == 255)
        self.cores_originais = self.img[self.indices_y,self.indices_x]
        cv2.fillPoly(self.img,[pts],self.color[self.index_cls])
        print(f'total de pixels {len(self.cores_originais)} da classe {self.classe}')
        self.saving_pixels(self.cores_originais)


    def saving_pixels(self,pts_tsave):
        for key,value in self.dict.items():
            if self.classe == key:
                pass
        print(self.dict)
        

    def deleting_pixels(self):
        pass
        

    def change_class(self,teleop_key):
        if teleop_key == ord('e'):
            self.index_cls +=1
        elif teleop_key == ord('q'):
            self.index_cls -=1

        if self.index_cls < 0:
            self.index_cls = 0
        if self.index_cls > len(self.cls) -1 :
            self.index_cls = len(self.cls) - 1
        
        self.classe = self.cls[self.index_cls]
        print(f'CLASSE ATUAL: {self.classe}')
        

    def run(self):
        print('Classificador de pixels 2000')
        self.cls_creator()

        cv2.namedWindow(self.window)
        cv2.setMouseCallback(self.window, self.draw_polygone)

        self.load_image()

        print(f'CLASSE ATUAL: {self.classe}')

        while True:
            self.key = cv2.waitKey(0) & 0xFF

            #navegeação das imagens
            if self.key == ord('d'):
                self.index +=1
                self.load_image()
            elif self.key == ord('a'):
                self.index -= 1
                self.load_image()
            #navegação das classes
            elif self.key == ord('q'):
                self.change_class(self.key)
            elif self.key == ord('e'):
                self.change_class(self.key)
            #remove ultima marcação
            elif self.key == ord('z'):
                self.deleting_pixels()
            #quebra do loop
            elif self.key == ord('w'):
                print(self.classe)
                break

        
o = Pixel_Classifier('/home/ivan/color_segmentation/images_color_segmentation')
o.run()
cv2.destroyAllWindows()

# problema 1: da pra fzr um polygono com pontos de classes diferentes 
# problema 2: fzr com que as classes nao sejam hardcoded