from django.urls import path
from .views import *
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('register/All/', RegisterViewAll.as_view()),
    path('verify/', VerifyOtpView.as_view()),
    path('register/<int:pk>/', RegisterViewEdit.as_view()),
    path('login/', LoginView.as_view()),


    path('userdetails/', UserDetailsView.as_view()),
    path('userdetails/<int:user>/', UserDetailsViewEdit.as_view()),
    path('userdetails/profile/picture/<int:user>/', EditProfilePictureViews.as_view()),
    path('address/', AddressView.as_view()),
    path('address/<int:user>/', AddressViewEdit.as_view()),


    path('profile/address/', ProfileAddressView.as_view()),

    path('guardian/', GuardianView.as_view()),
    path('guardian/<int:user>/', GuardianViewEdit.as_view()),

     path('education/',EducationView.as_view()),
    path('education/<int:user>/', EducationViewEdit.as_view()),

    path('company/', CompanyView.as_view()),
    path('company/<int:user>/', CompanyViewEdit.as_view()),
    path('post/<int:user>/', PostView.as_view()),
    # path('post/<int:user>/', PostViewRead.as_view()),
    path('post/<int:pk>/<int:user>/', PostViewEdit.as_view()),

    path('post/view/<int:user_id>/', Home.as_view()),
    path('post/manage/<int:user_id>/<int:pk>/', Home.as_view()),

    path('profile/<int:user_id>/', EmployerProfileView.as_view()),
    path('profile/student/<int:user_id>/', StudenProfileView.as_view()),
    path('user-details/<int:pk>/', UserDetailsAddressView.as_view()),

    path('apply/',  ApplyViews.as_view()),
     path('abort/<int:pk>',  AbortViews.as_view()),


    path('apply/create/<int:user>/<int:post>',  ApplyEditViews.as_view()),
    
    path('apply/applied/<int:post_id>/',  AppliedView.as_view()),
    
    path('post/view/home', Home2.as_view()),
    path('student/bookmark', BookmarkView.as_view()),
    path('student/bookmark/<int:pk>', BookmarkViewEdit.as_view()),
    path('student/post/description/<int:post_id>', StudentPostView.as_view()),
    path('student/bookmark/view/<int:user_id>', BookmarkUserPostViews.as_view()),
    path('student/activity-log/view/<int:user_id>', ActivityLogViews.as_view()),
    path('applicant/view/<int:post_id>', ApplicantViews.as_view()),
    
    path('applicant/view/app/atay', ApprovedApplicantViews.as_view()),
    path('web/profile/<int:user_id>', WebProfile.as_view()),

    path('user/posts/<int:id>/', Get_user_posts.as_view(), name='get_user_posts'),
    path('user/applied/<int:id>/', Get_applied_user.as_view(), name='get_applied_user'),
    
    path('user/applicant/<int:id>/', Get_applicant_user.as_view(), name='get_applicant_user'),

    path('add/schedule/', ScheduleViews.as_view()),
    path('edit/schedule/<int:pk>/', ScheduleEditViews.as_view()),

    path('notif/<int:id>/', Get_notif_user.as_view()),

    path('activity/<int:id>/', Get_activity_user.as_view()),

     path('notif/stu/<int:id>/', Get_notif_stu_user.as_view()),

]
