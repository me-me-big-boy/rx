from decimal import Decimal

from django import template


register = template.Library()


@register.filter
def fmt_dec(val: Decimal) -> Decimal:
    """
    Drop the fractional portion of a decimal value if the value is an
    integer.
    """

    return int_val if (int_val := val.to_integral_value()) == val else val
