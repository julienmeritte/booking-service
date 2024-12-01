from fastapi import APIRouter
from fastapi import Query
from fastapi.responses import JSONResponse

import app.models.hotel as HotelModel
import app.models.additional_service as AdditionalServiceModel
import app.models.hotel_room as HotelRoomModel
import app.models.reservation as ReservationModel
import app.models.reservation_additional_service as ReservationAdditionalServiceModel
import app.models.room_category as RoomCategoryModel

import app.sql_engine as db
from app.routes import router

import logging
import smtplib
from email.mime.text import MIMEText
import os


router = APIRouter(
    prefix="/mail",
    tags=["Mail"],
    responses={404: {"description": "Not found"}},
)


port = 465

sender = "clo5amneos@gmail.com"
recipients = []
password = os.environ["GMAIL_PWD"]


@router.get("/subscription")
async def subscription_mail(destinataire: str):
    msg = MIMEText("Bienvenue chez Clo5. Vous vous êtes inscrit avec succès.")
    msg["Subject"] = "Inscription à CLO5"
    msg["From"] = sender
    msg["To"] = destinataire
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, destinataire, msg.as_string())
    print("Message sent!")
    return {"status": "Mail successfully sent."}
