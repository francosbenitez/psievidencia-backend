from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.response import Response


class Register(generics.GenericAPIView):

    # serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # send_activation_email(user, request)

        return Response(
            UserSerializer(user, context=self.get_serializer_context()).data
        )
