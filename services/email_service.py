from fastapi import BackgroundTasks
from jinja2 import Environment, FileSystemLoader
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailService:

    @staticmethod
    def render_template(template_name: str, context: dict) -> str:
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template(template_name)
        return template.render(context)

    @staticmethod
    async def send_email_verification(email: str, username: str, code: str) -> None:
        verify_url = f"{os.getenv('APP_URL')}/auth/verify-email?code={code}"

        html = EmailService.render_template("email_verification.html", {
            "code": code,
            "username": username,
            "verification_link": verify_url
        })

        await EmailService.send_email(
            to=email,
            subject="Confirme seu e-mail - UNAS",
            html_content=html
        )
        
    @staticmethod
    async def send_email_reset_password(email: str, username: str, code: str) -> None:
        
        html = EmailService.render_template("email_reset_password.html", {
            "code": code,
            "username": username
        })

        await EmailService.send_email(
            to=email,
            subject="Redefinição de senha - UNAS",
            html_content=html
        )


    @staticmethod
    async def send_email(to: str, subject: str, html_content: str):
        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_pass = os.getenv("SMTP_PASS")

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = to

        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, to, msg.as_string())
