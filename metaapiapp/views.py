from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import requests
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework import status
from .models import *
from .serializers import *
import pandas as pd
import json

# Create your views here.

@csrf_exempt
def post_on_fb_screen(request):
    print(request.method)
    return  render(request,'fb_post.html')


@csrf_exempt
def get_post_on_fb_screen(request):
    print(request.method)
    return  render(request,'get_fb_post.html')


class FBpost(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        data = request.data
        page_id = '122949824076754'
        url = 'https://graph.facebook.com/v19.0/{}/feed'.format(page_id)
        payload = {
            'message':data.get('message'),
            'is_published':data.get('is_published'),
            'link':data.get('link'),
            "scheduled_publish_time":data.get('scheduled_publish_time'),
            'access_token':'EAAGbWZBZBTqmwBOw2wLwGKZCC0E0ZAoxoJvc9mJXG1arTwM8a95py2AQ1ZC9qaOQWn5eAErHksNhew9pEH0ntrkZA85woYGqlNBJB4bFyaz6zbxK8CaadDLDJTBUAo0abZCxlymXP1rz33C1ruhZApcIBc0VI82HBPaerNKBcDGUWeZBac86HeIDc5YLVpjRaEjkrMO3ZAtoDyjZBIt5wUZD'
        }
        keys_to_remove = [key for key,value in payload.items() if value is None]
        for key in keys_to_remove:
            del payload[key]
        response = requests.post(url, data=payload)
        response_data = response.json()
        print(response_data,"sjfhbdrshj")
        if 'error' in response_data:
            print(response_data['error']['message'])
            return JsonResponse({'message':response_data['error']['message']})
        else:
            save_log = pagePost(page_post_id=response_data['id'])
            save_log.save()
            return JsonResponse({'message':"Posted Successfully"})
        

class GetFBpost(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        page_id = request.data.get('page_id','122949824076754') 
        url = 'https://graph.facebook.com/v19.0/{}/feed'.format(page_id)
        payload = {
            'access_token':'EAAGbWZBZBTqmwBOw2wLwGKZCC0E0ZAoxoJvc9mJXG1arTwM8a95py2AQ1ZC9qaOQWn5eAErHksNhew9pEH0ntrkZA85woYGqlNBJB4bFyaz6zbxK8CaadDLDJTBUAo0abZCxlymXP1rz33C1ruhZApcIBc0VI82HBPaerNKBcDGUWeZBac86HeIDc5YLVpjRaEjkrMO3ZAtoDyjZBIt5wUZD'
        }
        keys_to_remove = [key for key,value in data.items() if value is None]
      
        response = requests.get(url, params=payload)
        response_data = response.json()
        if 'error' in response_data:
            print(response_data['error']['message'])
            return JsonResponse({'message':response_data['error']['message']})
        else:
            serializer = PagePostSerializer(pagePost.objects.all(),many=True)
            serializer_df =  pd.DataFrame(serializer.data)
            df = pd.DataFrame(response_data['data'])
            main_df = df.merge(serializer_df, how='inner',left_on=['id'],right_on=['page_post_id'])
            main_df['story'] = main_df['story'].astype(str)
            print(main_df)
            data_ = main_df.to_dict(orient='records')
            # temp_str = str(data_).replace("'",'"')
            # temp_str = temp_str.replace("'",'"')
            print(str(data_).replace("'",'"'))
            res = json.loads(str(data_).replace("'",'"'))
            # print(res,type(res))
            print(res)
            return JsonResponse({'data':res})


class GetPostInsights(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        page_post_id =  request.data.get('page_post_id','122949824076754_338188559239017')  
        url = 'https://graph.facebook.com/{}/insights'.format(page_post_id)
        payload = {
            'access_token':'EAAGbWZBZBTqmwBOw2wLwGKZCC0E0ZAoxoJvc9mJXG1arTwM8a95py2AQ1ZC9qaOQWn5eAErHksNhew9pEH0ntrkZA85woYGqlNBJB4bFyaz6zbxK8CaadDLDJTBUAo0abZCxlymXP1rz33C1ruhZApcIBc0VI82HBPaerNKBcDGUWeZBac86HeIDc5YLVpjRaEjkrMO3ZAtoDyjZBIt5wUZD',
            'metric':'post_reactions_by_type_total'
        }
     
        response = requests.get(url, params=payload)
        response_data = response.json()
        print(response_data,"sjfhbdrshj")
        likes = 0
        if 'error' in response_data:
            print(response_data['error']['message'])
            return JsonResponse({'message':response_data['error']['message']})
        else:
            for dict_value in response_data['data']:
                print(dict_value,"dhsbcsjc")
                if dict_value['name'] == 'post_reactions_by_type_total':
                    likes = dict_value['values'][0]['value']
            
            print(likes,"jhvbdh")
            page_post = pagePost.objects.filter(page_post_id=page_post_id)
            if len(page_post)>0:
                page_post[0].likes_count = likes['like']
                page_post[0].save()

            return JsonResponse(response_data)



class GetPostComments(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        page_post_id =  request.data.get('page_post_id','122949824076754_338188559239017')
        url = 'https://graph.facebook.com/{}/comments?fields=from,message'.format(page_post_id)
      
        payload = {
            'access_token':'EAAGbWZBZBTqmwBOw2wLwGKZCC0E0ZAoxoJvc9mJXG1arTwM8a95py2AQ1ZC9qaOQWn5eAErHksNhew9pEH0ntrkZA85woYGqlNBJB4bFyaz6zbxK8CaadDLDJTBUAo0abZCxlymXP1rz33C1ruhZApcIBc0VI82HBPaerNKBcDGUWeZBac86HeIDc5YLVpjRaEjkrMO3ZAtoDyjZBIt5wUZD',
            
        }
        response = requests.get(url, params=payload)
        response_data = response.json()
        print(response_data,"sjfhbdrshj")
        comments = 0
        if 'error' in response_data:
            print(response_data['error']['message'])
            return JsonResponse({'message':response_data['error']['message']})
        else:
            comments = len(response_data['data'])
            page_post = pagePost.objects.filter(page_post_id=page_post_id)
            if len(page_post)>0:
                page_post[0].comments_count = comments
                page_post[0].save()

            return JsonResponse(response_data)