import datetime

from mongoengine import Document, DynamicDocument
from mongoengine import (
    StringField, ListField,
    ReferenceField, DecimalField, DateTimeField
)
from mongoengine import signals
from mongoengine.django.auth import User

class Review(DynamicDocument):

    RATING_CHOICES = [
        (1.0, 1.0),
        (1.5, 1.5),
        (2.0, 2.0),
        (2.5, 2.5),
        (3.0, 3.0),
        (3.5, 3.5),
        (4.0, 4.0),
        (4.5, 4.5),
        (5.0, 5.0)
    ]
    rating = DecimalField(required=True, choices=RATING_CHOICES)
    comment = StringField()
    author = ReferenceField(User)
    business = ReferenceField('Business')
    tags = ListField(StringField())
    created = DateTimeField(default=datetime.datetime.now)

    meta = {
        'ordering': ['-created']
    }


class Business(DynamicDocument):

    name = StringField(required=True)
    overall_rating = DecimalField()
    tags = ListField(StringField())

    def reviews(self):
        return Review.objects.filter(business=self)


def update_business_summary(sender, document, **kwargs):
    # update overall business rating
    rating_sum = Review.objects(business=document.business).sum('rating')
    num_of_ratings = len(Review.objects(business=document.business))
    business = document.business
    business.overall_rating = rating_sum / num_of_ratings

    # update overall business tags
    business.tags.extend(document.tags)
    
    business.save()

signals.post_save.connect(update_business_summary, sender=Review)
