from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from .models import Item
from .metrics import metrics
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def item_list(request):
    start_time = time.time()
    if request.method == 'GET':
        try:
            items = Item.objects.all()
            data = [{'id': item.id, 'name': item.name, 'description': item.description, 'created_at': item.created_at, 'updated_at': item.updated_at} for item in items]
            logger.info('Retrieved all items')
            # 上报指标
            metrics.increment('items.list')
            metrics.timing('items.list.duration', (time.time() - start_time) * 1000)
            return JsonResponse({'items': data})
        except Exception as e:
            metrics.increment('items.list.error')
            metrics.timing('items.list.error.duration', (time.time() - start_time) * 1000)
            logger.error(f'Error retrieving items: {e}')
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            item = Item.objects.create(name=data['name'], description=data['description'])
            logger.info(f'Created item: {item.name}')
            # 上报指标
            metrics.increment('items.create')
            metrics.timing('items.create.duration', (time.time() - start_time) * 1000)
            return JsonResponse({'id': item.id, 'name': item.name, 'description': item.description, 'created_at': item.created_at, 'updated_at': item.updated_at})
        except Exception as e:
            metrics.increment('items.create.error')
            metrics.timing('items.create.error.duration', (time.time() - start_time) * 1000)
            logger.error(f'Error creating item: {e}')
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def item_detail(request, item_id):
    start_time = time.time()
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        metrics.increment('items.get.error')
        metrics.timing('items.get.error.duration', (time.time() - start_time) * 1000)
        logger.error(f'Item with id {item_id} not found')
        return JsonResponse({'error': 'Item not found'}, status=404)

    if request.method == 'GET':
        try:
            logger.info(f'Retrieved item: {item.name}')
            # 上报指标
            metrics.increment('items.get')
            metrics.timing('items.get.duration', (time.time() - start_time) * 1000)
            return JsonResponse({'id': item.id, 'name': item.name, 'description': item.description, 'created_at': item.created_at, 'updated_at': item.updated_at})
        except Exception as e:
            metrics.increment('items.get.error')
            metrics.timing('items.get.error.duration', (time.time() - start_time) * 1000)
            logger.error(f'Error retrieving item: {e}')
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            item.name = data.get('name', item.name)
            item.description = data.get('description', item.description)
            item.save()
            logger.info(f'Updated item: {item.name}')
            # 上报指标
            metrics.increment('items.update')
            metrics.timing('items.update.duration', (time.time() - start_time) * 1000)
            return JsonResponse({'id': item.id, 'name': item.name, 'description': item.description, 'created_at': item.created_at, 'updated_at': item.updated_at})
        except Exception as e:
            metrics.increment('items.update.error')
            metrics.timing('items.update.error.duration', (time.time() - start_time) * 1000)
            logger.error(f'Error updating item: {e}')
            return JsonResponse({'error': str(e)}, status=400)
    elif request.method == 'DELETE':
        try:
            item_name = item.name
            item.delete()
            logger.info(f'Deleted item: {item_name}')
            # 上报指标
            metrics.increment('items.delete')
            metrics.timing('items.delete.duration', (time.time() - start_time) * 1000)
            return JsonResponse({'message': 'Item deleted'})
        except Exception as e:
            metrics.increment('items.delete.error')
            metrics.timing('items.delete.error.duration', (time.time() - start_time) * 1000)
            logger.error(f'Error deleting item: {e}')
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def error_log(request):
    """Generate error level log for testing"""
    start_time = time.time()
    if request.method == 'GET':
        try:
            # Log an error message
            logger.error('This is a test error log message')
            # 上报指标
            metrics.increment('test.error_log')
            metrics.timing('test.error_log.duration', (time.time() - start_time) * 1000)
            return JsonResponse({'message': 'Error log generated successfully'})
        except Exception as e:
            metrics.increment('test.error_log.error')
            metrics.timing('test.error_log.error.duration', (time.time() - start_time) * 1000)
            logger.error(f'Error in error_log: {e}')
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def http_error_500(request):
    """Return 500 Internal Server Error for testing"""
    start_time = time.time()
    if request.method == 'GET':
        try:
            # Return 500 Internal Server Error
            logger.error('Returning 500 Internal Server Error for testing')
            # 上报指标
            metrics.increment('test.http_error.500')
            metrics.timing('test.http_error.500.duration', (time.time() - start_time) * 1000)
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
        except Exception as e:
            metrics.increment('test.http_error.500.error')
            metrics.timing('test.http_error.500.error.duration', (time.time() - start_time) * 1000)
            logger.error(f'Error in http_error_500: {e}')
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def http_error_404(request):
    """Return 404 Not Found for testing"""
    start_time = time.time()
    if request.method == 'GET':
        try:
            # Return 404 Not Found
            logger.error('Returning 404 Not Found for testing')
            # 上报指标
            metrics.increment('test.http_error.404')
            metrics.timing('test.http_error.404.duration', (time.time() - start_time) * 1000)
            return JsonResponse({'error': 'Not Found'}, status=404)
        except Exception as e:
            metrics.increment('test.http_error.404.error')
            metrics.timing('test.http_error.404.error.duration', (time.time() - start_time) * 1000)
            logger.error(f'Error in http_error_404: {e}')
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def health_check(request):
    """Health check endpoint for monitoring"""
    start_time = time.time()
    if request.method == 'GET':
        try:
            logger.info('Health check requested')
            # 上报指标
            metrics.increment('health.check')
            metrics.timing('health.check.duration', (time.time() - start_time) * 1000)
            return HttpResponse('OK')
        except Exception as e:
            metrics.increment('health.check.error')
            metrics.timing('health.check.error.duration', (time.time() - start_time) * 1000)
            logger.error(f'Error in health_check: {e}')
            return HttpResponse('ERROR', status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
