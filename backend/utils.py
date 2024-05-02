import re


def format_number_before_save(phone_number):
    if phone_number is not None:
        # Convert to string and remove spaces
        phone_number_str = str(phone_number).replace(" ", "")
        pattern = re.compile(r'^(\+?\d{1,3})?(\d{10})$')

        # Check if the phone number matches the pattern
        match = pattern.match(phone_number_str)
        if match:
            # If the phone number starts with '0', strip it and prepend '+234'
            if match.group(1) == '+234':
                processed_phone_number = phone_number_str
            # If the phone number starts with '0', strip it and prepend '+234'
            elif match.group(1) == '0':
                processed_phone_number = '+234' + match.group(2)
            elif match.group(1) == '234':  # If the phone number starts with '234', add '+'
                processed_phone_number = '+' + match.group(1) + match.group(2)
            else:
                # If it doesn't start with '0' or '234', directly prepend '+234'
                processed_phone_number = '+234' + phone_number_str
        else:
            # If it doesn't match the pattern, handle the error or log it
            print(f"Invalid phone number format: {phone_number_str}")
    else:
        # Handle the case when phone_number is None
        processed_phone_number = None
    return processed_phone_number