from django.contrib import admin
from .models import *
from allauth.socialaccount.models import SocialApp
# Register your models here.
@admin.register(UsersData)
class UsersDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'rank', 'cash_earned', 'wins', 'losses', 'games_played', 'win_rate', 'win_streak', 'Achievements', 'level','slug', 'created_at')
    search_fields = ('user__email', 'user__phone')
    list_filter = ('rank', 'level')

@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'created_at')
    search_fields = ('user__email', 'otp')
    list_filter = ('created_at',)


@admin.register(GameData)
class GameDataAdmin(admin.ModelAdmin):
    list_display = ('game_name', 'game_category', 'game_rating')

@admin.register(PromptGame)
class PromptGameAdmin(admin.ModelAdmin):
    list_display = ('game', 'prompt', 'user_prompt', 'similarity_score', 'created_at')
    search_fields = ('game__game_name', 'prompt')
    list_filter = ('created_at',)

class LudoGameAdmin(admin.ModelAdmin):
    list_display = ('user', 'winner', 'duration')