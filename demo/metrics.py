import statsd
import time
import logging
from functools import wraps
from django.http import HttpRequest

logger = logging.getLogger(__name__)

# 初始化StatsD客户端
class MetricsClient:
    def __init__(self):
        try:
            self.client = statsd.StatsClient(host='localhost', port=8125, prefix='django.demo')
            self.initialized = True
            logger.info('StatsD client initialized successfully')
        except Exception as e:
            self.client = None
            self.initialized = False
            logger.warning(f'Failed to initialize StatsD client: {e}')
    
    def increment(self, metric_name, value=1, tags=None):
        """增加计数器指标"""
        if self.initialized:
            try:
                self.client.incr(metric_name, value)
            except Exception as e:
                logger.warning(f'Failed to increment metric {metric_name}: {e}')
    
    def gauge(self, metric_name, value, tags=None):
        """设置 gauge 指标"""
        if self.initialized:
            try:
                self.client.gauge(metric_name, value)
            except Exception as e:
                logger.warning(f'Failed to set gauge metric {metric_name}: {e}')
    
    def timing(self, metric_name, value, tags=None):
        """记录时间指标"""
        if self.initialized:
            try:
                self.client.timing(metric_name, value)
            except Exception as e:
                logger.warning(f'Failed to record timing metric {metric_name}: {e}')
    
    def api_metrics(self, metric_prefix):
        """API接口指标装饰器"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                request = None
                
                # 从参数中获取request对象
                for arg in args:
                    if isinstance(arg, HttpRequest):
                        request = arg
                        break
                
                # 构建指标名称
                method = request.method.lower() if request else 'unknown'
                metric_base = f'{metric_prefix}.{method}'
                
                try:
                    # 执行原函数
                    result = func(*args, **kwargs)
                    
                    # 计算耗时
                    duration = (time.time() - start_time) * 1000
                    
                    # 上报成功指标
                    self.increment(metric_base)
                    self.timing(f'{metric_base}.duration', duration)
                    
                    return result
                except Exception as e:
                    # 计算错误耗时
                    duration = (time.time() - start_time) * 1000
                    
                    # 上报错误指标
                    self.increment(f'{metric_base}.error')
                    self.timing(f'{metric_base}.error.duration', duration)
                    
                    # 重新抛出异常
                    raise
            return wrapper
        return decorator
    
    def admin_metrics(self, metric_prefix):
        """管理后台指标装饰器"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                request = None
                
                # 从参数中获取request对象
                for arg in args:
                    if isinstance(arg, HttpRequest):
                        request = arg
                        break
                
                # 构建指标名称
                method = request.method.lower() if request else 'unknown'
                metric_base = f'admin.{metric_prefix}.{method}'
                
                try:
                    # 执行原函数
                    result = func(*args, **kwargs)
                    
                    # 计算耗时
                    duration = (time.time() - start_time) * 1000
                    
                    # 上报成功指标
                    self.increment(metric_base)
                    self.timing(f'{metric_base}.duration', duration)
                    
                    return result
                except Exception as e:
                    # 计算错误耗时
                    duration = (time.time() - start_time) * 1000
                    
                    # 上报错误指标
                    self.increment(f'{metric_base}.error')
                    self.timing(f'{metric_base}.error.duration', duration)
                    
                    # 重新抛出异常
                    raise
            return wrapper
        return decorator

# 创建全局MetricsClient实例
metrics = MetricsClient()

