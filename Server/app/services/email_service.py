from fastapi_mail import FastMail, MessageSchema
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.core.email import conf as email_conf

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates" / "email"

# Setup Jinja2 environment
env = Environment(
    loader=FileSystemLoader(searchpath=str(TEMPLATES_DIR)),
    autoescape=select_autoescape(['html', 'xml'])
)

class EmailService:
    @staticmethod
    async def send_welcome_email(email: str, user_name: str, ):
        """Send welcome email with verification link"""
        template = env.get_template('welcome-email.html')

        print("Preparing welcome email...", email, user_name)

        html = template.render(
            user_name=user_name,
            email=email,
        )
        
        message = MessageSchema(
            subject="Welcome to Our Platform!",
            recipients=[email],
            body=html,
            subtype="html"
        )
        
        fm = FastMail(email_conf)
        await fm.send_message(message)


# on task assignment, send email to assigned user
    @staticmethod
    async def send_task_assigned_email(email: str, user_name: str, task_name: str):
        """Send task assigned email"""
        template = env.get_template('task-assigned.html')
        html = template.render(
            user_name=user_name,
            task_name=task_name
        )

        message = MessageSchema(
            subject="Task Assigned Notification",
            recipients=[email],
            body=html,
            subtype="html"
        )

        fm = FastMail(email_conf)
        await fm.send_message(message)


# on task status change, notify project creator about update
    @staticmethod
    async def send_task_status_update_email(email: str, user_name: str, task_name: str, previous_status: str, new_status: str, task_id: int, timestamp: str):
        """Send task status update email"""
        template = env.get_template('task-status-update.html')
        html = template.render(
        user_name=user_name,
        task_name=task_name,
        previous_status=previous_status,
        new_status=new_status,
        task_id=task_id,
        timestamp=timestamp
    )

        message = MessageSchema(
            subject="Task Status Update Notification",
            recipients=[email],
            body=html,
            subtype="html"
        )

        fm = FastMail(email_conf)
        await fm.send_message(message)

