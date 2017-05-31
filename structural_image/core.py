# -*- coding: utf-8 -*-
"""
Created on Wed May 17 01:35:45 2017

@author: Alexander Sovetsky
"""
t = time.time()

import matplotlib as mpl
import pylab
import math 
import scipy
import numpy as np
import array
import os
import matplotlib.pyplot as plt
import math, time

#Каталог из которого будем брать файлы
directory = 'F:/example/'
def wayfunc(direct):
    #Получаем список файлов в переменную files
    files = os.listdir(direct)
    #Фильтруем список по расширению
    datfile = list(filter(lambda x: x.endswith('.dat'), files))
    return datfile

filename=wayfunc(directory)

#Берём первый файл, потом можно будет все по очереди читать.
filename=''.join(filename[0])
name=directory+filename
#Открываем первый файл   
with open(name,'rb') as f:
 dat=np.fromfile(f,dtype=np.ushort)
#Задаём параметра одного В-скана    
datspectral=512#.astype(int)
datAscans=1024
#Определяем количество кадров(В-сканов)
def sizefunc(name,datspectral,datAscans):
    size=os.stat(name).st_size
    frames=int(size/(datspectral*datAscans*2))#2байта-одно значение
    return frames
frames=sizefunc(name,datspectral,datAscans)
#Изменяем форму массива: из строки в 3D-массив
m=np.reshape(np.ravel(dat),(datspectral,datAscans,frames), order='F')
#Задаём и получаем структурные изображения из спектров B-сканов
def getstruct(m,datspectral,datAscans,frames):
   structure1=np.ndarray(shape=(datspectral,datAscans/4,frames),dtype=np.complex)#complex64
   k=np.ndarray(shape=(datspectral,datAscans/4,frames),dtype=np.complex)
   for n in range(0,frames):
      k[:,:,n]=-1j*m[:,1::4,n]+1j*m[:,3::4,n]+m[:,3::4,n]+m[:,1::4,n]-2*m[:,2::4,n]
      structure1[:,:,n]=np.fft.ifft2(k[:,:,n],s=None, axes=(-2, -1),norm='ortho')#-2,-1 np.fft.ifft2
   structure=np.double(20*(np.log10(np.abs(structure1))))
   return structure
structure=getstruct(m,datspectral,datAscans,frames)
#Строим структурные изображения
fig = plt.figure(figsize=(12,4))
bounds = np.linspace(np.min(structure), np.max(structure), 30)
cmap = mpl.cm.get_cmap('hot',20)#'YlOrRd',20)#'Reds',7)#'YlOrBr',7)#'hot',7)#'brg_r',7)#'Set1',7)#'Wistia_r',7)#'coolwarm',7)#'Spectral',7)#'summer',7)#'Set2',7)#'jet',7)#'RdBu', 7)
ax = fig.add_axes([0, 0, 1, 1])
cf=plt.imshow(structure[0:255,0:127,56], cmap=cmap, vmin=5,vmax=40)#20*math.log10
plt.colorbar(cf,ax=ax)#ticks=bounds, extend='max', extendfrac=100)
plt.xlabel('width / px')
plt.ylabel('depth / px')
plt.axis('normal')
plt.title('Structure OCT image')

#ПРОБОВАЛ СОЗДАТЬ ВИДЕО ИЗ КАДРОВ
#for m in range(0,frames):
#img1 = cv2.imread(structure(:,:,m))
#video = cv2.VideoWriter('video.avi',-1,1,(width,height))
#for m in range(0,frames):
#     video.write(structure[:,:,m])

#cv2.destroyAllWindows()
#video.release()
 #ПРОБОВАЛ СОЗДАТЬ ВИДЕО ИЗ КАДРОВ   
#import subprocess as subp
#from os.path import join
#
#log_dir = directory#'' # путь куда положить файл с записью
#CORE_DIR = 'F:\\' # путь где лежит ffmpeg.exe
#video_file = join(log_dir, 'video_' + files[0] + '.flv')
#FFMPEG_BIN = join(CORE_DIR, 'ffmpeg-20170520-64ea4d1-win64-static\\bin\\ffmpeg.exe')
#
#command = [
#    FFMPEG_BIN,
#    '-y',
#    '-loglevel', 'error',
#    '-f', 'gdigrab',
#    '-framerate', '12',
#    '-i', 'desktop',
#    '-s', '960x540',
#    '-pix_fmt', 'yuv420p',
#    '-c:v', 'libx264',
#    '-profile:v', 'main',
#    '-fs', '50M',
#    video_file]
#ffmpeg = subp.Popen(command, stdin=subp.PIPE, stdout=subp.PIPE, stderr=subp.PIPE)
#ИДЁТ ЗАПИСЬ ПРИнТСКРИНОВ СО ВСЕГО ЭКРАНА
#ffmpeg.stdin.write("q")
#ffmpeg.stdin.close()


def test():
   assert(wayfunc('F:/example/test')[0] == '1_elasto_liver_load.dat')
test()
def test2():
   assert(sizefunc(name,datspectral,datAscans)==512)
test2()

elapsed = time.time() - t
print("Elapsed time: {:.3f} sec".format(elapsed))
