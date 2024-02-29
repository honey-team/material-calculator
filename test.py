def standard_form(x: str) -> str:
    """
    Converts a string representation of a number to its standard form.

    Args:
        num_str: The string representation of the number.

    Returns:
        The standard form of the number.
    """

    num = float(x)
    exp = 0
    while num >= 10:
        num /= 10
        exp += 1
    while num < 1:
        num *= 10
        exp -= 1

    return f"{num:.5 f} * 10**{exp}"

import flet as ft
def app(page: ft.Page):
    def change(e):
        txt.value = standard_form(e.control.value)
        page.update()
    txt = ft.Text('0')
    page.add(
        ft.TextField(on_change=change),
        txt
    )

ft.app(app)
