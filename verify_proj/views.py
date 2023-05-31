from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate , login
from codes.forms import CodeForm
from users.models import CustomUser
from .utils import send_sms, generate_otp, verify_otp

@login_required
def home_view(request):
    return render(request, 'main.html',{})

#chế độ xem xác thực
def auth_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            request.session['pk'] = user.pk
            return redirect('verify-view')
    return render(request, 'auth.html', {'form': form})

#chế độ xem xác minh
def verify_view(request):
    #khởi tạo biểu mẫu , chuyển vào bài đăng yêu cầu hoặc không
    form = CodeForm(request.POST or None)
    pk =  request.session.get('pk')
    if pk:
        #lấy tất csr các quyền của người dùng
        user = CustomUser.objects.get(pk =pk)
        #mã người dùng 
        code = user.code 
        #đặt vào tên người dùng và mã code , nội dung gửi cùng vs sms
        code_user = f"{user.username}: {user.code}"
        if not request.POST:
            #truy cập in ra người dùng mã 
            generate_otp(user.phone_number)
        if form.is_valid():
            #lấy số từ form, so với form
            num = form.cleaned_data.get('number')

            #so sánh mã ở trên có khớp với mã đã nhập hay k
            if(verify_otp(num, user.phone_number) == "approved"):
                code.save()
                login(request, user)
                return redirect('home-view')
            else:
                return redirect('login-view')
    return render(request, 'verify.html', {'form': form})
