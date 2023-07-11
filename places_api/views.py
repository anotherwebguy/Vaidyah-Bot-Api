from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from dotenv import dotenv_values
import requests
from urllib.parse import urlencode

env_vars = dotenv_values(".env")
api_key = env_vars['PLACES_API_KEY']

# Create your views here.

@api_view(['GET'])
def getNearbyHospitals(request):
    try:
        val = request.GET.get('val')
        print(val)
        lat,long = val.split(' , ')
        print(lat,long)
        url = "https://api.foursquare.com/v3/places/search"
        params = {
            "query": "hospital",
            "ll": lat+","+long,
            "open_now": "true",
            "sort": "DISTANCE"
        }
        headers = {
            "Accept": "application/json",
            "Authorization": api_key
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            res = response.json()
            print(res)
            names = [item['name'] for item in res['results']]
            images = [item['categories'][0]['icon']['prefix'] + 'bg_64' + item['categories'][0]['icon']['suffix'] for item in res['results']]
            addresses = [item['location']['formatted_address'] for item in res['results']]
            locations = []
            for result in res["results"]:
                latitude = result["geocodes"]["main"]["latitude"]
                longitude = result["geocodes"]["main"]["longitude"]
                locations.append((latitude, longitude))
            urls = []
            for lat, lng in locations:
                url = f"https://www.google.com/maps/search/?{urlencode({'api': 1, 'query': f'{lat},{lng}'})}"
                urls.append(url)
            return Response({'names':names,'images':images,'addresses':addresses,'urls':urls})
        else:
            print("Error:", response.status_code)
            return Response("Can't recognize your location. Please try again.")
    except:
        return Response("Something went wrong. Please try again later.")