import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Client, Calculation, ClientType
from .interpreter import calc_result

class CalculateView(APIView):
    """
    API endpoint for performing engineering economic calculations.
    """
    permission_classes = [AllowAny]
    
    def get_client(self, client_id, client_type):
        """Get or create client based on ID and type."""
        try:
            if client_id:
                # Try to get existing client with the same ID and type
                client = Client.objects.get(id=client_id, client_type=client_type)
                client.last_seen = timezone.now()
                client.save()
                return client, False
        except (Client.DoesNotExist, ValueError):
            # If client doesn't exist or ID is invalid, create a new one
            pass
            
        # Create new client
        client = Client.objects.create(client_type=client_type)
        return client, True
    
    @swagger_auto_schema(
        operation_description="Calculate the result of an engineering economic expression",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['expression'],
            properties={
                'expression': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='The engineering economic expression to evaluate',
                    example='(20000(P|A, 15%, 2) + 25000(P|A, 0.15, 3)(P|F, 15%, 2))'
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Calculation successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'result': openapi.Schema(type=openapi.TYPE_STRING),
                        'client_id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid'),
                    }
                )
            ),
            400: "Invalid input: Expression is required or invalid",
            500: "An error occurred during calculation"
        },
        manual_parameters=[
            openapi.Parameter(
                'sama-clientid',
                openapi.IN_HEADER,
                description='Client ID for tracking usage',
                type=openapi.TYPE_STRING,
                format='uuid',
                required=False
            ),
            openapi.Parameter(
                'sama-clienttype',
                openapi.IN_HEADER,
                description='Type of client (web, api, mobile)',
                type=openapi.TYPE_STRING,
                enum=['web', 'api', 'mobile'],
                default='api',
                required=False
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        # Get client ID and type from headers
        client_id = request.headers.get('sama-clientid')
        client_type = request.headers.get('sama-clienttype', 'api').lower()
        
        # Validate client type
        if client_type not in dict(ClientType.choices):
            client_type = ClientType.API
        else:
            client_type = ClientType(client_type)
        
        # Get or create client
        client, is_new = self.get_client(client_id, client_type)
        
        # Get expression from request
        expression = request.data.get('expression')
        if not expression:
            return Response(
                {"error": "Expression is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialize response
        response_headers = {
            'sama-clientid': str(client.id),
            'sama-clienttype': client.get_client_type_display().lower(),
        }
        
        # Calculate result and track the calculation
        calculation = Calculation.objects.create(
            client=client,
            expression=expression
        )
        
        try:
            result = calc_result(expression)
            calculation.result = result
            calculation.save()
            
            response_data = {
                'result': result,
                'client_id': str(client.id),
            }
            return Response(
                response_data,
                status=status.HTTP_200_OK,
                headers=response_headers
            )
            
        except Exception as e:
            calculation.error = str(e)
            calculation.save()
            
            response_headers['sama-error'] = 'calculation_error'
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST,
                headers=response_headers
            )