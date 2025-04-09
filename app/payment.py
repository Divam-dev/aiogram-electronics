import os
from aiogram.types import LabeledPrice
from dotenv import load_dotenv

load_dotenv()

PROVIDER_TOKEN = os.getenv("REDSYS_PROVIDER_TOKEN", "2051251535:TEST:OTk5MDA4ODgxLTAwNQ")

def create_redsys_invoice(order_data, user_data):
    """
    Create payment invoice data using Redsys payment system
    
    Args:
        order_data: Dictionary containing the order items
        user_data: Dictionary containing user information
    
    Returns:
        Dictionary with payment details for Telegram's native payment API
    """
    # Calculate total amount
    total_amount = 0
    product_descriptions = []
    
    for flower_name, item in order_data.items():
        quantity = item["quantity"]
        price = float(item["price"])
        total_amount += price * quantity
        product_descriptions.append(f"{flower_name} x{quantity}")
    
    # Format for Redsys
    currency_code = user_data.get("currency_code", "UAH")
    total_amount_integer = int(total_amount * 100)  # Convert to kopecks/cents
    
    # Create a unique order reference
    chat_id = user_data.get("chat_id")
    order_reference = f"order_{chat_id}_{int(os.urandom(4).hex(), 16)}"
    
    # Create product description
    description = ", ".join(product_descriptions)
    if len(description) > 100:
        description = description[:97] + "..."
    
    # Create invoice data for Telegram's payment API
    invoice_data = {
        "provider_token": PROVIDER_TOKEN,
        "title": "Flower Order",
        "description": description,
        "currency": currency_code,
        "prices": [LabeledPrice(label="Total", amount=total_amount_integer)],
        "payload": order_reference,
        "need_name": True,
        "need_phone_number": True,
        "need_email": True
    }
    
    return {
        "invoice_data": invoice_data,
        "orderReference": order_reference,
        "reason": "Ok"
    }