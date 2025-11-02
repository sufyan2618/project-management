# app/services/email_service.py
from fastapi_mail import MessageSchema, MessageType
from app.core.config import settings
from app.core.email import fn  # Changed from 'fn' to 'fm'


async def send_email(
    email_to: str,
    user_name: str,
):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome Email</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #f4f4f7; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        <table role="presentation" style="width: 100%; border-collapse: collapse;">
            <tr>
                <td align="center" style="padding: 40px 0;">
                    <!-- Main Container -->
                    <table role="presentation" style="width: 600px; border-collapse: collapse; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);">
                        
                        <!-- Header -->
                        <tr>
                            <td style="padding: 40px 40px 30px; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px 8px 0 0;">
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600;">
                                    Welcome to Project Management! 🎉
                                </h1>
                            </td>
                        </tr>
                        
                        <!-- Body -->
                        <tr>
                            <td style="padding: 40px;">
                                <p style="margin: 0 0 20px; color: #333333; font-size: 16px; line-height: 1.6;">
                                    Hi <strong>{user_name}</strong>,
                                </p>
                                
                                <p style="margin: 0 0 20px; color: #555555; font-size: 16px; line-height: 1.6;">
                                    We're thrilled to have you on board! Your account has been successfully created, and you're ready to start managing your projects efficiently.
                                </p>
                                
                                <p style="margin: 0 0 30px; color: #555555; font-size: 16px; line-height: 1.6;">
                                    Here's what you can do next:
                                </p>
                                
                                <!-- Feature List -->
                                <table role="presentation" style="width: 100%; margin-bottom: 30px;">
                                    <tr>
                                        <td style="padding: 15px; background-color: #f8f9fa; border-radius: 6px; margin-bottom: 10px;">
                                            <p style="margin: 0; color: #667eea; font-weight: 600; font-size: 15px;">✨ Create Your First Project</p>
                                            <p style="margin: 5px 0 0; color: #666; font-size: 14px;">Start organizing your tasks and collaborating with your team</p>
                                        </td>
                                    </tr>
                                    <tr><td style="height: 10px;"></td></tr>
                                    <tr>
                                        <td style="padding: 15px; background-color: #f8f9fa; border-radius: 6px;">
                                            <p style="margin: 0; color: #667eea; font-weight: 600; font-size: 15px;">👥 Invite Team Members</p>
                                            <p style="margin: 5px 0 0; color: #666; font-size: 14px;">Collaborate seamlessly with your colleagues</p>
                                        </td>
                                    </tr>
                                    <tr><td style="height: 10px;"></td></tr>
                                    <tr>
                                        <td style="padding: 15px; background-color: #f8f9fa; border-radius: 6px;">
                                            <p style="margin: 0; color: #667eea; font-weight: 600; font-size: 15px;">📊 Track Progress</p>
                                            <p style="margin: 5px 0 0; color: #666; font-size: 14px;">Monitor your project milestones in real-time</p>
                                        </td>
                                    </tr>
                                </table>
                                
                                <!-- CTA Button -->
                                <table role="presentation" style="margin: 0 auto;">
                                    <tr>
                                        <td style="text-align: center;">
                                            <a href="http://localhost:3000/dashboard" style="display: inline-block; padding: 14px 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 16px;">
                                                Get Started
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                                
                                <p style="margin: 30px 0 0; color: #777; font-size: 14px; line-height: 1.6;">
                                    If you have any questions or need assistance, feel free to reach out to our support team.
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 30px 40px; background-color: #f8f9fa; border-radius: 0 0 8px 8px; text-align: center;">
                                <p style="margin: 0 0 10px; color: #999; font-size: 13px;">
                                    © 2025 Project Management App. All rights reserved.
                                </p>
                                <p style="margin: 0; color: #999; font-size: 12px;">
                                    Lahore, Punjab, Pakistan
                                </p>
                                <div style="margin-top: 15px;">
                                    <a href="#" style="color: #667eea; text-decoration: none; margin: 0 10px; font-size: 12px;">Privacy Policy</a>
                                    <span style="color: #ddd;">|</span>
                                    <a href="#" style="color: #667eea; text-decoration: none; margin: 0 10px; font-size: 12px;">Terms of Service</a>
                                    <span style="color: #ddd;">|</span>
                                    <a href="#" style="color: #667eea; text-decoration: none; margin: 0 10px; font-size: 12px;">Contact Us</a>
                                </div>
                            </td>
                        </tr>
                        
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    message = MessageSchema(
        subject="Welcome to Project Management!",
        recipients=[email_to],
        body=html_content,
        subtype=MessageType.html
    )
    
    await fn.send_message(message)
