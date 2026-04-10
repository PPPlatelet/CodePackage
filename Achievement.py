import numpy as np

def get_tolerance():
    print("请输入误差阈值（例如 0.005），直接回车使用默认值 0.005：")
    line = input().strip()
    if line == "":
        return 0.005
    try:
        tol = float(line)
        if tol <= 0:
            print("误差阈值必须为正数，使用默认值 0.005。")
            return 0.005
        return tol
    except ValueError:
        print(f"无效输入 '{line}'，使用默认值 0.005。")
        return 0.005

def get_rates_from_input():
    """从用户输入读取浮点数，直到空行"""
    print("请输入成就达成率（百分比，如 46.12），每行一个，输入空行结束：")
    rates = []
    while True:
        line = input().strip()
        if not line:
            break
        try:
            val = float(line)
            rates.append(val)
        except ValueError:
            print(f"无效输入 '{line}'，请重新输入一个数字，或直接回车结束。")
    return rates

def find_candidates(rates, tolerance = 0.005, max_N = 10_000_000, batch_size = 1_000_000):
    """向量化搜索满足所有成就显示精度的 N"""
    rates = np.array(rates)
    if rates.size == 0:
        return []

    # 预计算 r/100，避免重复除法
    r_over_100 = rates[:, None] / 100.0

    candidates = []
    for start in range(1, max_N + 1, batch_size):
        end = min(start + batch_size, max_N + 1)
        N_batch = np.arange(start, end, dtype=np.float64)

        # 计算 x = round(r * N / 100)
        x = np.round(r_over_100 * N_batch)   # 广播：(len(rates), batch_size)

        # 反向计算百分比并与原始 r 比较
        back_pct = 100.0 * x / N_batch
        errors = np.abs(back_pct - rates[:, None])

        # 检查所有成就误差 <= tolerance
        ok_mask = np.all(errors <= tolerance, axis=0)

        candidates.extend(N_batch[ok_mask].astype(int).tolist())

    return candidates

def main():
    tolerance = get_tolerance()
    print(f"使用误差阈值: {tolerance}")

    rates = get_rates_from_input()
    if not rates:
        print("未输入任何有效百分比，程序结束。")
        input("按回车键退出...")
        return

    print(f"正在搜索 1 ~ 10,000,000 范围内的候选总玩家数...")
    candidates = find_candidates(rates, tolerance)

    print(f"\n找到 {len(candidates)} 个候选 N")
    if candidates:
        # 显示前 10 个，若太多则只显示示例
        if len(candidates) > 10:
            print(f"示例（前10个）：{candidates[:10]}")
        else:
            print(f"全部候选：{candidates}")
    else:
        print("未找到任何符合条件的 N，请检查输入百分比是否合理。")
    
    # 等待用户按键后退出
    input("按回车键退出...")

if __name__ == "__main__":
    main()