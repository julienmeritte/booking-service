import os
from fastapi import Depends, HTTPException, Request, Query, status
from pydantic import ValidationError

import jwt
import logging
from datetime import datetime


ACCESS_TOKEN_EXPIRE_MINUTES = 1200  # Changer à 1h
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
JWT_REFRESH_SECRET_KEY = os.environ["JWT_REFRESH_SECRET_KEY"]


def verify_token(req: Request):
    try:
        token = req.headers["Authorization"]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No Token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_parsed = str.replace(str(token), "Bearer ", "")
    logging.error(token_parsed)

    try:
        payload = jwt.decode(token_parsed, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        logging.error(payload)

        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except (
        jwt.exceptions.InvalidSignatureError,
        jwt.ExpiredSignatureError,
        ValidationError,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True
