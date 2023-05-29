from django.shortcuts import render, get_object_or_404 , redirect
from .models import PutUserInfo, Petition, StaticData
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login # 아이디, 비밀번호 일치 여부
from .train import predict_result
from django.contrib import messages

def index(request):
    return render(request, 'boards/index.html')

def start(request):
    return render(request, 'boards/signin.html')

def tologin(request):
    inputusername = request.POST.get('username')
    inputpassword = request.POST.get('password')
    namecheck = PutUserInfo.objects.filter(username=inputusername, password=inputpassword)
    if namecheck:
        return render(request, 'boards/register.html')
    else:
        messages.error(request, '로그인에 실패하였습니다.')
        return render(request, 'boards/signin.html', {'login_failed':True})

def gotosignup(request):
    return render(request, 'boards/signup.html')

def signup(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    
    if username and password and email:
        info = PutUserInfo(username=username, password=password, email=email)
        info.save()
        return render(request, 'boards/register.html',{'signup_compelete':True})
    
    else:
        messages.error(request, '양식을 모두 채워주세요.')
        return render(request, 'boards/signup.html', {'signup_failed':True})

def texttodb(request):
    category = request.POST.get('category')
    title = request.POST.get('title')
    content = request.POST.get('content')

    if category and title and content:
        ouputcontent = StaticData.objects.get(s_categorynum=category)
        result = predict_result(content)
        # result = {'name':"Transformer_KOREAN", 'score':50}
        num = result['score']
        info = Petition(category=category, title = title, content=content, percent = num)
        info.save()
        context = {'result':result, 'ouput':ouputcontent}
        return render(request, 'boards/output.html', context)
    else:
        messages.error(request,'내용을 입력하세요.')
        return render(request, 'boards/register.html', {'write_failed': True})
    
def returntoregister(request):
    return render(request, 'boards/register.html')

def register(request):
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('register')
        else:
            # 로그인 실패 처리
            pass
    else:
        # GET 요청 처리
        pass

def registertotable(request):
    board_all = Petition.objects.order_by('-pk')
    context = {'boards':board_all}
    return render(request, 'boards/table_register.html', context)


def detail(request,pk):
    board = Petition.objects.get(pk=pk)
   
    context = {
        'board':board
    }

    return render(request, "boards/table_detail.html", context)
