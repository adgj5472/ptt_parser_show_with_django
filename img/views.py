from django.shortcuts import render
from django.http import HttpResponse
from img.models import img,ig_img
from cloud import settings

#----爬蟲
import sys
sys.path.append("../")
from new_ig_parser import parser,little
#driver = webdriver.Chrome(executable_path=r'chromedriver.exe') # chrome瀏覽器
#driver = webdriver.PhantomJS(executable_path='phantomjs.exe')  # PhantomJs
#----

from django.shortcuts import render_to_response #創建模板到填寫模板到回應的動作

# Create your views here.
def index(request):
    return render(request,'index.html')
def ig_search(request):
    if 'username' in request.GET:
        user=request.GET['username']
        exist=ig_img.objects.filter(username=user)
        if not exist:
            little(user)
            #driver.close()  # 關閉瀏覽器
            #driver.quit()   # 結束全部視窗
            img_list = ig_img.objects.filter(username=user)
            images_list=[]
            for i in range(len(img_list) - 1, 0, -1):
                images_list.append(img_list[i])
            return render(request,'ig_show.html',{'images':images_list,'username':user})
            #return HttpResponse('downloaded'+user)
        else:
            img_list = ig_img.objects.filter(username=user)

            images_list=[]
            for i in range(len(img_list) - 1, 0, -1):
                images_list.append(img_list[i])
            return render(request,'ig_show.html',{'images':images_list ,'username':user})
            #return HttpResponse('Welcome!~'+user)
    else:
        return render_to_response('ig_search.html',locals())


def ptt(request):
    img_list =img.objects.all()
    images_list=[]
    for i in range(len(img_list) - 1, 0, -1):
        images_list.append(img_list[i])
    return render(request,'ptt.html',{'images':images_list})
