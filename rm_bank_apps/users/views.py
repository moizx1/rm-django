from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .serializers import UserSerializer
from ..accounts.serializers import AccountSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User Registered Successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_my_profile(request):
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Profile updated successfully'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    if not old_password or not new_password:
        return Response({'error': 'Both old and new passwords are required'}, status=400)
    if not user.check_password(old_password):
        return Response({'error': 'Old password is incorrect'}, status=400)
    user.set_password(new_password)
    user.save()
    return Response({'message': 'Password changed successfully'})

@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic
def register_customer_with_account(request):
    user_data = request.data.get('user')
    account_data = request.data.get('account')

    if not user_data or not account_data:
        return Response({'error': 'Both user and account data are required'}, status=400)

    user_data['roles'] = ['account_holder']

    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        saved_user = user_serializer.save()

        account_data['user'] = saved_user.id
        account_serializer = AccountSerializer(data=account_data)

        if account_serializer.is_valid():
            saved_account = account_serializer.save()

            return Response({
                'user': UserSerializer(saved_user).data,
                'account': AccountSerializer(saved_account).data,
                'message': 'User and account created successfully'
            }, status=201)
        else:
            return Response(account_serializer.errors, status=400)
    else:
        return Response(user_serializer.errors, status=400)
        