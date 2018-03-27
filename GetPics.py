# -*- coding: utf-8 -*-

import PicsPy
import os
from datetime import datetime
from math import *
from PIL import Image, ImageDraw #Подключим необходимые библиотеки. 

global sImg

mp = [] # карта пикселей
esize = 8 # размер стороны четверти изображения
sz = 2*esize
size = (sz,sz)
size2 = (2*sz,2*sz)

#dirs = [] # внутренние каталоги

# PicsPy.directory - Каталог из которого будем брать изображения
# dirs = ['e:\\MDM\\EX63']
# PicsPy.directory = 'C:\\Users\\PovarnitsynDA\\Downloads\\Свадьба_ДЛ'

# Запись лога
def log(s):
    f = open('log.txt', 'a', encoding='utf-8')
    if s:
        s = s.replace('\n',' \ ')
        f.write(str(datetime.today()) + ': ' + s + '\n')
        print(s)
    return True

# Определение направления яркости для 4х писелей
def eBrMap(img):
    global sImg
    mFr = '' # карта силы яркости
    mf = [0,0,0,0]; fr = 0
    fsum = 0
    #pix = img.load() #Выгружаем значения пикселей.
    for x in range(sz):
        for y in range(sz):
            if 0 < x < (sz - 1) and 0 < y < (sz - 1):
                idp = mp[x*esize+y]
                mf[1] = mp[(x-1)*sz+y]
                mf[2] = mp[(x+1)*sz+y]
                mf[0] = mp[x*sz+y-1]
                mf[3] = mp[x*sz+y+1]
                dm = 0; t = -1; k = 0
                for kmf in mf:
                    if kmf - idp > dm :
                        dm = kmf - idp
                        t = k
                    k += 1
                if t >= 0: fr = 2*t+int(dm/5)+1
                else: fr = 9
                if idp == mf[0] == mf[1] == mf[2] == mf[3]: fr = 0
                mFr += str(fr)
                fsum += fr
    if fsum < 35: log('Внимание! Пустое или почти пустое изображение: '+ sImg)
    return mFr

# Определение яркости для четверти
def eBr(img,bR,bT):
    pix = img.load() #Выгружаем значения пикселей.
    dx = 0; dy = 0
    if bR == True: dx = esize
    if bT == True: dy = esize
    s = 0
    for x in range(esize):
        for y in range(esize):
            a = pix[x+dx, y+dy][0]
            b = pix[x+dx, y+dy][1]
            c = pix[x+dx, y+dy][2]
            s += a + b + c
            idp = int((a + b + c)/(3*25.6))
            mp.append(idp)
    d = s / (esize*esize * 256*3)
    return d

# Определение соотношения сторон изображения
def eSize(w, h):
    if w <= h: return 1
    return 2

def eNier(d):
    iNier = -1
    i = int(d)
    if d-i < 0.1: iNier = i - 1
    if i+1-d < 0.1: iNier = i + 1
    if iNier > 9: iNier = 9
    return iNier

