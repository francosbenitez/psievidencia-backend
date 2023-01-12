from rest_framework import generics
from .serializers import PsychologistSerializer, RegisterPsychologistSerializer
from rest_framework.response import Response


class Register(generics.GenericAPIView):
    """Register psychologists"""

    serializer_class = RegisterPsychologistSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        psychologist = serializer.save()

        return Response(
            PsychologistSerializer(
                psychologist, context=self.get_serializer_context()
            ).data
        )
