import smtplib, logging
from email.message import EmailMessage
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message 
from aiogram import Router
from aiogram import F

logging.basicConfig(level=logging.INFO)

SMTP = 'smtp@gmail.com'
SMTP_PORT = 587
SMTP_SENDER_EMAIL = True 