from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    # Foydalanuvchi uchun refresh tokenini yaratish
    refresh = RefreshToken.for_user(user)

    # Refresh tokenning amal qilish muddatini 10 daqiqaga o'rnatish
    refresh.set_exp(from_time=datetime.now(), lifetime=timedelta(minutes=10))

    # Access tokenning amal qilish muddatini 10 daqiqaga o'rnatish
    refresh.access_token.set_exp(from_time=datetime.now(), lifetime=timedelta(minutes=10))

    # Tokenlarni so'rovga javob sifatida qaytarish
    return {
        "refresh": str(refresh),  # Refresh tokenni string sifatida qaytarish
        "access": str(refresh.access_token),  # Access tokenni string sifatida qaytarish
    }
