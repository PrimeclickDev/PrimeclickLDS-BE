def intro_response():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<GetDigits numDigits="1" finishOnKey="#" timeout="5" callbackUrl="https://coral-app-kajof.ondigitalocean.app/call/user/input/">'
    response += '<Say voice="man">'
    response += "Welcome to Primeclick Autoleads voice demo. Please press 1 to continue and 2 to quit."
    response += '</Say>'
    # response += '<Play url="https://www.dropbox.com/scl/fi/1jw1xzn6ho27ju3zyi6dq/Primeclick.mp3">'
    # response += '</Play>'
    response += '</GetDigits>'
    response += '</Response>'
    return response


def positive_flow():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<Say voice="man">'
    response += 'Thank you for showing interest in our product. Will be in touch!'
    response += '</Say>'
    response += '</Response>'
    return response