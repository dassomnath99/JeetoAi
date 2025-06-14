from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class UsersData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userdata')
    phone = models.CharField(max_length=10, unique=True, null=True, blank=True)
    rank = models.IntegerField(blank=True, null=True, default=0)
    cash_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    win_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    win_streak = models.IntegerField(default=0)
    Achievements = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default.jpg')
    level = models.CharField(max_length=50,choices=[
        ('Novice','Novice'),
        ('Pattern Seeker','Pattern Seeker'),
        ('Neural Thinker','Neural Thinker'),
        ('Prompt Decoder','Prompt Decoder'),
        ('Human GPT','Human GPT'),
        ('Prompt Architect','Prompt Architect'),
        ('GOD OF AI','GOD OF AI'),
    ],default='Novice')
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}"

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"OTP for user ID {self.user.id}"

    
class GameData(models.Model):
    game_name = models.CharField(max_length=100)
    game_description = models.TextField()
    game_image = models.ImageField(upload_to='game_images/')
    game_category = models.CharField(max_length=50, choices=[
        ('FPS', 'FPS'),
        ('Strategy', 'Strategy'),
        ('RPG', 'RPG'),
        ('Adventure', 'Adventure'),
        ('Racing', 'Racing'),
        ('Sports', 'Sports'),
    ], default='FPS')
    game_players = models.IntegerField(default=1)
    game_duration = models.DurationField(default=timezone.timedelta(minutes=30))
    game_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    created_at = models.DateField(null=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            super().save(*args, **kwargs)
            self.slug = f"{self.game_name.replace(' ', '-').lower()}-{self.id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.game_name}"

class PromptGame(models.Model):
    game = models.ForeignKey(GameData, on_delete=models.CASCADE, related_name='prompt_games')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prompt_games')
    prompt = models.TextField()
    image = models.ImageField(upload_to='prompt_images/', null=True, blank=True)
    user_prompt = models.TextField(null=True, blank=True)
    similarity_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Prompt for {self.game.game_name} - {self.prompt[:50]}..."

class LudoGame(models.Model):
    game = models.ForeignKey(GameData, on_delete=models.CASCADE, related_name='ludo_games')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ludo_games')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ludo_wins', null=True, blank=True)
    moves = models.JSONField(default=list, blank=True)
    duration = models.DurationField(default=timezone.timedelta(minutes=30))

    def __str__(self):
        return f"Ludo Game for {self.user.username}"