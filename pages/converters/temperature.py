from pages.utils.number import Number


def temperature():
    def a(x: Number, a_t: int, b_t: int):
        K = 0
        match a_t:
            case 0:
                K = x
            case 1:
                K = x + 273.15
            case 2:
                K = (x + 459.67) * 5 / 9
            case 3:
                K = x / 0.8 + 273.15

        match b_t:
            case 0:
                return K
            case 1:
                return K - 273.15
            case 2:
                return K * 1.8 - 459.67
            case 3:
                return 0.8 * (K - 273.15)

    return {
        "name": "Температура",
        "size": 20,
        "image": "temperature.png",
        "sel_image": "temperature.png",
        "types": ["кельвин (K)", "градус Цельсия (°С)", "градус Фаренгейта (°F)", "Градус Реомюра (°R)"],
        "function": a,
        "mem_name": "temperature",
    }
