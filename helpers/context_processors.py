import json

from helpers.jwt_utils import create_jwt_token


def conduit_debug(request):
    """Context processor that provides data for window.__conduit_debug__ interface.

    The HTMX views use Django session auth, but the e2e test suite
    expects window.__conduit_debug__ with a JWT token for API calls.
    """
    if request.user.is_authenticated:
        token = request.session.get("jwt_token")
        if not token:
            token = str(create_jwt_token(request.user, request))
            request.session["jwt_token"] = token
        user_data = {
            "username": request.user.username,
            "email": request.user.email,
            "bio": request.user.bio or None,
            "image": request.user.image or None,
            "token": token,
        }
        return {
            "conduit_user_json": json.dumps(user_data),
            "conduit_token": token,
        }
    return {
        "conduit_user_json": "null",
        "conduit_token": "",
    }
