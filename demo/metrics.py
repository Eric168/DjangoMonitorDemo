import statsd
import time
import logging

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
    
    def timing_decorator(self, metric_name):
        """时间装饰器"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    duration = (time.time() - start_time) * 1000  # 转换为毫秒
                    self.timing(metric_name, duration)
                    return result
                except Exception as e:
                    duration = (time.time() - start_time) * 1000
                    self.timing(f'{metric_name}.error', duration)
                    raise
            return wrapper
        return decorator

# 创建全局MetricsClient实例
metrics = MetricsClient()
