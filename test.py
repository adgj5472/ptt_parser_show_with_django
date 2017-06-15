#----------------------------------------------------------------------
#import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloud.settings")
#import django
#django.setup()
#python外部腳本連接django model---------------------------------------

#from img.models import img



#img_list =img.objects.all()
#print(img_list[0].photo)
#get=img.objects.get(pk=2)
#print(get.photo)

#img_seq=[]
#img_list =img.objects.all()
#for i in range(len(img_list)-1,0,-1):
#    img_seq.append(img_list[i])
#    print(i)
#print(img_seq)
import sqlite3

def show(user):
    print(user[0])
    


conn=sqlite3.connect('db.sqlite3')
cursor=conn.cursor()
cursor.execute('select distinct username from img_ig_img')
values= cursor.fetchall()
print(values)

for user in values:
    show(user)
