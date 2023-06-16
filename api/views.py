from django.shortcuts import render
from django.core import serializers
from .models import * 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import generics,status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import (RegisterSerializer,
                          ScheduleSerializer,
                          StudentProfileSerializer,
                          BookmarSerializer,
                          ApplicantAppSerializer,
                          EducationBGSerializer,
                          WebProfileSerializer,
                          AppliedSerializer,
                          ApplicantSerializer,
                          BookmarkUserPostSerializer,
                          ActivityLogSerializer,
                          VerifyOtp,
                          ApplySerializer,
                          ApplySerializer,
                          EditProfilePicture,
                          UserDetailsAddressSerializer,
                          ProfileSerializer,
                          ProfileAddressSerializer,
                          LoginSerializer,
                          UserDetailsSerializer,
                          AddressSerializer,
                          GuardianSerializer,
                          CompanySerializer,
                          PostSerializer,
                          UserSerializer,
                          UserDetailsSerializer2 )  
from .email import *
from django.contrib.auth.hashers import make_password, check_password
import json
from rest_framework.generics import GenericAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

# Create your views here.



class RegisterView(APIView):
    serializer_class = RegisterSerializer


    def post(self,request):
        data=request.data
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_otp(serializer.data['email'])
        # queryset = User.objects.all()
        return Response(
          'Registered successfully!'
        )
      
class RegisterViewAll(generics.ListAPIView):
    serializer_class = RegisterSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

