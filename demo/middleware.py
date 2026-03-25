import time
from django.http import HttpRequest
from .metrics import metrics

class AdminStatsdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 只处理管理后台的请求
        if request.path.startswith('/admin/'):
            start_time = time.time()
            
            # 处理请求
            response = self.get_response(request)
            
            # 计算耗时
            duration = (time.time() - start_time) * 1000
            
            # 构建指标名称
            path = request.path.strip('/').replace('/', '.')
            method = request.method.lower()
            metric_prefix = f'admin.{path}'
            
            # 上报指标
            metrics.increment(f'{metric_prefix}.{method}')
            metrics.timing(f'{metric_prefix}.{method}.duration', duration)
            
            return response
        else:
            return self.get_response(request)