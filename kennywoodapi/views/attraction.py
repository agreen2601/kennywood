"""Attractions for Kennywood Amusement Park"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Attraction


class AttractionSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for attractions

    Arguments:
        serializers
    """
    class Meta:
        model = Attraction
        url = serializers.HyperlinkedIdentityField(
            view_name='attraction',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'area_id')


class Attractions(ViewSet):
    """Attractions for Kennywood Amusement Park"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Attraction instance
        """
        newattrctn = Attraction()
        newattrctn.name = request.data["name"]
        newattrctn.area_id = request.data["area_id"]
        newattrctn.save()

        serializer = AttractionSerializer(
            newattrctn, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single attraction

        Returns:
            Response -- JSON serialized attraction instance
        """
        try:
            attrctn = Attraction.objects.get(pk=pk)
            serializer = AttractionSerializer(
                attrctn, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a attraction

        Returns:
            Response -- Empty body with 204 status code
        """
        attrctn = Attraction.objects.get(pk=pk)
        attrctn.name = request.data["name"]
        attrctn.area_id = request.data["area_id"]
        attrctn.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single attraction

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            attrctn = Attraction.objects.get(pk=pk)
            attrctn.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Attraction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to attractions resource

        Returns:
            Response -- JSON serialized list of attractions
        """
        attrctns = Attraction.objects.all()

        area = self.request.query_params.get('area', None)
        if area is not None:
            attrctns = attrctns.filter(area_id=area)

        serializer = AttractionSerializer(
            attrctns, many=True, context={'request': request})
        return Response(serializer.data)
