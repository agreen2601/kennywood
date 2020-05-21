"""Itineraries for Kennywood Amusement Park"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Itinerary


class ItinerarySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for itineraries

    Arguments:
        serializers
    """
    class Meta:
        model = Itinerary
        url = serializers.HyperlinkedIdentityField(
            view_name='itinerary',
            lookup_field='id'
        )
        fields = ('id', 'starttime', 'attraction_id', 'customer_id')


class Itineraries(ViewSet):
    """Itineraries for Kennywood Amusement Park"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized itinerary instance
        """
        newitin = Itinerary()
        newitin.starttime = request.data["starttime"]
        newitin.attraction_id = request.data["attraction_id"]
        newitin.save()

        serializer = ItinerarySerializer(
            newitin, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single itinerary

        Returns:
            Response -- JSON serialized Itinerary instance
        """
        try:
            itin = Itinerary.objects.get(pk=pk)
            serializer = ItinerarySerializer(
                itin, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a itinerary

        Returns:
            Response -- Empty body with 204 status code
        """
        itin = Itinerary.objects.get(pk=pk)
        itin.starttime = request.data["starttime"]
        itin.customer_id = request.data["customer_id"]
        itin.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single itinerary

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            itin = Itinerary.objects.get(pk=pk)
            itin.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Itinerary.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to itineraries resource

        Returns:
            Response -- JSON serialized list of itineraries
        """
        itins = Itinerary.objects.all()

        customer = self.request.query_params.get('customer', None)
        if customer is not None:
            itins = itins.filter(customer_id=customer)

        serializer = ItinerarySerializer(
            itins, many=True, context={'request': request})
        return Response(serializer.data)
