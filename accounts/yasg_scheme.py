from drf_yasg import openapi

from accounts.serializers import StudentSerializer

registration_post_scheme = openapi.Response(
    description="You get a json:",
    schema=StudentSerializer
)

registration_post_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'user': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password'],
        ),
        'full_name': openapi.Schema(type=openapi.TYPE_STRING),
        'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
        'passport_data': openapi.Schema(type=openapi.TYPE_STRING),
    },
    required=['user', 'full_name', 'phone_number']
)
