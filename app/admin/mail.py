from app import mail, Config
from flask_mail import Message


def send_email(subject, recipients, body):
    if None in recipients:
        return None

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
    body = "Hi,\n\nUnfortunately, your COVE dataset submission has been denied at this time. " \
           "Please feel free to respond with any questions or concerns.\n\nThank you for your time."

    return send_email(subject, [recipient], body)


def send_dataset_to_approve(recipient, dataset_name):
    subject = "A dataset has been submitted to COVE."
    body = "Hi,\n\nA dataset by the name: " + str(dataset_name) + " has been submitted to COVE and is pending approval"\
           + " in the admin panel.\n\nThis is an automated email."

    return send_email(subject, [recipient], body)


def send_edit_request_notification(recipient, dataset_name, d_id):
    subject = "COVE - An admin has requested an edit on your dataset."
    body = "Hi,\n\nAn admin has requested that an edit be made on the dataset: " + dataset_name + ". You may respond"\
        + " to this request here: " + str(Config.BASE_URL) + "datasets/" + str(d_id) + "/edit/requests (You must be"\
        + " logged into the same account used to add the dataset to COVE). Once the edit"\
        + " has been made please reply to the edit request and an admin will respond accordingly."\
        + "\n\nThank you for your time."

    return send_email(subject, [recipient], body)


def send_admin_message_notification(request_id, dataset_id):
    subject = "There has been a reply to edit request: #" + str(request_id)
    body = "Please visit: " + str(Config.BASE_URL) + "datasets/" + str(dataset_id) + "/edit/requests" + " to proceed." \
           + "\n\nThis is an automated email."

    return send_email(subject, [str(Config.NOTIFY_ADMIN_EMAIL)], body)


def send_owner_message_notification(recipient, request_id, dataset_id):
    subject = "COVE - There has been a reply to edit request: #" + str(request_id)
    body = "Hi,\n\nAn admin has sent a reply to an edit request on a dataset you own. Please visit: "\
           + str(Config.BASE_URL) + "datasets/" + str(dataset_id) + "/edit/requests" + " to view the message." \
           + "\n\nThank you for your time."

    return send_email(subject, [recipient], body)
