from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
from django.http import HttpResponse, HttpRequest, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control, never_cache
from django.views.decorators.http import require_http_methods
import json

@cache_control (
    private=True,
    max_age = 180 * 60, #6 часов
    no_cache = True,
    no_site = False
)
def Quote_list(request: HttpRequest):
    if request.method == 'GET':
        quotes = Quote.objects.all()
        quotes_list = []
        for quote in quotes:
            tags = quote.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
            quotes_list.append(prepare_data(quote, tags_list))
        return JsonResponse(quotes_list, safe=False)

@cache_control(
    private=True,
    max_age=180 * 60,  # 6 часов
    no_cache=True,
    no_site=False
)
@csrf_exempt
@require_http_methods(["GET", "POST"])
def Quote_list_create(request: HttpRequest):
    if request.method == 'GET':
        quotes = Quote.objects.all()
        quotes_list = []
        for quote in quotes:
            tags = quote.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
            quotes_list.append(prepare_data(quote, tags_list))
        return JsonResponse(quotes_list, safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        quote = Quote.objects.create(
            quote=data['quote'],
            author=data['author']
        )
        if 'tags' in data:
            tags = Tag.objects.filter(id__in=data['tags'])
            quote.tag.set(tags)
        
        tags = quote.tag.all()
        tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
        response_data = prepare_data(quote, tags_list)
        response_data['_links'] = {
            'self': {
                'type': 'GET',
                'url': f'{request.build_absolute_uri("/")}Quotes/{quote.id}/'
            }
        }
        return JsonResponse(response_data, status=201)

@cache_control(
    private=True,
    max_age=720 * 60,  
    no_cache=False,
    no_site=False
)
@csrf_exempt
@require_http_methods(["GET", "DELETE", "PATCH"])
def Quote_detail_delete_update(request: HttpRequest, quote_id: int):
    try:
        quote = Quote.objects.get(id=quote_id)
    except Quote.DoesNotExist:
        return JsonResponse({"error": "Quote not found"}, status=404)
    
    if request.method == 'GET':
        tags = quote.tag.all()
        tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
        quote_dict = prepare_data(quote, tags_list)
        return JsonResponse(quote_dict)
    
    elif request.method == 'DELETE':
        quote.delete()
        return JsonResponse({"message": "Quote deleted successfully"}, status=204)
    
    elif request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            
            if 'quote' in data:
                quote.quote = data['quote']
            if 'author' in data:
                quote.author = data['author']
            
            if 'tags' in data:
                tags = Tag.objects.filter(id__in=data['tags'])
                quote.tag.set(tags)
            
            quote.save()
            
            tags = quote.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
            response_data = prepare_data(quote, tags_list)
            
            return JsonResponse(response_data)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@cache_control(
    private=True,
    max_age=43200 * 60,  # месяц
    no_cache=False,
    no_site=False
)
@csrf_exempt
@require_http_methods(["GET", "DELETE", "PATCH"])
def tag_detail_delete_update(request: HttpRequest, tag_id: int):
    try:
        tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        return JsonResponse({"error": "Tag not found"}, status=404)
    
    if request.method == 'GET':
        tag_dict = {
            "id": tag.id,
            "name": tag.name
        }
        return JsonResponse(tag_dict)
    
    elif request.method == 'DELETE':
        tag.delete()
        return JsonResponse({"message": "Tag deleted successfully"}, status=204)
    
    elif request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            
            if 'name' in data:
                tag.name = data['name']
                tag.save()
            
            return JsonResponse({
                "id": tag.id,
                "name": tag.name
            })
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@cache_control(
    private=True,
    max_age=1440 * 60,  # 24 часа
    no_cache=True,
    no_site=False
)
@csrf_exempt
@require_http_methods(["GET", "POST"])
def tag_list_create(request: HttpRequest):
    if request.method == 'GET':
        tags = Tag.objects.all()
        tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
        return JsonResponse(tags_list, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            if not data.get('name'):
                return JsonResponse({"error": "Name field is required"}, status=400)
                
            tag = Tag.objects.create(name=data['name'])
            
            response_data = {
                "id": tag.id,
                "name": tag.name,
                "_links": {
                    'self': {
                        'type': 'GET',
                        'url': f'{request.build_absolute_uri("/")}tags/{tag.id}/'
                    }
                }
            }
            return JsonResponse(response_data, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@cache_control (
    private=True,
    max_age = 720 * 60, #12 часов
    no_cache = True,
    no_site = False
)
def Quote_via_tag_id(request: HttpRequest, tag_id: int):
    if request.method == 'GET':
        quotes = Quote.objects.filter(tag=tag_id)
        quotes_list = []
        for quote in quotes:
            tags = quote.tag.all()
            tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
            quotes_list.append(prepare_data(quote, tags_list))

        return JsonResponse(quotes_list, safe=False)


def prepare_data(quote_data: Quote, tag_data: list[Tag]):
    quote_dict = {
        "id": quote_data.id,
        "quote": quote_data.quote,
        "author": quote_data.author,
        "tags": tag_data
    }
    return quote_dict

@cache_control(
    private=True,
    max_age=60,  # 1 minute - short cache since it's random
    no_cache=True,
    no_site=False
)
def quote_random(request: HttpRequest):
    if request.method == 'GET':
        quotes = Quote.objects.all()
        if not quotes.exists():
            return JsonResponse({"error": "No quotes available"}, status=404)
        random_quote = quotes.order_by('?').first()
        tags = random_quote.tag.all()
        tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
        response_data = prepare_data(random_quote, tags_list)
        
        return JsonResponse(response_data)