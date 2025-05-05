#!/usr/bin/env python3
"""
Test script for verifying Gmail SMTP connection using environment variables.
Run this script to test if your email configuration is working correctly.
"""

import os
import sys
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_email_connection(recipient_email=None):
    """
    Test the email connection using environment variables.

    Args:
        recipient_email (str, optional): Email address to send test message to.
            If not provided, sends to the sender's own email.

    Returns:
        bool: True if successful, False otherwise
    """
    # Load environment variables
    load_dotenv()

    # Get email configuration
    email_sender = os.getenv("EMAIL_SENDER")
    email_password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    # Verify configuration
    if not email_sender:
        logger.error("EMAIL_SENDER not found in environment variables")
        return False

    if not email_password:
        logger.error("EMAIL_PASSWORD not found in environment variables")
        return False

    # If recipient not specified, send to self
    if not recipient_email:
        recipient_email = email_sender

    try:
        logger.info(f"Testing connection to {smtp_server}:{smtp_port}")
        logger.info(f"Using sender email: {email_sender}")

        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = recipient_email
        msg['Subject'] = "Test Email - Gmail Connection"

        # Email body
        body = """
        <html>
        <body>
            <h2>Gmail Connection Test</h2>
            <p>This is a test email to verify that your Gmail SMTP settings are working correctly.</p>
            <p>If you're seeing this message, your configuration is working!</p>
            <hr>
            <p>Configuration details:</p>
            <ul>
                <li>SMTP Server: {}</li>
                <li>SMTP Port: {}</li>
                <li>Sender: {}</li>
            </ul>
        </body>
        </html>
        """.format(smtp_server, smtp_port, email_sender)

        msg.attach(MIMEText(body, 'html'))

        # Connect to SMTP server
        logger.info("Connecting to SMTP server...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Start TLS encryption
            logger.info("Starting TLS encryption...")
            server.starttls()

            # Login
            logger.info("Logging in...")
            server.login(email_sender, email_password)

            # Send email
            logger.info(f"Sending test email to {recipient_email}...")
            server.send_message(msg)

        logger.info("Email sent successfully!")
        logger.info(f"Check {recipient_email} for the test message")
        return True

    except Exception as e:
        logger.error(f"Error testing email connection: {str(e)}")
        return False


if __name__ == "__main__":
    # Check if recipient email was provided as command-line argument
    recipient_email = sys.argv[1] if len(sys.argv) > 1 else None

    print("=== Gmail Connection Test ===")
    print("This script will test your Gmail SMTP settings from your .env file.")
    print("If successful, a test email will be sent.")

    if not recipient_email:
        print("\nNo recipient email provided. The test email will be sent to your sender address.")
        response = input("Enter a different recipient email (or press ENTER to continue): ")
        if response.strip():
            recipient_email = response.strip()

    print("\nTesting connection...")
    success = test_email_connection(recipient_email)

    if success:
        print("\n✅ Connection test successful! Check your email for the test message.")
    else:
        print("\n❌ Connection test failed. Please check your .env configuration and error messages above.")
        print("\nCommon issues:")
        print("1. Incorrect EMAIL_PASSWORD (make sure you're using an App Password, not your regular password)")
        print("2. 2-Step Verification not enabled on your Google account")
        print("3. Less secure app access is disabled (need to use App Password instead)")
        print("4. Network or firewall blocking the connection")