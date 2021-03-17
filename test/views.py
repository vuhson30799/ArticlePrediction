from django.shortcuts import render
from test.backend.services import predict_from_urls
import time


def index(request):
    return render(request, 'test/index.html')


def check(request):
    start = time.perf_counter()
    result_list = predict_from_urls(request.GET.get('urls'))
    end = time.perf_counter()
    print(f"Proceed in {end - start:0.4f} seconds")
    context = {'result_list' : result_list}
    return render(request, 'test/index.html', context)

