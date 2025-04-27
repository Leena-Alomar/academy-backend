from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course,User,Schedule,Lesson
from .serializers import UserSerializer,CourseSerializer,ScheduleSerializer ,LessonSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import generics, status, permissions

     
# User Registration
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    try:
      response = super().create(request, *args, **kwargs)
      user = User.objects.get(username=response.data['username'])
      refresh = RefreshToken.for_user(user)
      content = {'refresh': str(refresh), 'access': str(refresh.access_token), 'user': response.data }
      return Response(content, status=status.HTTP_201_CREATED)
    except Exception as err:
      print(err)
      return Response({ 'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    



# Login View
class LoginView(APIView):

  def post(self, request):
    try:
      username = request.data.get('username')
      password = request.data.get('password')
      user = authenticate(username=username, password=password)
      if user:
        refresh = RefreshToken.for_user(user)
        content = {'refresh': str(refresh), 'access': str(refresh.access_token),'user': UserSerializer(user).data}
        return Response(content, status=status.HTTP_200_OK)
      return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
      return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    try:
      user = User.objects.get(username=request.user.username)
      try:
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh),'access': str(refresh.access_token),'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
      except Exception as token_error:
        return Response({"detail": "Failed to generate token.", "error": str(token_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as err:
      return Response({"detail": "Unexpected error occurred.", "error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 

# Define the Coures view
class CourseDetailsView(APIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = CourseSerializer 

  def get(self, request):
    try:
      queryset = Course.objects.all()
      serializer = CourseSerializer(queryset, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as err:
      return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Define the Schedule view
class ScheduleDetailsView(APIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = ScheduleSerializer

  def get(self, request, id):
    

      try:
          schedule = get_object_or_404(Schedule, pk=id)
          lessons = Lesson.objects.filter(lesson_sch=schedule)
          return Response({
              "schedule": ScheduleSerializer(schedule).data,
              "lessons": LessonSerializer(lessons, many=True).data,
          }, status=status.HTTP_200_OK)
      except Exception as err:
          return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



  def delete(self, request, id):
      try:
          schedule = get_object_or_404(Schedule, pk=id)
          schedule.delete()
          return Response({'success': True}, status=status.HTTP_200_OK)
      except Exception as err:
          return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ScheduleLessonRelationView(APIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = ScheduleSerializer

  def put(self, request, id):
    try:
        schedule = Schedule.objects.get(id=id)
        lesson = Lesson.objects.get(id=id)
    except (Schedule.DoesNotExist, Lesson.DoesNotExist):
        return Response({'error': 'Schedule or Lesson not found'}, status=404)
    lesson.lesson_sch = schedule
    lesson.save()
    return Response({'message': f'Lesson {lesson.lesson_name} added to Schedule {schedule.schedule_id}'}, status=200)

# here how can i have id for two diff modles
  def delete(self, request, schedule_id, lesson_id):
    try:
        schedule = Schedule.objects.get(id=id)
        lesson = Lesson.objects.get(id=id)
    except (Schedule.DoesNotExist, Lesson.DoesNotExist):
        return Response({'error': 'Schedule or Lesson not found'}, status=404)
    lesson.delete()
    return Response({'message': f'Lesson {lesson.lesson_name} is deleted'}, status=200)

    def post(self, request, schedule_id):
        try:
            schedule = Schedule.objects.get(id=id)
        except (Schedule.DoesNotExist):
            return Response({'error': 'Schedule not found'}, status=404)

        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(lesson_sch=schedule)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Define the Lesson view
class LessonDetailsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LessonSerializer

    def get(self, request, id):
        lesson = get_object_or_404(Lesson, pk=id)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)


    def delete(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, pk=id)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class LessonRelationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LessonSerializer

    def put(self, request, lesson_id):
        try:
            lesson = get_object_or_404(Lesson, id=lesson_id)
            serializer = LessonSerializer(lesson, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Lesson.DoesNotExist:
            return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, lesson_id):
        try:

            lesson = Lesson.objects.get(id=lesson_id)
        except ( Lesson.DoesNotExist):
            return Response({'error': ' Lesson not found'}, status=404)
        lesson.lesson_sch = None
        lesson.save()
        lesson.delete()
        return Response({'message': f'Lesson {lesson.lesson_name} is deleted'}, status=200)


    def post(self, request,lesson_id):
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    