def Process(dirs):                     

    print('Загрузка данных...')
    # Работа с загрузкой данных
    for dr in dirs:
        imgs = [] # список всех изображений
        msave = {} # словарь для записи
        #Получаем список файлов в переменную files 
        # files = os.listdir(directory)
        for d, dirs, files in os.walk(dr):
            for f in files:
                f = f.lower()
                if f.endswith(('.jpg','.jpeg','.gif','.png','.bmp')):
                    imgs.append(d+'\\'+f)

        # работа с изображениями
        if len(imgs)>0:
            ip = 0
            log('--------------------------------------------------------------')
            log(dr)
            print('Найдено: '+str(len(imgs))+' изображений!')
            for jpg in imgs:
                try:
                    jpg = jpg.replace('/','\\')
                    imt = Image.open(jpg) #Открываем изображение. 
                    width = imt.size[0]   #Определяем ширину. 
                    height = imt.size[1]  #Определяем высоту.
                    if width < sz or height < sz :
                        log('Внимание пропуск! Подозрительные размеры изображения: '+str(width)+'x'+str(height)+' - '+jpg)
                        continue # пропускаем файл
                    # получение картинки 16x16
                    imt.thumbnail(size2, Image.NEAREST)
                    imt = imt.resize(size, Image.ANTIALIAS)
                    if jpg.endswith(('.gif','.png')):
                        imt.convert('RGB').save('temp.jpg', 'JPEG')
                        imt = Image.open('temp.jpg')
                    simg = ''; simgs = {}
                    #Ссоотношение сторон
                    simg += str(eSize(width,height))
                    if simg == '1':
                        dd = 10*((width-1)/height)**2
                        simg += str(int(dd))
                    else:
                        dd = 10*(height/width)**2
                        simg += str(int(dd))
                    if (eNier(dd)) >= 0: simgs['1'] = eNier(dd)
                    # Общая яркость
                    mp = [] # карта пикселей
                    d1 = eBr(imt,True,True)
                    d2 = eBr(imt,True,False)
                    d3 = eBr(imt,False,True)
                    d4 = eBr(imt,False,False)
                    dd = 10*(d1+d2+d3+d4)/4
                    simg += str(int(dd))
                    if (eNier(dd)) >= 0: simgs['2'] = eNier(dd)
                    # Разница яркости лево-право
                    dd = (d1+d3)/2 - (d2+d4)/2
                    if dd >= 0:
                        idd = 5 + int(5*sqrt(dd))
                        dd = 5 + 5*sqrt(dd)
                        simg += str(idd)
                    else:
                        idd = 5 - int(5*sqrt(-dd))
                        dd = 5 + 5*sqrt(-dd)
                        simg += str(idd)
                    if (eNier(dd)) >= 0: simgs['3'] = eNier(dd)
                    # Разница яркости низ-верх
                    dd = (d1+d2)/2 - (d3+d4)/2
                    if dd >= 0:
                        idd = 5 + int(5*sqrt(dd))
                        dd = 5 + 5*sqrt(dd)
                        simg += str(idd)
                    else:
                        idd = 5 - int(5*sqrt(-dd))
                        dd = 5 + 5*sqrt(-dd)
                        simg += str(idd)
                    if (eNier(dd)) >= 0: simgs['4'] = eNier(dd)
                    # Разница яркости по диагоналям
                    dd = (d1+d4)/2 - (d2+d3)/2
                    if dd >= 0:
                        idd = 5 + int(5*sqrt(dd))
                        dd = 5 + 5*sqrt(dd)
                        simg += str(idd)
                    else:
                        idd = 5 - int(5*sqrt(-dd))
                        dd = 5 + 5*sqrt(-dd)
                        simg += str(idd)
                    if (eNier(dd)) >= 0: simgs['5'] = eNier(dd)
                    #print(simg)
                    sImg = '"'+jpg+'", "'
                    sImg += eBrMap(imt)+'", 0'
                    if not simg in msave:
                        msave[simg] = []
                    msave[simg].append(sImg)
                    if len(simgs) > 0:
                        for k in simgs:
                            ss = simg
                            es = str(simgs[k])
                            ik = int(k)
                            ss = ss[0:ik]+es+ss[ik+1:]
                            if not ss in msave:
                                msave[ss] = []
                            msave[ss].append(sImg)
                    ip += 1        
                    if ip % 100 == 0: print('Обработано '+str(int(100*ip/len(imgs)))+'% ('+str(ip)+' из '+str(len(imgs))+')')
                except Exception as e:
                    log('! Ошибка в файле: ' + jpg + ' - ' + str(e))

        print('Загрузка завершена!')

        # запись всех данных
        for key in msave.keys():
            with open('data/'+key+'.txt','a', encoding='utf-8') as f:
                f.write('\n'.join(msave[key]) + '\n')
        print('Данные сохранены!')

    print('!!! Загрузка всех каталогов успешно завершена !!!')
