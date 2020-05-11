from django.shortcuts import render

# Create your views here.
def detectFaces(request):
    return render(request,'admin/detectfaces.html')