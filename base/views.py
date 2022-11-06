from django.shortcuts import get_object_or_404
from django.db.models import Q
from base.models import Advocate, Company
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializer import AdvocateSerializer, CompanySerializer


paginator = PageNumberPagination()
paginator.page_size = 20
# Create your views here
base_url = "https://cado-finder-api.herokuapp.com"
@api_view(['GET'])
def endpoints(request):
    data = [f"{base_url}/advocates", f"{base_url}/advocates/:username",f"{base_url}/advocates/search",f"{base_url}/companies", f"{base_url}/companies/:name"]
    return Response(data)

#Advocates
@api_view(['GET','POST'])
def advocate_list(request):
    if request.method == 'GET':
        advocates = Advocate.objects.all()
        result_page = paginator.paginate_queryset(advocates, request)
        serializer = AdvocateSerializer(result_page, many = True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        try:
            advocate = Advocate.objects.create(
                company = Company.objects.filter(name=request.data['company']).first(),
                name = request.data['name'],
                username = request.data['username'],
                bio = request.data['bio'],
                profile_pic = request.data['profile_pic'],
                twitter = request.data['twitter']   
            )
            serializer = AdvocateSerializer(advocate, many=False)
            return Response(serializer.data)
        except Exception as e:
            return Response(e)

@api_view(['GET'])
def advocate_search(request):
    query = request.GET.get('query')
    if query:
        advocates = Advocate.objects.filter(Q(username__icontains=query) | Q(bio__icontains=query))
        result_page = paginator.paginate_queryset(advocates, request)
        serializer = AdvocateSerializer(result_page, many = True)
        return paginator.get_paginated_response(serializer.data)
    else:
        return Response("query parameter missing")

@api_view(['GET', 'PUT','DELETE'])
def advocate_info(request, username):
    advocate = get_object_or_404(Advocate,username=username)
    if request.method == 'GET':
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
    if request.method == 'PUT':
        advocate.company = Company.objects.filter(name=request.data['company']).first()
        advocate.username = request.data['username']
        advocate.bio = request.data['bio']
        advocate.name = request.data['name']
        advocate.twitter = request.data['twitter']
        advocate.profile_pic = request.data['profile_pic']
        advocate.save()
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
    if request.method == 'DELETE':
        advocate.delete()
        return Response("user deleted")

# Companies
@api_view(['GET','POST'])
def company_list(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        result_page = paginator.paginate_queryset(companies, request)
        serializer = CompanySerializer(result_page, many = True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        company = Company.objects.create(
            name = request.data['name'],
            bio = request.data['bio'],
            profile_img = request.data['profile_img'],
            location = request.data['location'],
            url = request.data['url']
        )
        serializer = CompanySerializer(company, many=False)
        return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
def company_info(request,name):
    company = get_object_or_404(Company, name=name)
    if request.method == 'GET':
        serializer = CompanySerializer(company, many = False)
        return Response(serializer.data)
    if request.method == 'PUT':
        company.name = request.data['name']
        company.bio = request.data['bio']
        company.profile_img = request.data['profile_img']
        company.location = request.data['location']
        company.url = request.data['url']
        company.save()
        serializer = CompanySerializer(company, many =False)
        return Response(serializer.data)
    if request.method == 'DELETE':
        company.delete()
        return Response("Company Deleted")
    


    


