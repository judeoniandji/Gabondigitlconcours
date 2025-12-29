from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        iat = validated_token.get('iat')
        if iat is not None and getattr(user, 'token_valid_after', None) is not None:
            try:
                cutoff = int(user.token_valid_after.timestamp())
                if int(iat) < cutoff:
                    raise AuthenticationFailed('Token révoqué', code='token_revoked')
            except Exception:
                pass
        return user
