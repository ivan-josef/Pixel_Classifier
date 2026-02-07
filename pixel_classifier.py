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
        self.dict_pixels = {}
        self.dict_poly = {}


    # this function is responsible for creating classes and their respective dictionaires 
    # for storing pixels and polygons
    def cls_creator(self):
        self.n_cls = int(input('how many classes do you want to mark?: '))
        a = 0
        b = 255
        for i in range(self.n_cls):
            print(f'{i+1}º class: ')
            name = input()
            self.cls.append(name)
            self.color.append((randint(a,b),randint(a,b),randint(a,b)))

            # dictionaires
            self.dict_pixels[name] = []
            self.dict_poly[name] = []

        self.classe = self.cls[0]
 
    # this function is responsible for loading the image, controling the swap index, and calling 
    # the refresh_screen function
    def load_image(self):
        if self.index < 0:
            self.index = 0
        if self.index > len(self.files) -1:
            self.index = len(self.files) - 1 

        self.complete_path = os.path.join(self.path,self.files[self.index])
        self.img_raw = cv2.imread(self.complete_path)
        self.list = [] # The list of points is emptied if you change the image.
        self.refresh_screen()


    # This function is responsible for drawing polygons whenever an image or a polygon is deleted or drawed.
    def refresh_screen(self):
        self.img = self.img_raw.copy()

        for i,nome_clas in enumerate(self.cls):
            cor = self.color[i]
            lista_poligonos = self.dict_poly[nome_clas]

            for poly in lista_poligonos:
                cv2.fillPoly(self.img,[poly],cor)

        cv2.imshow(self.window,self.img)

    # This is the mouse callback function, responsible for drawing the points and calling the getting_pixels and 
    # refresh_screen functions to draw the polygons.
    def draw_polygone(self,event,x,y,flags,param):
        
        if event == cv2.EVENT_LBUTTONDOWN:
            self.list.append([x,y])
            cv2.circle(self.img,(x,y),3,self.color[self.index_cls])
            cv2.imshow(self.window,self.img)

            self.cls_flag = False # This flag prevents a polygon from being formed by two different classes.

        elif event == cv2.EVENT_RBUTTONDOWN:
            self.pts = np.array(self.list,np.int32)
            self.pts.reshape((-1, 1, 2))
            self.getting_pixels()
            self.dict_poly[self.classe].append(self.pts)
            self.refresh_screen()

            self.cls_flag = True # This flag prevents a polygon from being formed by two different classes.
            self.list = [] # clear the list of points
    

    # This function is responsible for retrieving the pixels below the polygon.
    def getting_pixels(self): 
        self.mask = np.zeros(self.img.shape[:2],np.uint8)
        cv2.fillPoly(self.mask,[self.pts],255)
        self.indices_y,self.indices_x = np.where(self.mask == 255)

        # convert to the HSV standard
        self.img_hsv = cv2.cvtColor(self.img_raw,cv2.COLOR_BGR2HSV)
        self.colors_hsv = self.img_hsv[self.indices_y,self.indices_x]

        print(f'{len(self.colors_hsv)} salvos na classe {self.classe}')
        self.saving_pixels()

    # saves the pixels in their respective classes
    def saving_pixels(self):
        if self.classe in self.dict_pixels:
            self.dict_pixels[self.classe].append(self.cores_hsv)
        else:
            print(f'Erro: classe: {self.classe} nao encontrada')
    
    # This function is responsible for removing pixels from the dictionary and polygons from the image.
    def deleting_pixel(self,pressed_key):
        if pressed_key == ord('z'):
            if self.classe in self.dict_pixels:
                list_points = self.dict_pixels[self.classe]
                list_polys = self.dict_poly[self.classe]
                if len(list_points) > 0:
                    list_points.pop()
                    if len(list_polys) > 0:
                        list_polys.pop()
                    print(f'poligono da classe {self.classe} removido')

                    self.refresh_screen()
                else:
                    print('vc nao possui nenhum ponto nessa lista')

    # this function swaps classes
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

