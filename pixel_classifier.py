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
        self.cls_flag = False 
        self.cls = []
        self.color = []
        self.classe = ''
        self.dict = {}
        self.img_history = []

    def cls_creator(self):
        self.n_cls = int(input('quantas classes voce vai marcar?: '))
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
        self.img_raw = cv2.imread(self.complete_path)
        self.img = self.img_raw.copy()
        self.img_history = [] # zera o historico da imagem
        self.list = [] # zera a lista de pontos interminados ao mudar de img
        cv2.imshow(self.window,self.img)


    def draw_polygone(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.list) == 0:
                self.img_history.append(self.img.copy())
            self.list.append([x,y])
            cv2.circle(self.img,(x,y),3,self.color[self.index_cls])
            cv2.imshow(self.window,self.img)
            self.cls_flag = False

        elif event == cv2.EVENT_RBUTTONDOWN:
            self.pts = np.array(self.list,np.int32)
            self.pts.reshape((-1, 1, 2))
            self.getting_pixels()
            cv2.fillPoly(self.img,[self.pts],self.color[self.index_cls])
            cv2.imshow(self.window,self.img)
            self.cls_flag = True
            self.list = []
    

    def getting_pixels(self): 
        self.mask = np.zeros(self.img.shape[:2],np.uint8)
        cv2.fillPoly(self.mask,[self.pts],255)
        self.indices_y,self.indices_x = np.where(self.mask == 255)
        self.img_hsv = cv2.cvtColor(self.img_raw,cv2.COLOR_BGR2HSV)
        self.cores_hsv = self.img_hsv[self.indices_y,self.indices_x]
        print(f'{len(self.cores_hsv)} salvos na classe {self.classe}')
        self.saving_pixels()


    def saving_pixels(self):
        if self.classe in self.dict:
            self.dict[self.classe].append(self.cores_hsv)
        else:
            print(f'Erro: classe: {self.classe} nao encontrada')
    
    
    def deleting_pixel(self,pressed_key):
        if pressed_key == ord('z'):
            if self.classe in self.dict:
                list_points = self.dict[self.classe]
                if len(list_points) > 0:
                    list_points.pop()
                    print(f'poligono da classe {self.classe} removido')
                    if len(self.img_history) > 0:
                        self.img = self.img_history.pop()
                        cv2.imshow(self.window,self.img)
                else:
                    print('vc nao possui nenhum ponto nessa lista')
        

    def change_class(self,teleop_key):
        if teleop_key == ord('e') and self.cls_flag:
            self.index_cls +=1
        elif teleop_key == ord('q') and self.cls_flag:
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
                self.deleting_pixel(self.key)
                
            #quebra do loop
            elif self.key == ord('w'):
                break

        
o = Pixel_Classifier('/home/ivan/Pixel_Classifier/images_color_segmentation')
o.run()
cv2.destroyAllWindows()

