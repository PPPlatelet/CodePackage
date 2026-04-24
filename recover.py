from decimal import Decimal, ROUND_CEILING

def recover_counts(percentages, max_total=20000):
    p = [Decimal(str(x)) for x in percentages]
    solutions = []
    hundred = Decimal("100")
    half_step = Decimal("0.005")

    for N in range(1, max_total + 1):
        lowers = []
        uppers = []
        ok = True

        for target in p:
            low_pct = target - half_step
            high_pct = target + half_step

            low_raw = Decimal(N) * low_pct / hundred
            high_raw = Decimal(N) * high_pct / hundred

            lo = int(low_raw.to_integral_value(rounding=ROUND_CEILING))
            hi = int(high_raw.to_integral_value(rounding=ROUND_CEILING)) - 1

            lo = max(0, lo)
            hi = min(N, hi)

            if lo > hi:
                ok = False
                break

            lowers.append(lo)
            uppers.append(hi)

        if not ok:
            continue

        sum_lo = sum(lowers)
        sum_hi = sum(uppers)
        if not (sum_lo <= N <= sum_hi):
            continue

        ans = lowers[:]
        rem = N - sum_lo
        for i in range(len(ans)):
            if rem == 0:
                break
            take = min(rem, uppers[i] - lowers[i])
            ans[i] += take
            rem -= take

        solutions.append((N, ans))

    return solutions


arr1 = [16.95, 25.42, 8.48, 10.17, 38.98]
arr2 = [42.37, 13.56, 6.78, 5.09, 32.2]
arr3 = [55.93, 13.56, 6.78, 6.78, 16.95]
sol1 = recover_counts(arr1, max_total=1000)
sol2 = recover_counts(arr2, max_total=1000)
sol3 = recover_counts(arr3, max_total=1000)

print("solutions for arr1:", sol1[:10])
print("count for arr1:", len(sol1))
print("solutions for arr2:", sol2[:10])
print("count for arr2:", len(sol2))
print("solutions for arr3:", sol3[:10])
print("count for arr3:", len(sol3))