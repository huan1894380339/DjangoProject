from app.models import BlackListedToken
import jwt
from projectnew import settings


def cronjob_blacklist():
    for obj in BlackListedToken.objects.all():
        token = obj.token
        try:
            jwt.decode(
                jwt=token, key=settings.SECRET_KEY,
                algorithms=['HS256'],
            )
        except jwt.ExpiredSignatureError:
            # Signature has expired
            token_expired = BlackListedToken.objects.get(token=token)
            token_expired.delete()
