"""Every number printed in the book that is computed (not quoted) comes from here."""
from datetime import datetime, timedelta


def bedtime(wake, hours):
    t = datetime.strptime(wake, "%H.%M") - timedelta(hours=hours)
    return t.strftime("%H.%M")


SLEEP_TABLE = [(w, bedtime(w, 9), bedtime(w, 10)) for w in ("05.00", "05.30", "06.00")]
READ_15_30 = 15 * 30            # menit membaca dalam 30 hari
READ_15_30_H = READ_15_30 / 60  # jam
WATER_GLASS = 1650 / 200        # gelas 200 mL untuk AKG 1.650 mL
# Isi Piringku proportions of a whole plate
PLATE = {"sayur": 1/2 * 2/3, "buah": 1/2 * 1/3, "pokok": 1/2 * 2/3, "lauk": 1/2 * 1/3}

if __name__ == "__main__":
    print("SLEEP_TABLE", SLEEP_TABLE)
    print("bangun 05.30 tidur 9 jam ->", bedtime("05.30", 9))
    print("READ", READ_15_30, "menit =", READ_15_30_H, "jam")
    print("WATER_GLASS", round(WATER_GLASS, 2))
    print("PLATE", {k: round(v, 3) for k, v in PLATE.items()}, "sum", sum(PLATE.values()))
