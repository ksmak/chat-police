from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
)

from .models import Chat
from .serializers import ChatSerializer


class ChatViewSet(ViewSet):
    """ChatViewSet."""

    def list(self, request):
        queryset = Chat.objects.filter(users__in=[self.request.user.id])
        serializer = ChatSerializer(queryset, many=True)
        return Response(serializer.data)


class FileUploadView(APIView):
    """View for upload user's files."""

    def post(self, request):
        if not request.FILES and not request.FILES["file"]:
            return Response({"error": "File not found."}, HTTP_400_BAD_REQUEST)

        file = request.FILES["file"]

        fs = FileSystemStorage()

        fs.save(file.name, file)

        return Response(
            {
                "filename": file.name,
            },
            HTTP_202_ACCEPTED,
        )
