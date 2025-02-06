from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Person
from .serializers import PersonSerializer

class StatsView(APIView):
    def get(self, request):
        total = Person.objects.count()  # นับจำนวนทั้งหมด
        checked_in = Person.objects.filter(verified=0).count()  # verified = 0
        in_checkin_room = Person.objects.filter(verified=1).count()  # verified = 1
        in_graduation_room = Person.objects.filter(verified=2).count()  # verified = 2

        stats = {
            'total': total,
            'checked_in': checked_in,
            'in_checkin_room': in_checkin_room,
            'in_graduation_room': in_graduation_room
        }
        return Response(stats, status=status.HTTP_200_OK)

class PersonList(APIView):
    def get(self, request):
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            person = Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        ids = request.data.get('ids', [])  # รับรายการ ID ที่ต้องการลบ
        if not ids:
            return Response({'error': 'No IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

        Person.objects.filter(id__in=ids).delete()  # ลบข้อมูลตาม ID
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class PersonDetail(APIView):
    def get(self, request, pk):
        try:
            person = Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PersonSerializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            person = Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk):
        try:
            person = Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)