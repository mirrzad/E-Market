from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .seializers import RegisterSerializer, UserSerializer
from account.models import User
from rest_framework import viewsets


class RegisterApiView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.POST)
        if ser_data.is_valid():
            sd = ser_data.validated_data
            user = User(
                phone_number=sd['phone_number'],
                email=sd['email'],
            )
            user.set_password(sd['password'])
            user.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAuthTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        token = get_object_or_404(Token, user=request.user)
        token.delete()
        return Response({'detail': 'Token deleted'}, status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def list(self, request):
        page_num = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 2)
        paginator = Paginator(self.queryset.filter(is_active=True), limit)
        try:
            srz_data = self.serializer_class(instance=paginator.page(page_num), many=True)
        except:
            return Response({'detail': 'This page contains no results'}, status=status.HTTP_404_NOT_FOUND)
        return Response(srz_data.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        if user != request.user:
            return Response({'permission denied': 'You are not the owner'}, status=status.HTTP_403_FORBIDDEN)
        srz_data = self.serializer_class(instance=user, data=request.data, partial=True)
        if srz_data.is_valid(raise_exception=True):
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        if user != request.user:
            return Response({'permission denied': 'You are not the owner'}, status=status.HTTP_403_FORBIDDEN)
        user.is_active = False
        user.save()
        return Response({'detail': 'User deleted'}, status=status.HTTP_204_NO_CONTENT)
