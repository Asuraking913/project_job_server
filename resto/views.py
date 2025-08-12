from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import ApplicationSerializer, JobApplySerializer, JobSerializer, ProductSerializer, OrderItemsSerializer, UserProfileSerializer
from .models import Apply, Product, OrderItem, Order, Profile, User, Job
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
import json
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.pagination import PageNumberPagination


# Create your views here.
def Home(request):
    return HttpResponse("<h1>This is the home age</h1>")


class GetUserInformationView(APIView):

    def get(self, request):
        user_id = request.query_params.get('id')
        user = User.objects.get(id = user_id)

        if user:

            try:

                profile = Profile.objects.get(user = user)


            except Exception as e:

                profile = Profile(user = user)
                print('Intiated')
                profile.save()

    
            response = {
                'id' : user.id,
                'first_name' : user.first_name if user.first_name else "",
                'last_name' : user.last_name if user.last_name else "",
                'phone_number' : user.phone_number if user.phone_number else "",
                'location' : user.address_default if user.address_default else "",
                'email' : user.email if user.email else "",
                'job_title' : profile.job_title if profile.job_title else "",
                'experience' : profile.experience if profile.experience else "",
                'hourly_rate' : profile.hourly_rate if profile.hourly_rate else "",
                'languages' : profile.languages if profile.languages else "",
                'bio' : profile.bio if profile.bio else "", 
                'skills' : profile.skills if profile.skills else "",
                'education' : profile.education if profile.education else "",
                'website_link' : profile.website_link if profile.website_link else "",
                'linkedin_link' : profile.linkdeln_link if profile.linkdeln_link else "",
            }
        
            return Response(response, status = status.HTTP_200_OK)
        return Response({
                "error" : "Invalid User Credentials"
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        user_id = self.request.data['id']
        experience = self.request.data['experience']
        hourly_rate = self.request.data['hourly_rate']
        languages = self.request.data['languages']
        bio = self.request.data['bio']
        skills = self.request.data['skills']
        website_link = self.request.data['website_link']
        linkdeln_link = self.request.data['linkedin_link']
        first_name = self.request.data['first_name']
        last_name = self.request.data['last_name']
        email = self.request.data['email']
        location = self.request.data['location']
        education = self.request.data['education']
        phone = self.request.data['phone_number']
        job_title = self.request.data['job_title']

        # validation
        if not user_id: 
            return Response({
                "msg" : "Invalid user id"
             })


        user = User.objects.get(id = user_id)
        profile = Profile.objects.get(user = user)

        user.location = location
        user.first_name = first_name, 
        user.phone_number = phone
        user.email = email 
        user.save()

        profile.experience = experience
        profile.hourly_rate = hourly_rate
        profile.bio = bio
        profile.languages = languages
        profile.skills = skills
        profile.website_link = website_link
        profile.education = education
        profile.linkdeln_link = linkdeln_link
        profile.job_title = job_title
        profile.save()

        response_data = {
            'job_title' : profile.job_title,
            'experience' : profile.experience,
            'hourly_rate' : profile.experience, 
            'languages' : profile.languages, 
            'bio' : profile.bio,
            'skills' : profile.skills, 
            'education' : profile.education,
            'website_link' : profile.website_link, 
            'linkedin_link' : profile.linkdeln_link,
            'id' : user.id, 
            'first_name' : user.first_name, 
            'last_name' : user.last_name, 
            'phone_number' : user.phone_number, 
            'location' : user.location, 
            'email' : user.email, 
            'role' : user.role
        }

        return Response(response_data, status=status.HTTP_200_OK)


class CreateJobView(generics.ListCreateAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):

        job = Job.objects.all()

        return job

    def perform_create(self, serializer):
        user_id = self.request.data.get('user_id')
        user = User.objects.get(id = user_id)
        serializer.save(user = user)

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'

class ProductView(generics.ListCreateAPIView):
    # permission_classes = [AllowAny, IsAuthenticated]
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        # product = Product.objects.all()
        product = Product.objects.all().order_by("-created_at")
        return product
    
    def perform_create(self, serializer):
        return super().perform_create(serializer)
    



class order_item(APIView):

    def post(self, request):

        serializer = JobApplySerializer( data = request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED )

        user_id = serializer.validated_data['user_id']
        job_id = serializer.validated_data['job_id']

        list_apply = Apply.objects.all()

        for applications in list_apply:
            if applications.job.id == job_id and applications.user.id == user_id:
                response = {
                    "msg" : "This user already applied for this job"
                }  

                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id = user_id)
        job = Job.objects.get(id = job_id)

        new_application = Apply(user = user, job = job)
        new_application.save()

        response = {
            "msg" : "Application Successful"
        }

        return Response(response, status=status.HTTP_201_CREATED)


    def get(self, request):
        user_id = request.query_params.get('id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"msg": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        list_jobs = Job.objects.filter(user=user)
        apply_list = Apply.objects.all()

        serializer = JobSerializer(list_jobs, many=True)

        send_list = []
        apply_id = []

        for job in list_jobs:
            for app in apply_list:

                if job.id == app.job.id:
                    target_user_id = app.user
                    try:
                        profile = Profile.objects.get(user = user)
                    except Profile.DoesNotExist:
                        profile = Profile.objects.create(user = user)

                    new_data = {
                        "id" : job.id, 
                        "jobId": job.id, 
                        "profile_id" : job.id, 
                        "job_title" : job.job_title, 
                        "experience" : "3",
                        "hourly_rate" : 12500.00,
                        "languages": profile.languages, 
                        "bio" : profile.bio,
                        "skills" : profile.skills, 
                        "education" : profile.education,
                        "website_link": profile.website_link,
                        "linkedin_link": profile.linkdeln_link,
                        "name": f"{app.user.first_name} {app.user.last_name}",
                        "email": app.user.email,
                        "phone": app.user.phone_number,
                        "location": app.user.address_default,
                        "appliedDate": app.applied_date,
                        "expectedSalary": app.salary,
                        "status": app.status,
                        "rating": 4.2,
                        "avatar": "ER",
                        "app_id" : app.id, 
                        "user_id" : app.user.id
                    }

                    print(new_data)

                    send_list.append(new_data)

    
        return Response({"data" : serializer.data, "app" : send_list}, status=status.HTTP_200_OK)


class GetDashboardDetails(APIView): 

    def get(self, request):

        user_id = request.query_params.get('id')

        if not user_id:
            return Response({"msg" : "Invalid user Id"})
        
        user = User.objects.get(id = user_id)

        list_apply = Apply.objects.filter(user = user).all()

        response = []
        for app in list_apply:


            if app.user.id == user.id:

                response_data = {
                    "id" : app.id, 
                    "jobId" : app.job.id, 
                    "job_title" : app.job.job_title,
                    "company_name" : f"{app.job.user.first_name} {app.job.user.last_name}",
                    "job_type" : app.job.job_type, 
                    "location" : app.job.location,
                    "category" : app.job.category, 
                    "payment_type" : app.job.payment_type,
                    "min_budget" : app.job.min_budget,
                    "max_budget" : app.job.max_budget,
                    "company_size" : app.job.company_size,
                    "required_skills" : app.job.required_skills, 
                    "special_skills" : app.job.special_skills,
                    "duration" : app.job.duration, 
                    "postedDate" : app.job.posted_date,
                    "description" : app.job.description,
                    "appliedDate" : app.applied_date,
                    "status" : app.status, 
                    "expectedSalary" : f"{app.job.min_budget} {app.job.max_budget}", 
                    "hourly_rate" : "",
                    # "experience" : ""
                    "app_id" : app.id
    
                }

                

                response.append(response_data)



        return Response(response, status = status.HTTP_200_OK)


class AcceptAppplicationView(APIView):

    def post(self, request):

        serialize_data = ApplicationSerializer(data = request.data)

        if not serialize_data.is_valid():

            return Response(serialize_data.errors, status=status.HTTP_400_BAD_REQUEST)

        app_id = serialize_data.validated_data['app_id']
        user_id = serialize_data.validated_data['user_id']
        status_data = serialize_data.validated_data['status']

        try:
            user = User.objects.get(id = user_id)
            application = Apply.objects.get(id = app_id)
        except Exception as e:
            print(e)
            return Response({"Error" : "Model does not exist"}, status = status.HTTP_400_BAD_REQUEST)

        if user and application and application.user == user:
            
            application.status = status_data
            application.save()

            return Response({"msg" : "Status saved successfully"})


        return Response({"Error" : "An error occured two"}, status = status.HTTP_400_BAD_REQUEST)
