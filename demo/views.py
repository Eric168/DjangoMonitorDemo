from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from .models import Item
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def item_list(request):
    if request.method == 'GET':
        items = Item.objects.all()
        data = [{'id': item.id, 'name': item.name, 'description': item.description, 'created_at': item.created_at, 'updated_at': item.updated_at} for item in items]
        logger.info('Retrieved all items')
        return JsonResponse({'items': data})
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            item = Item.objects.create(name=data['name'], description=data['description'])
            logger.info(f'Created item: {item.name}')
            return JsonResponse({'id': item.id, 'name': item.name, 'description': item.description, 'created_at': item.created_at, 'updated_at': item.updated_at})
        except Exception as e:
            logger.error(f'Error creating item: {e}')
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def item_detail(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        logger.error(f'Item with id {item_id} not found')
        return JsonResponse({'error': 'Item not found'}, status=404)

    if request.method == 'GET':
        logger.info(f'Retrieved item: {item.name}')
        return JsonResponse({'id': item.id, 'name': item.name, 'description': item.description, 'created_at': item.created_at, 'updated_at': item.updated_at})
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            item.name = data.get('name', item.name)
            item.description = data.get('description', item.description)
            item.save()
            logger.info(f'Updated item: {item.name}')
            return JsonResponse({'id': item.id, 'name': item.name, 'description': item.description, 'created_at': item.created_at, 'updated_at': item.updated_at})
        except Exception as e:
            logger.error(f'Error updating item: {e}')
            return JsonResponse({'error': str(e)}, status=400)
    elif request.method == 'DELETE':
        item.delete()
        logger.info(f'Deleted item: {item.name}')
        return JsonResponse({'message': 'Item deleted'})

@csrf_exempt
def error_log(request):
    """Generate error level log for testing"""
    if request.method == 'GET':
        # Log an error message
        logger.error('This is a test error log message')
        return JsonResponse({'message': 'Error log generated successfully'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def http_error_500(request):
    """Return 500 Internal Server Error for testing"""
    if request.method == 'GET':
        # Return 500 Internal Server Error
        logger.error('Returning 500 Internal Server Error for testing')
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def http_error_404(request):
    """Return 404 Not Found for testing"""
    if request.method == 'GET':
        # Return 404 Not Found
        logger.error('Returning 404 Not Found for testing')
        return JsonResponse({'error': 'Not Found'}, status=404)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def health_check(request):
    """Health check endpoint for monitoring"""
    if request.method == 'GET':
        logger.info('Health check requested')
        return HttpResponse('OK')
    return JsonResponse({'error': 'Method not allowed'}, status=405)
