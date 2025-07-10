from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .utils import query_knowledge_base, process_document
from .llm import get_llm_response
from .models import Document, InteractionLog
from .serializers import DocumentSerializer, AskQuestionSerializer

class UploadThrottle(AnonRateThrottle):
    rate = '5/minute'

@method_decorator(csrf_exempt, name='dispatch')
@extend_schema(
    request=AskQuestionSerializer,
    responses={
        200: OpenApiResponse(
            response={
                'type': 'object',
                'properties': {
                    'answer': {'type': 'string', 'description': 'The answer to the question'},
                    'sources': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': 'List of source documents and pages'
                    }
                }
            },
            description='Successful response with answer and sources'
        ),
        400: OpenApiResponse(
            response={'type': 'object', 'properties': {'error': {'type': 'string'}}},
            description='Bad request due to missing or invalid question'
        ),
        401: OpenApiResponse(
            response={'type': 'object', 'properties': {'detail': {'type': 'string'}}},
            description='Unauthorized due to missing or invalid token'
        ),
        429: OpenApiResponse(
            response={'type': 'object', 'properties': {'detail': {'type': 'string'}}},
            description='Too many requests (rate limit exceeded)'
        ),
        500: OpenApiResponse(
            response={'type': 'object', 'properties': {'error': {'type': 'string'}}},
            description='Server error during context retrieval or LLM processing'
        )
    },
    description='Query the knowledge base with a natural language question (rate-limited to 10 requests/minute, requires token authentication)'
)
class AskQuestionView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = AskQuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        question = serializer.validated_data['question']
        
        # Retrieve relevant chunks
        try:
            results = query_knowledge_base(question)
            context = "\n".join([result['text'] for result in results])
            sources = [f"{result['metadata']['file_name']} - Page {result['metadata']['page']}" for result in results]
        except Exception as e:
            return Response({"error": f"Failed to retrieve context: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Get LLM response
        try:
            answer = get_llm_response(question, context)
        except Exception as e:
            return Response({"error": f"LLM processing failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Log interaction
        try:
            InteractionLog.objects.create(
                user=request.user,
                question=question,
                answer=answer,
                sources=sources
            )
        except Exception as e:
            print(f"Failed to log interaction: {str(e)}")
        
        return Response({
            "answer": answer,
            "sources": sources
        }, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
@extend_schema(
    request=DocumentSerializer,
    responses={
        201: OpenApiResponse(
            response={
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'description': 'Success message'},
                    'file_name': {'type': 'string', 'description': 'Name of the uploaded file'}
                }
            },
            description='Successful document upload and processing'
        ),
        400: OpenApiResponse(
            response={'type': 'object', 'properties': {'error': {'type': 'string'}}},
            description='Bad request due to invalid file or file_name'
        ),
        401: OpenApiResponse(
            response={'type': 'object', 'properties': {'detail': {'type': 'string'}}},
            description='Unauthorized due to missing or invalid token'
        ),
        429: OpenApiResponse(
            response={'type': 'object', 'properties': {'detail': {'type': 'string'}}},
            description='Too many requests (rate limit exceeded)'
        ),
        500: OpenApiResponse(
            response={'type': 'object', 'properties': {'error': {'type': 'string'}}},
            description='Server error during document processing'
        )
    },
    description='Upload a PDF file to create a searchable knowledge base (rate-limited to 5 requests/minute, requires token authentication)'
)
class DocumentUploadView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UploadThrottle]

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            document = serializer.save()
            try:
                process_document(document.id)
                return Response({
                    "message": "Document uploaded and processed successfully",
                    "file_name": document.file_name
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                document.delete()
                return Response({"error": f"Processing failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)