class RegisterViewEdit(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RegisterSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset
    

class VerifyOtpView(APIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        data=request.data
        serializer = VerifyOtp(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        otp = serializer.data['otp']
        user = User.objects.filter(email=email)
        if not user.exists():
            
            return Response({
                'status':400,
                'message': 'Something Went Wrong',
                'data':"Wrong Email"
            })
        if user[0].otp != otp:
            return Response({
                'status':400,
                'message': 'Something Went Wrong',
                'data': "Wrong Otp"
            })
        
        user = user.first()
        user.is_Verified = True
        user.save()
        

        return Response({
                'status': 200,
                'message': 'Account Verified',
                'data': {}
            })
        
class LoginView(APIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        data=request.data
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        password = serializer.data['password']
        user = User.objects.filter(email=email)
        
        user_data = serializer.data

        if not user.exists():

            return Response({
                'status':400,
                'message': 'Something Went Wrong',
                'data':"Incorrect Email Or password"
            })
        else:
            passw = check_password(password,user[0].password)
            if not passw:
                return Response({
                    'status':400,
                    'message': 'Something Went Wrong',
                    'data': "Incorrect Email Or password",
            })
        if not user[0].is_Verified:
            return Response({
                'status':200,
                'message': 'Check Your Email For Verification',
                'is_Verified': user[0].is_Verified,
                'email':user[0].email
            })
        else:
            profile = UserDetails.objects.filter(user=user[0].id)
            guardian = Guardian.objects.filter(user=user[0].id)
            education = EducationBg.objects.filter(user=user[0].id)
            


            if not profile:

                return Response({
                    'status': 200,
                    'message': 'Account Verified',
                    'id': user[0].id,
                    'usertype': user[0].usertype,
                    'email': user[0].email,
                    'password': user[0].password,
                    'created_at': user[0].created_at,
                    'is_Verified': user[0].is_Verified, 
                    'data': "No User Details",
                })
            elif user[0].usertype == "Student":
                if not guardian:
                    return Response({
                    'status': 200,
                    'message': 'Account Verified',
                    'id': user[0].id,
                    'usertype': user[0].usertype,
                    'email': user[0].email,
                    'password': user[0].password,
                    'created_at': user[0].created_at,
                    'is_Verified': user[0].is_Verified, 
                    'data': "No Guardian",
                })
                elif not education:
                    return Response({
                    'status': 200,
                    'message': 'Account Verified',
                    'id': user[0].id,
                    'usertype': user[0].usertype,
                    'email': user[0].email,
                    'password': user[0].password,
                    'created_at': user[0].created_at,
                    'is_Verified': user[0].is_Verified, 
                    'data': "No Education",
                })
                else:
                     return Response({
                    'status': 200,
                    'message': 'Account Verified',
                    'id': user[0].id,
                    'usertype': user[0].usertype,
                    'email': user[0].email,
                    'password': user[0].password,
                    'created_at': user[0].created_at,
                    'is_Verified': user[0].is_Verified, 
                    'data': "READY",
                })
            else:
                     return Response({
                    'status': 200,
                    'message': 'Account Verified',
                    'id': user[0].id,
                    'usertype': user[0].usertype,
                    'email': user[0].email,
                    'password': user[0].password,
                    'created_at': user[0].created_at,
                    'is_Verified': user[0].is_Verified, 
                    'data': "READY",
                })
class UserDetailsView(generics.ListCreateAPIView):
    serializer_class = UserDetailsSerializer
    queryset = UserDetails.objects.all()

class UserDetailsViewEdit(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailsSerializer
    queryset = UserDetails.objects.all()
    lookup_field = 'user'

class AddressView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

class AddressViewEdit(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    lookup_field= 'user'


class ProfileAddressView(generics.ListCreateAPIView):
    serializer_class =ProfileAddressSerializer
    queryset = UserDetails.objects.select_related('user').prefetch_related('user__address_set')


class GuardianView(generics.ListCreateAPIView):
    serializer_class = GuardianSerializer
    queryset = Guardian.objects.all()

class GuardianViewEdit(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GuardianSerializer
    queryset = Guardian.objects.all()
    lookup_field = 'user'

class EducationView(generics.ListCreateAPIView):
    serializer_class = EducationBGSerializer
    queryset = EducationBg.objects.all()

class EducationViewEdit(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EducationBGSerializer
    queryset = EducationBg.objects.all()
    lookup_field = 'user'

class CompanyView(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

class CompanyViewEdit(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    lookup_field = 'user'

class PostView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        user = self.kwargs['user']
        return Post.objects.filter(user = user)
    # queryset = Post.objects.all()

class PostViewEdit(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        user = self.kwargs['user']
        return Post.objects.filter(user = user)
    


class UserPostView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()



class Home(generics.ListAPIView):
    # def get(self,request):
    #     # users = User.objects.prefetch_related('id__userdetails_set').all()
    #     # users = UserDetails.objects.select_related('user').all()
    #     users = Post.objects.select_related('user').all()        
    #     # users = Post.objects.select_related('user').prefetch_related('id__post_set').all()
    #     # profile = users.user_profile.get(user=3)
    #     # post = users.post_profile.get(user=3)
    #     # post = profile.post_profile.get(user=3)
    #     user_list = serializers.serialize('json',users)
    #     return HttpResponse(user_list,content_type='text/json-comment-filter')
    serializer_class = UserDetailsSerializer2
    pagination_class = LimitOffsetPagination
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        usertype = "Employer"
        queryset = Post.objects.select_related('user').prefetch_related('user__userdetails_set','user__company_set','apply_set').filter(user = user_id)
        if usertype:
            queryset = queryset.filter(user__usertype = usertype).order_by('-created_at')
            # queryset = queryset.order_by('-user__post__created_at')
            return queryset

class Manage(generics.ListAPIView):
    # def get(self,request):
    #     # users = User.objects.prefetch_related('id__userdetails_set').all()
    #     # users = UserDetails.objects.select_related('user').all()
    #     users = Post.objects.select_related('user').all()        
    #     # users = Post.objects.select_related('user').prefetch_related('id__post_set').all()
    #     # profile = users.user_profile.get(user=3)
    #     # post = users.post_profile.get(user=3)
    #     # post = profile.post_profile.get(user=3)
    #     user_list = serializers.serialize('json',users)
    #     return HttpResponse(user_list,content_type='text/json-comment-filter')
    serializer_class = UserDetailsSerializer2
    pagination_class = LimitOffsetPagination
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        usertype = "Employer"
        queryset = Post.objects.select_related('user').prefetch_related('user__userdetails_set','user__company_set','apply_set').filter(user = user_id)
        if usertype:
            queryset = queryset.filter(user__usertype = usertype).order_by('-created_at')
            # queryset = queryset.order_by('-user__post__created_at')
            return queryset
class EmployerProfileView(generics.ListAPIView):
    # def get(self,request):
    #     # users = User.objects.prefetch_related('id__userdetails_set').all()
    #     # users = UserDetails.objects.select_related('user').all()
    #     users = Post.objects.select_related('user').all()        
    #     # users = Post.objects.select_related('user').prefetch_related('id__post_set').all()
    #     # profile = users.user_profile.get(user=3)
    #     # post = users.post_profile.get(user=3)
    #     # post = profile.post_profile.get(user=3)
    #     user_list = serializers.serialize('json',users)
    #     return HttpResponse(user_list,content_type='text/json-comment-filter')
    serializer_class = ProfileSerializer
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        usertype = "Employer"
        queryset = UserDetails.objects.select_related('user').prefetch_related('user__company_set','user__address_set').filter(user = user_id)
        # if usertype:
        #     queryset = queryset.filter(usertype = usertype)
            # queryset = queryset.order_by('-user__post__created_at')
        return queryset
    
    
# Edit profile with addresse Serializer I dont what Im doing
# class UserDetailsAndAddressUpdateView(GenericAPIView):
#     serializer_class = {
#         'user_details': UserDetailsSerializer,
#         'address': AddressSerializer,
#     }

#     def get_object(self, user_id):
#         user_details = UserDetails.objects.get(user=user_id)
#         address = Address.objects.get(user=user_id)
#         return {
#             'user_details': user_details,
#             'address': address,
#         }

#     def get_queryset(self):
#         return UserDetails.objects.all()

#     def perform_update(self, serializer):
#         serializer['user_details'].save()
#         serializer['address'].save()

#     def post(self, request, user_id):
#         data = {
#             'user_details': request.data.get('user_details'),
#             'address': request.data.get('address'),
#         }
#         obj = self.get_object(user_id)
#         serializer = {}
#         for key in data:
#             serializer[key] = self.serializer_class[key](obj[key], data=data[key], partial=True)
#             serializer[key].is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response({
#             'status': 'success',
#             'message': 'Details and Address updated successfully.',
#         })
class UserDetailsAddressView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailsAddressSerializer

    def get_object(self):
        user_id = self.request.user.id
        user_details = UserDetails.objects.get(user_id=user_id)
        address = Address.objects.get(user_id=user_id)

        return {
            'user_details': user_details,
            'address': address
        }

    def update(self, request, *args, **kwargs):
        user_id = request.user.id
        user_details = UserDetails.objects.get(user_id=user_id)
        address = Address.objects.get(user_id=user_id)

        user_details_serializer = UserDetailsSerializer(user_details, data=request.data.get('user_details'))
        if user_details_serializer.is_valid():
            user_details_serializer.save()

        address_serializer = AddressSerializer(address, data=request.data.get('address'))
        if address_serializer.is_valid():
            address_serializer.save()

        return self.get(request, *args, **kwargs)




class EditProfilePictureViews(generics.UpdateAPIView):
    serializer_class = EditProfilePicture
    queryset = UserDetails.objects.all()
    lookup_field = 'user'
    

class ApplyViews(generics.ListCreateAPIView):
    serializer_class = ApplySerializer
    queryset = Apply.objects.all()

class AbortViews(generics.RetrieveDestroyAPIView):
    serializer_class = ApplySerializer
    queryset = Apply.objects.all()

class applicantViews(generics.ListCreateAPIView):
    serializer_class = ApplySerializer
    queryset = Apply.objects.all()
class ApplyEditViews(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ApplySerializer
    queryset = Apply.objects.all()
    lookup_url_kwarg = ('user','post')
    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {}
        for field in self.lookup_url_kwarg:
            filter_kwargs[field] = self.kwargs.get(field)
        return get_object_or_404(queryset, **filter_kwargs)
        
        
        
       
class AppliedView(generics.ListAPIView):
    # def get(self,request):
    #     # users = User.objects.prefetch_related('id__userdetails_set').all()
    #     # users = UserDetails.objects.select_related('user').all()
    #     users = Post.objects.select_related('user').all()        
    #     # users = Post.objects.select_related('user').prefetch_related('id__post_set').all()
    #     # profile = users.user_profile.get(user=3)
    #     # post = users.post_profile.get(user=3)
    #     # post = profile.post_profile.get(user=3)
    #     user_list = serializers.serialize('json',users)
    #     return HttpResponse(user_list,content_type='text/json-comment-filter')
    serializer_class = AppliedSerializer
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        queryset = Apply.objects.select_related('user','post').prefetch_related('user__userdetails_set','user__address_set','user__guardian_set','user__educationbg_set').filter(post = post_id)
        queryset = queryset.order_by('-applied_at')
            # queryset = queryset.order_by('-user__post__created_at')
        return queryset



class Home2(generics.ListAPIView):
    # def get(self,request):
    #     # users = User.objects.prefetch_related('id__userdetails_set').all()
    #     # users = UserDetails.objects.select_related('user').all()
    #     users = Post.objects.select_related('user').all()        
    #     # users = Post.objects.select_related('user').prefetch_related('id__post_set').all()
    #     # profile = users.user_profile.get(user=3)
    #     # post = users.post_profile.get(user=3)
    #     # post = profile.post_profile.get(user=3)
    #     user_list = serializers.serialize('json',users)
    #     return HttpResponse(user_list,content_type='text/json-comment-filter')
    serializer_class = UserDetailsSerializer2
    def get_queryset(self):
        queryset = Post.objects.select_related('user').prefetch_related('user__userdetails_set','user__company_set','apply_set','bookmark_set','user__address_set').order_by('-created_at')
        return queryset
    
class StudenProfileView(generics.ListAPIView):
    # def get(self,request):
    #     # users = User.objects.prefetch_related('id__userdetails_set').all()
    #     # users = UserDetails.objects.select_related('user').all()
    #     users = Post.objects.select_related('user').all()        
    #     # users = Post.objects.select_related('user').prefetch_related('id__post_set').all()
    #     # profile = users.user_profile.get(user=3)
    #     # post = users.post_profile.get(user=3)
    #     # post = profile.post_profile.get(user=3)
    #     user_list = serializers.serialize('json',users)
    #     return HttpResponse(user_list,content_type='text/json-comment-filter')
    serializer_class = StudentProfileSerializer
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        
        queryset = User.objects.prefetch_related('userdetails_set','address_set','guardian_set','educationbg_set').filter(id = user_id)
        # if usertype:
        #     queryset = queryset.filter(usertype = usertype)
            # queryset = queryset.order_by('-user__post__created_at')
        return queryset
    
class BookmarkView(generics.ListCreateAPIView):
    serializer_class = BookmarSerializer
    queryset = Bookmark.objects.all()

class BookmarkViewEdit(generics.RetrieveDestroyAPIView):
    serializer_class = BookmarSerializer
    queryset = Bookmark.objects.all()

class StudentPostView(generics.ListAPIView):
    # def get(self,request):
    #     # users = User.objects.prefetch_related('id__userdetails_set').all()
    #     # users = UserDetails.objects.select_related('user').all()
    #     users = Post.objects.select_related('user').all()        
    #     # users = Post.objects.select_related('user').prefetch_related('id__post_set').all()
    #     # profile = users.user_profile.get(user=3)
    #     # post = users.post_profile.get(user=3)
    #     # post = profile.post_profile.get(user=3)
    #     user_list = serializers.serialize('json',users)
    #     return HttpResponse(user_list,content_type='text/json-comment-filter')
    serializer_class = UserDetailsSerializer2
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        queryset = Post.objects.select_related('user').prefetch_related('user__userdetails_set','user__company_set','apply_set','bookmark_set','user__address_set').filter(id=post_id)
        return queryset
    
class BookmarkUserPostViews(generics.ListAPIView):
    # def get(self,request):
    #     # users = User.objects.prefetch_related('id__userdetails_set').all()
    #     # users = UserDetails.objects.select_related('user').all()
    #     users = Post.objects.select_related('user').all()        
    #     # users = Post.objects.select_related('user').prefetch_related('id__post_set').all()
    #     # profile = users.user_profile.get(user=3)
    #     # post = users.post_profile.get(user=3)
    #     # post = profile.post_profile.get(user=3)
    #     user_list = serializers.serialize('json',users)
    #     return HttpResponse(user_list,content_type='text/json-comment-filter')
    serializer_class = BookmarkUserPostSerializer
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        queryset = Bookmark.objects.select_related('user','post').prefetch_related('user__userdetails_set','user__company_set','post__apply_set','post__bookmark_set','user__address_set').filter(user=user_id)
        return queryset
    
class ActivityLogViews(generics.ListAPIView):
    # def get(self,request):
    #     # users = User.objects.prefetch_related('id__userdetails_set').all()
    #     # users = UserDetails.objects.select_related('user').all()
    #     users = Post.objects.select_related('user').all()        
    #     # users = Post.objects.select_related('user').prefetch_related('id__post_set').all()
    #     # profile = users.user_profile.get(user=3)
    #     # post = users.post_profile.get(user=3)
    #     # post = profile.post_profile.get(user=3)
    #     user_list = serializers.serialize('json',users)
    #     return HttpResponse(user_list,content_type='text/json-comment-filter')
    serializer_class = ActivityLogSerializer
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        queryset = Apply.objects.select_related('user','post').filter(user=user_id)
        return queryset
    
class ApplicantViews(generics.ListAPIView):
    # def get(self,request):
    #     # users = User.objects.prefetch_related('id__userdetails_set').all()
    #     # users = UserDetails.objects.select_related('user').all()
    #     users = Post.objects.select_related('user').all()        
    #     # users = Post.objects.select_related('user').prefetch_related('id__post_set').all()
    #     # profile = users.user_profile.get(user=3)
    #     # post = users.post_profile.get(user=3)
    #     # post = profile.post_profile.get(user=3)
    #     user_list = serializers.serialize('json',users)
    #     return HttpResponse(user_list,content_type='text/json-comment-filter')
    serializer_class = ActivityLogSerializer
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        queryset = Apply.objects.select_related('user','post').filter(post__user=post_id)
        return queryset
    
                
# class UserDetailsView(generics.ListCreateAPIView):
#     serializer_class = WebProfileSerializer
#     queryset = UserDetails.objects.all()

class WebProfile(generics.ListAPIView):
    # def get(self,request):
    #     # users = User.objects.prefetch_related('id__userdetails_set').all()
    #     # users = UserDetails.objects.select_related('user').all()
    #     users = Post.objects.select_related('user').all()        
    #     # users = Post.objects.select_related('user').prefetch_related('id__post_set').all()
    #     # profile = users.user_profile.get(user=3)
    #     # post = users.post_profile.get(user=3)
    #     # post = profile.post_profile.get(user=3)
    #     user_list = serializers.serialize('json',users)
    #     return HttpResponse(user_list,content_type='text/json-comment-filter')
    serializer_class = WebProfileSerializer
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        queryset = User.objects.prefetch_related('address_set','userdetails_set','company_set','guardian_set','educationbg_set').filter(id=user_id)
        return queryset
    

    
class ApprovedApplicantViews(generics.ListCreateAPIView):
    serializer_class  = ApplicantSerializer
    queryset = Applicant.objects.all()


class Get_user_posts(APIView):
    @csrf_exempt
    def get(self, request, id):
        if request.method == 'GET':
            posts = Post.objects.filter(user__id=id, apply__applicant__status='Approved').annotate(
                applicantNO=Count('apply'),
                noApprove=Count('apply__applicant')
            ).select_related('user').order_by('-created_at').values(
                'id', 'looking_for', 'status', 'created_at', 'applicantNO', 'noApprove',
                'user__id', 'user__email', 'user__userdetails__profile','user__company__comp_name','user__userdetails__last_name',
                'user__userdetails__first_name','user__userdetails__mid_name','user__userdetails__suff_name',
                'user__address__street','user__address__city','user__address__province','user__address__zipcode','job_type','rate','salary',
                'start_date','end_date','job_type'
            )

            return JsonResponse({'posts': list(posts)})

class Get_applied_user(APIView):
    @csrf_exempt
    def get(self,request, id):
        if request.method == 'GET':
            posts = Post.objects.filter(id=id,apply__applicant__status = None,apply__id__isnull = False).select_related('user').order_by('-apply__applied_at').values(
                'id', 'looking_for', 'status', 'created_at','apply__id','apply__applicant__status',
                'user__id', 'user__email','apply__user__userdetails__profile','apply__user__userdetails__first_name','apply__user__userdetails__last_name','apply__user__userdetails__profile',
                'apply__user__userdetails__suff_name','apply__user__userdetails__contact_no','user__userdetails__first_name','user__userdetails__last_name','user__userdetails__mid_name',
                'user__userdetails__suff_name','user__email',
                'apply__user__userdetails__mid_name','apply__user__address__street','apply__user__address__city','apply__user__address__province','apply__user__address__zipcode',
                'apply__user__userdetails__birthday','apply__user__userdetails__id','apply__applicant__status','apply__user__email','apply__user__userdetails__age','apply__user__guardian__g_name','apply__user__guardian__g_contact_no',
                'apply__user__educationbg__sch_name','apply__user__educationbg__sch_address','apply__user__educationbg__year_level','apply__school_id','apply__cor','apply__cov_let'
                )
            return JsonResponse({'posts': list(posts)})
class Get_applicant_user(APIView): 
    @csrf_exempt
    def get(self,request, id):
        if request.method == 'GET':
            posts = Post.objects.filter(id=id,apply__applicant__status = "Approved").select_related('user').order_by('-apply__applied_at').values(
                'id','apply__applicant__status',
                'apply__user__userdetails__profile','apply__user__userdetails__first_name','apply__user__userdetails__last_name','apply__user__userdetails__profile',
                'apply__user__userdetails__suff_name' ,'apply__user__userdetails__contact_no',
                'apply__user__userdetails__mid_name','apply__user__address__street','apply__user__address__city','apply__user__address__province','apply__user__address__zipcode',
                'apply__user__userdetails__birthday','apply__user__userdetails__id','apply__applicant__status','apply__user__email','apply__user__userdetails__age','apply__user__guardian__g_name','apply__user__guardian__g_contact_no',
                'apply__user__educationbg__sch_name','apply__user__educationbg__sch_address','apply__user__educationbg__year_level','apply__school_id','apply__cor','apply__cov_let','apply__applicant__schedule__id','apply__applicant__id',
                'apply__applicant__schedule__applicant','apply__applicant__schedule__interview_type','apply__applicant__schedule__method','apply__applicant__schedule__start_date','apply__applicant__schedule__end_date',
                'apply__applicant__schedule__start_time','apply__applicant__schedule__end_time'
               
            )
            return JsonResponse({'posts': list(posts)})
class ScheduleViews(generics.ListCreateAPIView):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

class ScheduleEditViews(generics.RetrieveUpdateAPIView):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

class Get_notif_user(APIView): 
    @csrf_exempt
    def get(self,request, id):
        if request.method == 'GET':
            posts = Post.objects.filter(user__id=id,apply__applicant__apply = None,apply__id__isnull=False).select_related('user').order_by('-apply__applied_at').values(
                'id','apply__applicant__status','looking_for',
                'apply__user__userdetails__profile','apply__user__userdetails__first_name','apply__user__userdetails__last_name','apply__user__userdetails__profile',
                'apply__user__userdetails__suff_name' ,'apply__user__userdetails__contact_no',
                'apply__user__userdetails__mid_name','apply__user__address__street','apply__user__address__city','apply__user__address__province','apply__user__address__zipcode',
                'apply__user__userdetails__birthday','apply__user__userdetails__id','apply__applicant__status','apply__user__email','apply__user__userdetails__age','apply__user__guardian__g_name','apply__user__guardian__g_contact_no',
                'apply__user__educationbg__sch_name','apply__user__educationbg__sch_address','apply__user__educationbg__year_level','apply__school_id','apply__cor','apply__cov_let','apply__applicant__schedule__id','apply__applicant__id',
                'apply__applicant__schedule__applicant','apply__applicant__schedule__interview_type','apply__applicant__schedule__method','apply__applicant__schedule__start_date','apply__applicant__schedule__end_date',
                'apply__applicant__schedule__start_time','apply__applicant__schedule__end_time','apply__applied_at'
               
            )
            return JsonResponse({'posts': list(posts)})
        

class Get_activity_user(APIView): 
    @csrf_exempt
    def get(self,request, id):
        if request.method == 'GET':
            posts = Post.objects.filter(apply__id=id).select_related('user').order_by('-apply__applied_at').values(
                'id','apply__applicant__status','looking_for','image',
                'street','city','province','zipcode','job_type', 'salary','rate','start_date','end_date','user__company__comp_name'
                ,
                'apply__user__userdetails__profile','apply__user__userdetails__first_name','apply__user__userdetails__last_name','apply__user__userdetails__profile',
                'apply__user__userdetails__suff_name' ,'apply__user__userdetails__contact_no',
                'apply__user__userdetails__mid_name','apply__user__address__street','apply__user__address__city','apply__user__address__province','apply__user__address__zipcode',
                'apply__user__userdetails__birthday','apply__user__userdetails__id','apply__applicant__status','apply__user__email','apply__user__userdetails__age','apply__user__guardian__g_name','apply__user__guardian__g_contact_no',
                'apply__user__educationbg__sch_name','apply__user__educationbg__sch_address','apply__user__educationbg__year_level','apply__school_id','apply__cor','apply__cov_let','apply__applicant__schedule__id','apply__applicant__id',
                'apply__applicant__schedule__applicant','apply__applicant__schedule__interview_type','apply__applicant__schedule__method','apply__applicant__schedule__start_date','apply__applicant__schedule__end_date',
                'apply__applicant__schedule__start_time','apply__applicant__schedule__end_time','apply__applied_at','user__userdetails__first_name','user__userdetails__last_name',
                'user__userdetails__mid_name','user__userdetails__suff_name'
               
            )
            return JsonResponse({'posts': list(posts)})


class Get_notif_stu_user(APIView): 
    @csrf_exempt
    def get(self,request, id):
        if request.method == 'GET':
            posts = Post.objects.filter(apply__user__id=id).select_related('user').order_by('-apply__applied_at').values(
                'id','apply__applicant__status','looking_for','image',
                'street','city','province','zipcode','job_type', 'salary','rate','start_date','end_date','user__company__comp_name','user__userdetails__profile'
                ,
                'apply__user__userdetails__profile','apply__user__userdetails__first_name','apply__user__userdetails__last_name','apply__user__userdetails__profile',
                'apply__user__userdetails__suff_name' ,'apply__user__userdetails__contact_no',
                'apply__user__userdetails__mid_name','apply__user__address__street','apply__user__address__city','apply__user__address__province','apply__user__address__zipcode',
                'apply__user__userdetails__birthday','apply__user__userdetails__id','apply__applicant__status','apply__user__email','apply__user__userdetails__age','apply__user__guardian__g_name','apply__user__guardian__g_contact_no',
                'apply__user__educationbg__sch_name','apply__user__educationbg__sch_address','apply__user__educationbg__year_level','apply__school_id','apply__cor','apply__cov_let','apply__applicant__schedule__id','apply__applicant__id',
                'apply__applicant__schedule__applicant','apply__applicant__schedule__interview_type','apply__applicant__schedule__method','apply__applicant__schedule__start_date','apply__applicant__schedule__end_date',
                'apply__applicant__schedule__start_time','apply__applicant__schedule__end_time','apply__applied_at','user__userdetails__first_name','user__userdetails__last_name',
                'user__userdetails__mid_name','user__userdetails__suff_name','apply__applicant__date'
               
            )
            return JsonResponse({'posts': list(posts)})