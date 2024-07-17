import os

def send_error_email(error_message, sender_email, receiver_email, subject):
    body = (
        f'Dear Team,\n\n'
        f'{subject}:\n\n'
        f'Error Message: {error_message}\n\n'
        f'Please investigate and take necessary actions.\n\n'
        f'Regards,\nETL Team'
    )
    command = f'echo "{body}" | mail -s "{subject}" {receiver_email}'
    
    # Execute the command to send the email
    os.system(command)
    print("Email sent successfully!")
