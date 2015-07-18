from rest_framework import status, mixins, generics, permissions
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_mongoengine.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.authentication import SessionAuthentication
from .serializers import BusinessSerializer, ReviewSerializer
from .models import Business, Review


class BusinessList(ListCreateAPIView):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()


class BusinessDetails(RetrieveUpdateDestroyAPIView):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()


class BusinessReviewList(ListCreateAPIView):

    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()

    def get_queryset(self):
        business_id = self.kwargs['id']
        business = Business.objects(id=business_id)[0]
        return Review.objects.filter(business=business)

    def pre_save(self, object):
        business = Business.objects(id=self.kwargs['id'])[0]
        author = self.request.user
        object.business = business
        object.author = author

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

        # return Response(review, status=status.HTTP_200_OK)

# class BusinessReviewList(ListCreateAPIView):
#     serializer_class = ReviewSerializer
#     queryset = Review.objects.all()

#     def get_queryset(self):
#         business_id = self.kwargs['business_id']
#         return Business.objects.filter(self.queryset.filter()



