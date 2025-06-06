from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bidding(models.Model):
    bid = models.FloatField(default=0, blank=True, null=True)
    bidded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder", blank=True, null=True)

class Listing(models.Model):
    listing_name = models.CharField(max_length=64, blank=True, null=True)
    image_url = models.CharField(max_length=300, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    price = models.ForeignKey(Bidding, on_delete=models.CASCADE, related_name="bid_price", blank=True, null=True)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", blank=True, null=True)
    category = models.CharField(max_length=64, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True, default=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist_listing")

class Comment(models.Model):
    listing_name = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_on", blank=True, null=True)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter", blank=True, null=True)
    comment = models.CharField(max_length=512, blank=True, null=True)