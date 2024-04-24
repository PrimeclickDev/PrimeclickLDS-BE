def intro_response():
    response = '<?xml version="1.0"?>'
    response += '<Response>'
    response += '<GetDigits numDigits="1" finishOnKey="#" timeout="15" callbackUrl="https://coral-app-kajof.ondigitalocean.app/call/user/input">'
    response += '<Say voice="man">'
    response += "Welcome to Primeclick Autoleads voice demo. Please press 1 to continue and 2 to quit."
    response += '</Say>'
    # response += '<Play url="https://od.lk/s/NTZfMjk4NjI0OThf/Primeclick.mp3">'
    # response += '</Play>'
    response += '</GetDigits>'
    response += '</Response>'
    return response