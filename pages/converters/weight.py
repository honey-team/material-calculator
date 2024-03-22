from pages.utils.number import Number


def weight():
    def a(x: Number, a_t: int, b_t: int):
        pows = [-3, 0, 3, 6]

        p = Number(str(pows[a_t] - pows[b_t]))

        res = (10**p) * x
        return res

    return {
        "name": "Масса",
        "size": 20,
        "image": "weight_outlined.png",
        "sel_image": "weight.png",
        "types": ["миллиграмм", "грамм", "килограмм", "тонна"],
        "function": a,
        "mem_name": "weight",
    }
