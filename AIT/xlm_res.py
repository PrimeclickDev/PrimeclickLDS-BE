def intro_response(content1, user_name):  # Accepting content and the user's name
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<GetDigits numDigits="1" finishOnKey="#" timeout="5" callbackUrl="https://coral-app-kajof.ondigitalocean.app/call/user/input/">'

    # Check if the content is an audio file or text
    if content1.endswith(('.mp3', '.wav', '.ogg')):
        # If it's an audio file, use the url attribute in the Play tag
        response += f'<Play url="{content1}"/>'
    else:
        # If it's text, replace the {user_name} placeholder if present
        full_content = content1.replace("{user_name}", user_name) if "{user_name}" in content1 else content1
        response += f'<Say voice="woman">{full_content}</Say>'

    response += '</GetDigits>'
    response += '</Response>'

    return response


def positive_record(content2):
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Record finishOnKey="#" maxLength="25" trimSilence="true" playBeep="true" callbackUrl="https://coral-app-kajof.ondigitalocean.app/record/call/">'

    # Check if content2 is an audio file
    if content2.endswith(('.mp3', '.wav', '.ogg')):
        # Use the url attribute in the Play tag
        response += f'<Play url="{content2}"/>'
    else:
        # Otherwise, treat it as text and use Say tag
        response += f'<Say voice="man">{content2}</Say>'

    response += '</Record>'
    response += '</Response>'

    return response


def thank_you(content3):
    response = '<?xml version="1.0" encoding="UTF-8"?>'
    response += '<Response>'

    # Check if content3 is an audio file
    if content3.endswith(('.mp3', '.wav', '.ogg')):
        # Use the url attribute in the Play tag
        response += f'<Play url="{content3}"/>'
    else:
        # Otherwise, treat it as text and use Say tag
        response += f'<Say voice="man">{content3}</Say>'

    response += '</Response>'

    return response


def handle_inbound(content4):
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Say voice="man">'
    response += f"{content4}"
    response += '</Say>'
    response += '</Response>'
    return response

def default_handle_inbound():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Say voice="man">'
    response += "Thank you for calling Autoleads. Our customer support will be in touch. Thanks again!"
    response += '</Say>'
    response += '</Response>'
    return response
