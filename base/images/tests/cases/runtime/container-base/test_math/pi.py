# SPDX-License-Identifier: MIT
# Pi calculation adapted from https://github.com/MrBlaise/learnpython/blob/master/Numbers/pi.py
"""Spigot-algorithm Pi calculation, run inside the container for compute validation."""

from __future__ import annotations

import time
from collections.abc import Iterator

PI_1000 = (
    "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412"
    "737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051"
    "320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473"
    "035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989"
)

MAX_SECONDS_PER_COMPUTE = 20.0


def calc_pi(limit: int) -> Iterator[object]:
    """Calculate Pi digits one at a time via the spigot algorithm."""
    q, r, t, k, n, step = 1, 0, 1, 1, 3, 3
    counter = 0
    while counter != limit + 1:
        if 4 * q + r - t < n * t:
            yield n
            if counter == 0:
                yield "."
            if limit == counter:
                break
            counter += 1
            nr = 10 * (r - n * t)
            n = ((10 * (3 * q + r)) // t) - 10 * n
            q *= 10
            r = nr
        else:
            nr = (2 * q + r) * step
            nn = (q * (7 * k) + 2 + (r * step)) // (t * step)
            q *= k
            t *= step
            step += 2
            k += 1
            n = nn
            r = nr


def pi_to_places(places: int) -> str:
    """Return Pi, accurate to the given number of decimal places."""
    return "".join(str(d) for d in calc_pi(places))


def verify_pi_1000() -> bool:
    """Check that Pi to 1000 places matches the known reference value."""
    return pi_to_places(1000) == PI_1000


def verify_pi_n_times_1000(nrange: int = 10, mult: int = 1000) -> bool:
    """Repeatedly compute Pi at growing precision and assert performance (max 20s per computation)."""
    for count in range(nrange + 1):
        places = max(count * mult, 3)
        start = time.time()
        answer = pi_to_places(places)
        if len(answer) != places + 2 or time.time() - start > MAX_SECONDS_PER_COMPUTE:
            return False
    return True


if __name__ == "__main__":
    import sys

    checks = {"1000": verify_pi_1000, "n1000": verify_pi_n_times_1000}
    sys.exit(0 if checks[sys.argv[1]]() else 1)
