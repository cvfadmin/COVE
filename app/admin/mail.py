from app import mail, Config
from flask_mail import Message


def send_email(subject, recipients, body):
    msg = Message()

    msg.subject = subject
    msg.recipients = recipients
    msg.body = body

    mail.send(msg)
    return {
        'message': 'Sent Email'
    }


def send_dataset_approval(recipient, d_id):
    subject = "Your COVE dataset submission has been approved!"
    body = "Hello!\n\nThis is a quick email to let you know that your dataset has been approved and is now live at " + \
           str(Config.BASE_URL) + "datasets/" + str(d_id) + " !\n\nThank you for contributing to COVE."

    return send_email(subject, [recipient], body)


def send_dataset_denial(recipient):
    subject = "Your COVE dataset submission."
    body = "Hi,\n\nUnfortunately, your COVE dataset submission has been denied. " \
           "Please feel free to respond with any questions or concerns.\n\nThank you for your time."

    return send_email(subject, [recipient], body)


def send_dataset_to_approve(recipient, dataset_name):
    subject = "A dataset has been submitted to COVE."
    body = "Hi,\n\nA dataset by the name: " + str(dataset_name) + "has been submitted to COVE the and pending approval"\
           + "in the admin panel.\n\nThis is an automated email."

    return send_email(subject, [recipient], body)