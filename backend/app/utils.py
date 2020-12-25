import uuid

def generate_uuid(length):
    """Generates hex uuid with customized length.
    Example: d9f3a7e8

    Args:
        length (int): number of digits of uuid
    """
    return str(uuid.uuid4().hex)[:length]
