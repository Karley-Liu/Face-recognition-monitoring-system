from django.shortcuts import render

# Create your views here.
def bookviews(request):
    return render(request,'admin/admin_index2.html')