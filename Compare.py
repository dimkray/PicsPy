import os
import math

print('Загрузка данных...')

# Работа с загрузкой данных
#Получаем список файлов в переменную files
files = os.listdir('data')
ff = 0
for fl in files:
    try:
        if fl.endswith('.txt'):
            dmin = 3000000
            dmax = 0
            imgs = [] # список всех изображений
            gr = []   # список групп изображений
            with open('data/' + fl, 'r', encoding='utf-8') as f:
                print('Обработка: ' + str(int(100*ff/len(files))) + '%')
                for line in f:
                    m = []
                    poz = line.find('",')
                    m.append(line[1:poz]) # [0] - путь-имя файла
                    poz2 = line.find('",', poz+1)
                    ss = line[poz+4:poz2]
                    m.append(ss)          # [1] - карта направлений-силы яркости (14х14)
                    m.append(int(line[poz2+3:])) # [2] - признак обработки информации: 1 - обработано, 0 - не обработано
                    i = 0
                    for s in ss:
                        i += int(s)
                    if i > dmax: dmax = i
                    if i < dmin: dmin = i
                    m.append(i)
                    imgs.append(m)  # [3] - индекс общей силы-яркости (для группировки по силе-яркости)
            print(dmin)
            print(dmax)

            # Этап группировки для ускорения процесса сравнения
            if len(imgs) > 100:
                dd = (dmax-dmin)/20
                gr = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
                for img in imgs:
                    i = int((img[3]-dmin)/dd)
                    gr[i].append(img)
                    if img[3]%dd > dd*3/4: gr[i+1].append(img)
                    if img[3]%dd < dd/4 and i > 0: gr[i-1].append(img)
            else:
                gr = [[]]
                for img in imgs:
                    gr[0].append(img)
                
            # Этап сравнения
            mco = []
            for igr in gr:
                x = 0
                for img in igr:
                    for i in range(x+1, len(igr)):
                        if img[2] == False or igr[i][2] == False:
                            if abs(img[3] - igr[i][3]) < 200:
                                j = 0; d = 0
                                for s in img[1]:
                                    d += abs(int(s) - int(igr[i][1][j]))
                                    j += 1
                                if d < 300:
                                    m = []
                                    m.append(img[0])
                                    m.append(igr[i][0])
                                    m.append(d)
                                    mco.append(m)
                                    print(m)
                    x += 1
            # запись всех данных
            if len(mco) > 0 :
                with open('Compares.cmr','a') as f:
                    for co in mco:
                        f.write('"' + co[0] + '","' + co[1] + '",' + str(100*co[2]/1760) + ','+ str(co[2]) + '\n')
            # запись изменённых данных
            with open('data/' + fl, 'w', encoding='utf-8') as f:
                for img in imgs:
                    f.write('"'+img[0]+'", "'+img[1]+'", 1\n')
        ff += 1
    except Exception as e:
        print('Ошибка: ' + str(e))

print('Данные сохранены!')
