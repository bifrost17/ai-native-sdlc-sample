"""AC0: Preserve the subtotal of integer amounts."""
def subtotal(amounts):
    return sum(amounts)


def payable(amounts, discount_percent):
    """Return the subtotal after applying a percentage discount."""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("discount_percent must be between 0 and 100")

    total = subtotal(amounts)
    discount = total * discount_percent // 100
    return total - discount
