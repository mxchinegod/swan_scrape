def _f(tag, body):
    """
    The function `_f` takes a tag and a body of text, and prints the tag with an associated emoji and
    color code, followed by the body of text.
    
    :param tag: The `tag` parameter is a string that represents the tag for the log message. It can be
    one of the following values: "FATAL", "WARN", "INFO", "WAIT", or "SUCCESS"
    :param body: The `body` parameter is a string that represents the message or content that you want
    to display. It will be printed along with the tag and emoji
    """
    tags = [
        ("FATAL", "☠️", "\033[91m"),  # Red color for FATAL
        ("WARN", "🚨", "\033[93m"),   # Yellow color for WARN
        ("INFO", "ℹ️", "\033[94m"),   # Blue color for INFO
        ("WAIT", "☕️", "\033[96m"),    # Cyan color for WAIT
        ("SUCCESS", "🌊", "\033[92m") # Green color for SUCCESS
    ]
    matching_tags = [x for x in tags if x[0] == tag.upper()]
    if matching_tags:
        tag_text = matching_tags[0][0]
        emoji = matching_tags[0][1]
        color_code = matching_tags[0][2]
        print(f'{color_code}{emoji} {tag_text}: {body}\033[0m')  # Reset color after the text
    else:
        print(f'😭 UNKNOWN TAG - `{tag}`')