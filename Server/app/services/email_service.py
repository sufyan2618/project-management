import random
from app.core.celery_config import celery_app
import requests
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)



BREVO_API_KEY = settings.BREVO_API_KEY
BREVO_SENDER_EMAIL = settings.BREVO_SENDER_EMAIL
BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


class EmailService:

    @celery_app.task(bind=True, max_retries=3, name="send_email_task")
    def send_email(self, to_email: str, subject: str, html_content: str):
        """Send email using Brevo API"""
        try:
            headers = {
                "api-key": BREVO_API_KEY,
                "Content-Type": "application/json"
            }
            payload = {
                "sender": {
                    "email": BREVO_SENDER_EMAIL,
                    "name": "Project Management <no-reply>"
                },
                "to": [{"email": to_email}],
                "subject": subject,
                "htmlContent": html_content
            }
            response = requests.post(BREVO_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            logger.info(f"Email sent successfully to {to_email}")
        except requests.RequestException as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            raise self.retry(exc=e, countdown=2 ** self.request.retries)
        
    @staticmethod
    def generate_otp() -> str:
        """Generate a 6-digit OTP"""
        return str(random.randint(100000, 999999))




# class EmailService:

#     @staticmethod
#     def generate_otp(self) -> str:
#         """Generate a 6-digit OTP"""
#         return str(random.randint(100000, 999999))


#     @celery_app.task(bind=True, max_retries=3, name="send_verification_email_task")
#     async def send_verification_email(email: str, first_name: str,  otp: str):
#         """Send verification email with OTP"""
#         try:
#             template = env.get_template('email-verification.html')

#             logger.info(f"Preparing verification email for {email}")

#             html = template.render(
#                 otp=otp,
#                 first_name=first_name,
#                 email=email,
#             )
            
#             message = MessageSchema(
#                 subject="Email Verification OTP",
#                 recipients=[email],
#                 body=html,
#                 subtype="html"
#             )
            
#             fm = FastMail(email_conf)
#             await fm.send_message(message)
#             logger.info(f"Verification email sent successfully to {email}")
#         except Exception as e:
#             logger.error(f"Failed to send verification email to {email}: {str(e)}")
#             # Don't raise - allow registration to succeed even if email fails


#     @celery_app.task(bind=True, max_retries=3, name="send_welcome_email_task")
#     async def send_welcome_email(email: str, user_name: str, ):
#         """Send welcome email with verification link"""
#         try:
#             template = env.get_template('welcome-email.html')

#             logger.info(f"Preparing welcome email for {email}")

#             html = template.render(
#                 user_name=user_name,
#                 email=email,
#             )
            
#             message = MessageSchema(
#                 subject="Welcome to Our Platform!",
#                 recipients=[email],
#                 body=html,
#                 subtype="html"
#             )
            
#             fm = FastMail(email_conf)
#             await fm.send_message(message)
#             logger.info(f"Welcome email sent successfully to {email}")
#         except Exception as e:
#             logger.error(f"Failed to send welcome email to {email}: {str(e)}")
#             # Don't raise - allow registration to succeed even if email fails


# # on task assignment, send email to assigned user
#     @celery_app.task(bind=True, max_retries=3, name="send_task_assigned_email_task")
#     async def send_task_assigned_email(email: str, user_name: str, task_name: str):
#         """Send task assigned email"""
#         try:
#             template = env.get_template('task-assigned.html')
#             html = template.render(
#                 user_name=user_name,
#                 task_name=task_name
#             )

#             message = MessageSchema(
#                 subject="Task Assigned Notification",
#                 recipients=[email],
#                 body=html,
#                 subtype="html"
#             )

#             fm = FastMail(email_conf)
#             await fm.send_message(message)
#             logger.info(f"Task assigned email sent to {email}")
#         except Exception as e:
#             logger.error(f"Failed to send task assigned email to {email}: {str(e)}")


# # on task status change, notify project creator about update
#     @celery_app.task(bind=True, max_retries=3, name="send_task_status_update_email_task")
#     async def send_task_status_update_email(email: str, user_name: str, task_name: str, previous_status: str, new_status: str, task_id: int, timestamp: str):
#         """Send task status update email"""
#         try:
#             template = env.get_template('task-status-update.html')
#             html = template.render(
#             user_name=user_name,
#             task_name=task_name,
#             previous_status=previous_status,
#             new_status=new_status,
#             task_id=task_id,
#             timestamp=timestamp
#         )

#             message = MessageSchema(
#                 subject="Task Status Update Notification",
#                 recipients=[email],
#                 body=html,
#                 subtype="html"
#             )

#             fm = FastMail(email_conf)
#             await fm.send_message(message)
#             logger.info(f"Task status update email sent to {email}")
#         except Exception as e:
#             logger.error(f"Failed to send task status update email to {email}: {str(e)}")

