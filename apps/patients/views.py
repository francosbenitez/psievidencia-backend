from rest_framework import generics
from .serializers import PatientSerializer, RegisterPatientSerializer
from rest_framework.response import Response


class Register(generics.GenericAPIView):
    """Register patients"""

    serializer_class = RegisterPatientSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()

        return Response(
            PatientSerializer(patient, context=self.get_serializer_context()).data
        )
