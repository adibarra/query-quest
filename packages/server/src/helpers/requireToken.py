# @author: adibarra (Alec Ibarra)
# @description: Helper function to require a token for a request

from fastapi import Header, HTTPException, status
from helpers.types import SessionDict
from services.database import Database

db = Database()

async def requireToken(
    authorization: str = Header(...),
) -> SessionDict:
    """
    Validates the provided Authorization token and returns a dictionary containing the validated token owner and the token itself.

    This function checks if the Authorization header is properly formatted as "Bearer <token>", validates if the
    token exists in the database, and returns a dictionary with the token owner (associated with the token) and the token.

    If the Authorization header is missing or improperly formatted, a 400 Bad Request HTTPException is raised.
    If the token is invalid or not found in the database, a 401 Unauthorized HTTPException is raised.

    Args:
        authorization (str): The Authorization header passed in the request, typically in the format "Bearer <token>".

    Returns:
        SessionDict: A validated dictionary containing:
            - "user_uuid" (str): The owner of the token.
            - "token" (str): The token.

    Raises:
        HTTPException: If the Authorization header is missing or improperly formatted (400 Bad Request).
        HTTPException: If the token is invalid or not found in the database (401 Unauthorized).
    """
    try:
        # Split and validate the Authorization header
        parts = authorization.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad Request: Missing or Malformed Authorization Header",
            )

        # Extract the token
        token = parts[1]

        # Retrieve the session from the database
        session = db.get_session(token=token)

        if session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized: Invalid or Expired Token",
            )

        return session
    except HTTPException:
        # Re-raise expected HTTP exceptions
        raise
    except Exception as e:
        # Log unexpected exceptions for debugging
        print(f"Unexpected error in requireToken: {e}", flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error: Unexpected error during token validation",
        )
