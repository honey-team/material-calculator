from math import log as loga

import flet as ft

from pages.utils.const import INPUT_FILTER, S
from pages.utils.memory import mload, mwrite
from pages.utils.number import Number, get_low


def log(page: ft.Page):
    def get_log(a, b):
        return loga(b, a)

    def get_log10(b):
        return loga(b, 10)

    def get_ln(b):
        return loga(b)

    LOG = "log{a} {b} = {x}"
    LOG10 = "log {b} = {x}"
    LN = "ln {b} = {x}"

    def change_memory(*_):
        m = mload()
        m["pages"]["log"]["a"] = a.value
        m["pages"]["log"]["b"] = b.value
        mwrite(m)

    def change_args(*_):
        try:
            log.value = S(LOG.format(
                a=get_low(Number(a.value)), b=Number(b.value), x=get_log(float(Number(a.value)), float(Number(b.value)))
            ))
            log10.value = S(LOG10.format(b=Number(b.value), x=get_log10(float(Number(b.value)))))
            ln.value = S(LN.format(b=Number(b.value), x=get_ln(float(Number(b.value)))))
            page.update()
        except:
            log.value = S(LOG.format(a=get_low(Number(a.value)), b=Number(b.value), x="?"))
            log10.value = S(LOG10.format(b=Number(b.value), x="?"))
            ln.value = S(LN.format(b=Number(b.value), x="?"))
            page.update()
        change_memory()

    m = mload()
    a = ft.TextField(
        value=m["pages"]["log"]["a"], label=S("Основание логарифма"), on_change=change_args, input_filter=INPUT_FILTER
    )
    b = ft.TextField(
        value=m["pages"]["log"]["b"], label=S("Число логарифма"), on_change=change_args, input_filter=INPUT_FILTER
    )

    log = ft.Text(S(LOG.format(a=get_low(Number(a.value)), b=Number(b.value), x="?")), size=20)
    log10 = ft.Text(S(LOG10.format(b=Number(b.value), x=get_log10(float(Number(b.value))))), size=20)
    ln = ft.Text(S(LN.format(b=Number(b.value), x=get_ln(float(Number(b.value))))), size=20)

    page.add(a, b, log, log10, ln)

    return 20
