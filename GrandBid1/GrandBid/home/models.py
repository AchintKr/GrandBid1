from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.utils import timezone

User = get_user_model()

class Organiser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    organization_name = models.CharField(max_length=100)

    def __str__(self):
        return self.organization_name


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organiser = models.ForeignKey(Organiser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    base_price = models.IntegerField(default=10)
    max_credits_per_team = models.IntegerField(default=100)

    def __str__(self):
        return self.title


class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    purchase_price = models.IntegerField(default=0)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Bider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100)
    team_description = models.TextField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.team_name


class TeamRegistration(models.Model):
    team = models.ForeignKey(Bider, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    credits_remaining = models.IntegerField()
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'event')

    def __str__(self):
        return f"{self.team.team_name} -> {self.event.title}"


class AuctionBid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Bider, on_delete=models.CASCADE)
    bid_amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team.team_name} bid ₹{self.bid_amount} for {self.player.name}"


class TeamPlayer(models.Model):
    team = models.ForeignKey(Bider, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    purchase_price = models.IntegerField()

    class Meta:
        unique_together = ('team', 'event', 'player')

    def __str__(self):
        return f"{self.player.name} -> {self.team.team_name} @ ₹{self.purchase_price}"

# ---------------------------
# Optional Expansion Models
# ---------------------------

class EventRules(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    min_bid = models.IntegerField(default=10)
    bid_increment = models.IntegerField(default=5)
    max_players_per_team = models.IntegerField(default=11)

    def __str__(self):
        return f"Rules for {self.event.title}"


class NotificationLog(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification to {self.recipient.username}"


class AuctionStatus(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    is_live = models.BooleanField(default=False)
    has_ended = models.BooleanField(default=False)
    current_player_on_bid = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Auction Status for {self.event.title}"


class UploadBatchLog(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(Organiser, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    success_count = models.IntegerField()
    failure_count = models.IntegerField()

    def __str__(self):
        return f"{self.file_name} uploaded by {self.uploaded_by.organization_name}"