import flet as ft

from pages.utils.const import S
from pages.utils.memory import mload, mwrite
from pages.utils.number import Number


def quadratic(page: ft.Page) -> tuple[str, int]:
    txt = ft.Text(S("1x² + 2x + 3 = 0"), size=20)

    def on_change(*_):
        m = mload()
        m["pages"]["quadratic"]["a"] = a.value
        m["pages"]["quadratic"]["b"] = b.value
        m["pages"]["quadratic"]["c"] = c.value
        mwrite(m)

        ia = Number(x1) if (x1 := a.value) else 0
        ib = Number(x2) if (x2 := b.value) else 0
        ic = Number(x3) if (x3 := c.value) else 0

        sa = f"{ia}x²" if int(ia) > 0 else "" if int(ia) == 0 else f"{ia}x²"
        sb = f" + {ib}x" if int(ib) > 0 else "" if int(ib) == 0 else f' - {str(ib).replace("-", "")}x'
        sc = f" + {ic}" if int(ic) > 0 else "" if int(ic) == 0 else f' - {str(ic).replace("-", "")}'

        if not sa:
            if not sb:
                if not sc:
                    sc = "0"
                else:
                    sc = sc.replace("+ ", "")
            else:
                sb = sb.replace("+ ", "")
        txt.value = S(f"{sa}{sb}{sc} = 0")

        D = ib**2 - 4 * ia * ic
        d.value = S(f'D = b² - 4ac = ({ib})² - 4 × {ia if int(ia) > 0 else f"({ia})"} × {ic if int(ic) > 0 else f"({ic})"} = {D}')

        if int(D) < 0:
            r.value = S("Корней нет!")
        else:
            x1 = (-int(ib) + (D**0.5)) / (2 * ia)
            x2 = (-int(ib) - (D**0.5)) / (2 * ia)

            if int(D) == 0:
                r.value = S(f"x = (-b ± √D) / 2a = -{ib} ± √{D}) / 2*{ia} = {x1}")
            else:
                r.value = S(f"""x = (-b ± √D) / 2a = -{ib} ± √{D}) / 2*{ia}

x₁ = {x1}
x₂ = {x2}
""")

        page.update()

    m = mload()
    a = ft.TextField(
        label=S("a"),
        on_change=on_change,
        value=m["pages"]["quadratic"]["a"],
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9,.-]", replacement_string=""),
        border_color='primary,0.5'
    )
    b = ft.TextField(
        label=S("b"),
        on_change=on_change,
        value=m["pages"]["quadratic"]["b"],
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9,.-]", replacement_string=""),
        border_color='primary,0.5'
    )
    c = ft.TextField(
        label=S("c"),
        on_change=on_change,
        value=m["pages"]["quadratic"]["c"],
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9,.-]", replacement_string=""),
        border_color='primary,0.5'
    )

    ia = Number(x1) if (x1 := a.value) else 0
    ib = Number(x2) if (x2 := b.value) else 0
    ic = Number(x3) if (x3 := c.value) else 0

    D = ib**2 - 4 * ia * ic
    d = ft.Text(
        S(f'D = b² - 4ac = {ib**2} - 4 × {ia if int(ia) > 0 else f"({ia})"} × {ic if int(ic) > 0 else f"({ic})"} = {D}'),
        size=20,
    )

    r = ft.Text("", size=18)
    if int(D) < 0:
        r.value = S("Корней нет!")
    else:
        x1 = (-int(ib) + (D**0.5)) / (2 * ia)
        x2 = (-int(ib) - (D**0.5)) / (2 * ia)

        if int(D) == 0:
            r.value = S(f"x = (-b ± √D) / 2a = -{ib} ± √{D}) / 2*{ia} = {x1}")
        else:
            r.value = S(f"""x = (-b ± √D) / 2a = -{ib} ± √{D}) / 2*{ia}

x₁ = {x1}; x₂ = {x2}
""")

    page.add(txt, ft.Container(height=10), a, b, c, d, r)

    return 15
