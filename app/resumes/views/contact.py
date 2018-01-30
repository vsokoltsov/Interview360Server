from . import viewsets, list_route, Response, status, get_object_or_404
from rest_framework.views import APIView
from resumes.forms import ContactForm
from resumes.serializers import ContactSerializer

class ContactApiView(APIView):
    """ View for contact resource """

    def put(self, request, resume_id=None):
        """ Create or update new contact instance for resume """

        form = ContactForm(params=request.data)
        if form.submit():
            return Response(
                { 'contact': ContactSerializer(form.object).data }
            )
        else:
            return Response(
                { 'errors': form.errors }, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, resume_id=None):
        """ Delete existing contact """

        resume = get_object_or_404(Resume, resume_id)
        resume.contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
