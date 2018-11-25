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


def send_add_ds_request_approval(recipient, key):
    subject = "You can now add your dataset to COVE!"
    body = "Hello!\n\nThis is a quick email to let you know that your request to add a dataset has been approved." + \
           " Please fill out the form here for final consideration:" + Config.BASE_URL + 'datasets/create/' + \
           str(key) + " !\n\nThank you for contributing to COVE."

    return send_email(subject, [recipient], body)


def send_add_ds_request_denial(recipient):
    subject = "Your request to add a dataset to COVE."
    body = "Hi,\n\nUnfortunately, we will not be accepting your request at this time. " + \
           "Please feel free to respond with any questions or concerns.\n\nThank you for your time."

    return send_email(subject, [recipient], body)


def send_delete_ds_request_approval(recipient):
    subject = "COVE - Your request to delete a dataset has gone through."
    body = "Hello!\n\nThis is just a quick email to let you know that your request to have a dataset deleted" + \
           " has been approved. Please feel free to respond with any questions or concerns." + \
           "!\n\nThank you for contributing to COVE."

    return send_email(subject, [recipient], body)


def send_delete_ds_request_denial(recipient):
    subject = "COVE - Your request to delete a dataset."
    body = "Hi,\n\nUnfortunately, we will not be accepting your request to delete a dataset at this time." + \
           " Please feel free to respond with any questions or concerns.\n\nThank you for your time."

    return send_email(subject, [recipient], body)


def send_edit_ds_request_approval(recipient):
    subject = "COVE - Your request to edit a dataset."
    body = "Hello!\n\nThis is just a quick email to let you know that your request to have a dataset edited" + \
           " has been approved. We will be in touch to confirm any edits. Please feel free to respond with any" + \
           "questions or concerns. !\n\nThank you for contributing to COVE."

    return send_email(subject, [recipient], body)


def send_edit_ds_request_denial(recipient):
    subject = "COVE - Your request to edit a dataset."
    body = "Hi,\n\nUnfortunately, we will not be accepting your request to edit a dataset at this time." + \
           " Please feel free to respond with any questions or concerns.\n\nThank you for your time."
    return send_email(subject, [recipient], body)
