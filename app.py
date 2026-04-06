import gradio as gr
import pandas as pd
import random


def parse_numbers(text):
    parts = [p.strip() for p in text.split(",")]
    numbers = []
    for part in parts:
        if part == "":
            continue
        numbers.append(int(part))
    return numbers



def binary_search_steps(arr, target):
    low = 0
    high = len(arr) - 1
    steps = []

    while low <= high:
        mid = (low + high) // 2
        mid_value = arr[mid]

        if mid_value == target:
            steps.append(
                {
                    "low": low,
                    "high": high,
                    "mid": mid,
                    "mid_value": mid_value,
                    "status": "found",
                    "decision": f"Found {target} at index {mid}."
                }
            )
            return True, mid, steps

        if target < mid_value:
            steps.append(
                {
                    "low": low,
                    "high": high,
                    "mid": mid,
                    "mid_value": mid_value,
                    "status": "left",
                    "decision": f"{target} < {mid_value}, so move left."
                }
            )
            high = mid - 1
        else:
            steps.append(
                {
                    "low": low,
                    "high": high,
                    "mid": mid,
                    "mid_value": mid_value,
                    "status": "right",
                    "decision": f"{target} > {mid_value}, so move right."
                }
            )
            low = mid + 1

    steps.append(
        {
            "low": low,
            "high": high,
            "mid": None,
            "mid_value": None,
            "status": "not_found",
            "decision": f"{target} was not found."
        }
    )
    return False, -1, steps



def is_sorted_non_decreasing(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))



def escape_html(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")



def render_final_message(target, found, index, sorted_ok):
    if sorted_ok and found:
        title = "Binary search worked"
        body = f"The list is sorted, so binary search is valid here. The target {target} was found at index {index}."
        color = "#166534"
        bg = "#f0fdf4"
    elif sorted_ok and not found:
        title = "Binary search worked"
        body = f"The list is sorted, and binary search correctly concluded that {target} is not in the list."
        color = "#1d4ed8"
        bg = "#eff6ff"
    else:
        title = "Broken search case"
        body = "The list is not fully sorted. Binary search still follows its normal rules, but those rules depend on sorted data, so the result may be misleading."
        color = "#b91c1c"
        bg = "#fef2f2"

    return f"""
    <div style='padding:16px;border-radius:16px;background:{bg};border:1px solid #e2e8f0;'>
        <div style='font-size:24px;font-weight:800;color:{color};'>{escape_html(title)}</div>
        <div style='margin-top:8px;font-size:15px;color:#334155;'>{escape_html(body)}</div>
    </div>
    """



def steps_to_table(steps):
    rows = []
    for i, step in enumerate(steps, start=1):
        rows.append(
            {
                "Step": i,
                "Low": step["low"],
                "High": step["high"],
                "Mid": step["mid"],
                "Mid Value": step["mid_value"],
                "Decision": step["decision"]
            }
        )
    return pd.DataFrame(rows)



def render_visualizer(arr, target, steps, sorted_ok, current_step, is_playing):
    if not steps:
        return "<div style='padding:16px;border-radius:16px;background:#fff7ed;color:#9a3412;font-weight:700;'>No steps to display yet.</div>"

    idx = max(0, min(current_step, len(steps) - 1))
    step = steps[idx]
    prev_step = steps[idx - 1] if idx > 0 else None
    progress = ((idx + 1) / len(steps)) * 100
    mode_label = "Valid search" if sorted_ok else "Broken search"
    mode_color = "#166534" if sorted_ok else "#b91c1c"
    subtitle = "Binary search assumptions are satisfied." if sorted_ok else "Binary search may fail because the list is not fully sorted."
    status_text = "Playing" if is_playing else "Paused"

    cells = []
    for i, value in enumerate(arr):
        bg = "#f8fafc"
        border = "#cbd5e1"
        opacity = "0.55"
        outline = ""
        tags = []
        arrow = ""

        in_range = step["low"] is not None and step["high"] is not None and step["low"] <= i <= step["high"]
        if in_range:
            bg = "#ecfeff"
            border = "#06b6d4"
            opacity = "1"

        if i == step["mid"]:
            bg = "#fef3c7"
            border = "#f59e0b"
            outline = "box-shadow:0 0 0 4px rgba(245, 158, 11, 0.18);"
            arrow = "<div style='font-size:24px;line-height:1;color:#b45309;font-weight:900;margin-bottom:6px;'>↓</div>"
            tags.append("<span style='padding:3px 6px;border-radius:999px;font-size:10px;font-weight:800;color:white;background:#b45309;'>MID</span>")

        if i == step["low"]:
            tags.append("<span style='padding:3px 6px;border-radius:999px;font-size:10px;font-weight:800;color:white;background:#0f766e;'>LOW</span>")

        if i == step["high"]:
            tags.append("<span style='padding:3px 6px;border-radius:999px;font-size:10px;font-weight:800;color:white;background:#7c3aed;'>HIGH</span>")

        value_color = "#166534" if value == target else "#0f172a"

        cell = f"""
        <div style='width:92px;min-width:92px;padding:8px 8px 12px 8px;border:2px solid {border};background:{bg};border-radius:16px;text-align:center;opacity:{opacity};box-sizing:border-box;{outline}'>
            {arrow}
            <div style='font-size:21px;line-height:1.1;font-weight:800;color:{value_color};'>{escape_html(value)}</div>
            <div style='margin-top:6px;font-size:11px;color:#64748b;font-weight:700;'>i={i}</div>
            <div style='margin-top:6px;min-height:34px;display:flex;gap:4px;justify-content:center;flex-wrap:wrap;'>{''.join(tags)}</div>
        </div>
        """
        cells.append(cell)

    mid_text = "No midpoint available" if step["mid"] is None else f"mid = {step['mid']} | value = {step['mid_value']}"
    range_text = f"low = {step['low']} | high = {step['high']}"

    if prev_step is None or prev_step.get("mid") is None or step.get("mid") is None:
        movement_text = "Starting point"
    elif step["mid"] > prev_step["mid"]:
        movement_text = f"Midpoint moved right: i={prev_step['mid']} → i={step['mid']}"
    elif step["mid"] < prev_step["mid"]:
        movement_text = f"Midpoint moved left: i={prev_step['mid']} ← i={step['mid']}"
    else:
        movement_text = f"Midpoint stayed at i={step['mid']}"

    return f"""
    <div style='border:1px solid #e2e8f0;border-radius:20px;padding:18px;background:linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);box-shadow:0 8px 24px rgba(15, 23, 42, 0.06);'>
        <div style='display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:center;'>
            <div>
                <div style='font-size:24px;font-weight:800;color:#0f172a;'>Binary Search Visualizer</div>
                <div style='font-size:13px;font-weight:800;color:{mode_color};margin-top:4px;'>{mode_label}</div>
                <div style='margin-top:6px;color:#475569;font-size:14px;'>{subtitle}</div>
            </div>
            <div style='display:flex;align-items:center;gap:8px;font-size:13px;color:#475569;font-weight:700;'>
                <span style='width:10px;height:10px;border-radius:999px;background:{'#22c55e' if is_playing else '#94a3b8'};display:inline-block;'></span>{status_text}
            </div>
        </div>
        <div style='margin-top:16px;height:12px;background:#e2e8f0;border-radius:999px;overflow:hidden;'>
            <div style='height:100%;width:{progress}%;background:linear-gradient(90deg, #38bdf8 0%, #2563eb 100%);'></div>
        </div>
        <div style='margin-top:8px;font-size:13px;color:#475569;font-weight:700;'>Step {idx + 1} of {len(steps)}</div>
        <div style='margin-top:16px;display:flex;gap:10px;flex-wrap:wrap;'>
            <div style='background:white;border:1px solid #e2e8f0;border-radius:14px;padding:10px 12px;font-size:14px;color:#0f172a;'>Target: <strong>{escape_html(target)}</strong></div>
            <div style='background:white;border:1px solid #e2e8f0;border-radius:14px;padding:10px 12px;font-size:14px;color:#0f172a;'>{escape_html(range_text)}</div>
            <div style='background:white;border:1px solid #e2e8f0;border-radius:14px;padding:10px 12px;font-size:14px;color:#0f172a;'>{escape_html(mid_text)}</div>
        </div>
        <div style='margin-top:16px;display:flex;gap:10px;flex-wrap:wrap;'>
            <div style='background:#eff6ff;border:1px solid #bfdbfe;border-radius:14px;padding:10px 12px;font-size:14px;color:#1e3a8a;font-weight:700;'>
                {escape_html(movement_text)}
            </div>
        </div>
        <div style='margin-top:12px;background:white;border:1px solid #e2e8f0;border-left:5px solid #2563eb;border-radius:14px;padding:14px;font-size:15px;color:#0f172a;min-height:52px;'>
            {escape_html(step['decision'])}
        </div>
        <div style='margin-top:18px;padding:8px 2px 10px 2px;'>
            <div style='display:flex;flex-wrap:wrap;gap:12px;align-items:flex-start;'>
                {''.join(cells)}
            </div>
        </div>
        <div style='margin-top:16px;display:flex;gap:14px;flex-wrap:wrap;color:#475569;font-size:13px;font-weight:700;'>
            <div style='display:flex;align-items:center;gap:8px;'><span style='width:14px;height:14px;border-radius:4px;background:#ecfeff;border:1px solid #06b6d4;display:inline-block;'></span>Active search range</div>
            <div style='display:flex;align-items:center;gap:8px;'><span style='width:14px;height:14px;border-radius:4px;background:#fef3c7;border:1px solid #f59e0b;display:inline-block;'></span>Current midpoint</div>
            <div style='display:flex;align-items:center;gap:8px;'><span style='width:14px;height:14px;border-radius:4px;background:#f8fafc;border:1px solid #cbd5e1;display:inline-block;'></span>Outside current range</div>
            <div style='display:flex;align-items:center;gap:8px;'><span style='font-size:16px;color:#b45309;font-weight:900;'>↓</span>Current midpoint arrow</div>
            <div style='display:flex;align-items:center;gap:8px;'><span style='font-size:16px;color:#1e3a8a;font-weight:900;'>← →</span>Midpoint movement direction</div>
        </div>
    </div>
    """



def render_game_board(state):
    arr = state.get("arr", [])
    target = state.get("target")
    revealed = set(state.get("revealed", []))
    clicks_used = state.get("clicks_used", 0)
    binary_steps = state.get("binary_steps", 0)
    feedback = state.get("feedback", "Reveal values and try to find the target.")
    game_over = state.get("game_over", False)

    if not arr or target is None:
        return "<div style='padding:16px;border-radius:16px;background:#fff7ed;color:#9a3412;font-weight:700;'>Start a challenge to play.</div>"

    if game_over:
        if clicks_used < binary_steps:
            status_text = f"You win. You found the target in {clicks_used} reveals. Binary search needed {binary_steps}."
            status_color = "#166534"
        elif clicks_used == binary_steps:
            status_text = f"Tie game. You matched binary search at {binary_steps} reveals."
            status_color = "#1d4ed8"
        else:
            status_text = f"You found the target in {clicks_used} reveals. Binary search only needed {binary_steps}."
            status_color = "#b91c1c"
    else:
        status_text = f"Your reveals: {clicks_used}. Binary search benchmark: {binary_steps}."
        status_color = "#1d4ed8"

    cells = []
    for i, value in enumerate(arr):
        label = str(value) if i in revealed else "?"
        bg = "#ffffff" if i in revealed else "#f8fafc"
        border = "#2563eb" if i in revealed else "#cbd5e1"
        value_color = "#166534" if i in revealed and value == target else "#0f172a"
        target_tag = ""
        if i in revealed and value == target:
            target_tag = "<div style='margin-top:6px;font-size:10px;font-weight:800;color:#166534;'>TARGET</div>"

        cells.append(
            f"""
            <div style='width:92px;min-width:92px;padding:12px 8px;border:2px solid {border};background:{bg};border-radius:16px;text-align:center;box-sizing:border-box;'>
                <div style='font-size:21px;line-height:1.1;font-weight:800;color:{value_color};'>{escape_html(label)}</div>
                <div style='margin-top:6px;font-size:11px;color:#64748b;font-weight:700;'>i={i}</div>
                {target_tag}
            </div>
            """
        )

    return f"""
    <div style='border:1px solid #e2e8f0;border-radius:20px;padding:18px;background:linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);box-shadow:0 8px 24px rgba(15, 23, 42, 0.06);'>
        <div style='display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:center;'>
            <div>
                <div style='font-size:24px;font-weight:800;color:#0f172a;'>Human vs Binary Search</div>
                <div style='font-size:13px;font-weight:800;color:#1d4ed8;margin-top:4px;'>Reveal race challenge</div>
                <div style='margin-top:6px;color:#475569;font-size:14px;'>Reveal values one by one until you find the target. Then compare your total reveals against binary search.</div>
            </div>
            <div style='font-size:14px;font-weight:800;color:{status_color};background:#eff6ff;border:1px solid #bfdbfe;border-radius:12px;padding:10px 12px;'>{escape_html(status_text)}</div>
        </div>
        <div style='margin-top:16px;display:flex;gap:10px;flex-wrap:wrap;'>
            <div style='background:white;border:1px solid #e2e8f0;border-radius:14px;padding:10px 12px;font-size:14px;color:#0f172a;'>Target: <strong>{escape_html(target)}</strong></div>
            <div style='background:white;border:1px solid #e2e8f0;border-radius:14px;padding:10px 12px;font-size:14px;color:#0f172a;'>Binary search steps: <strong>{binary_steps}</strong></div>
            <div style='background:white;border:1px solid #e2e8f0;border-radius:14px;padding:10px 12px;font-size:14px;color:#0f172a;'>Your reveals: <strong>{clicks_used}</strong></div>
        </div>
        <div style='margin-top:12px;background:#f8fafc;border:1px solid #e2e8f0;border-left:5px solid #2563eb;border-radius:14px;padding:14px;font-size:15px;color:#0f172a;min-height:52px;'>
            {escape_html(feedback)}
        </div>
        <div style='margin-top:18px;padding:8px 2px 10px 2px;'>
            <div style='display:flex;flex-wrap:wrap;gap:12px;align-items:flex-start;'>
                {''.join(cells)}
            </div>
        </div>
    </div>
    """



def generate_example_input(mode, size):
    rng = random.Random()
    base = sorted(rng.sample(range(1, size * 10 + 50), size))

    if mode == "Working Example (Sorted)":
        target = rng.choice(base)
        return ", ".join(str(x) for x in base), target

    broken = base[:]
    if len(broken) >= 4:
        swaps = max(1, len(broken) // 6)
        for _ in range(swaps):
            i = rng.randint(0, len(broken) - 2)
            broken[i], broken[i + 1] = broken[i + 1], broken[i]

    if is_sorted_non_decreasing(broken):
        i = len(broken) // 2
        broken[i], broken[i + 1] = broken[i + 1], broken[i]

    target = rng.choice(broken)
    return ", ".join(str(x) for x in broken), target



def generate_example_for_ui(mode, size):
    return generate_example_input(mode, size)



def run_search(numbers_text, target):
    empty_df = steps_to_table([])
    empty_state = {"arr": [], "target": None, "steps": [], "sorted_ok": True, "current_step": 0, "is_playing": False}

    try:
        arr = parse_numbers(numbers_text)
    except ValueError:
        return (
            "<div style='padding:16px;border-radius:14px;background:#fef2f2;color:#991b1b;font-weight:700;'>Please enter only comma-separated integers, like 1, 3, 5, 7.</div>",
            "<div style='padding:16px;border-radius:14px;background:#fff7ed;color:#9a3412;font-weight:700;'>No visualizer available yet.</div>",
            empty_df,
            empty_state,
            gr.update(active=False)
        )

    if len(arr) == 0:
        return (
            "<div style='padding:16px;border-radius:14px;background:#fef2f2;color:#991b1b;font-weight:700;'>Please enter at least one number.</div>",
            "<div style='padding:16px;border-radius:14px;background:#fff7ed;color:#9a3412;font-weight:700;'>No visualizer available yet.</div>",
            empty_df,
            empty_state,
            gr.update(active=False)
        )

    target = int(target)
    sorted_ok = is_sorted_non_decreasing(arr)
    found, index, steps = binary_search_steps(arr, target)
    result_html = render_final_message(target, found, index, sorted_ok)
    state = {"arr": arr, "target": target, "steps": steps, "sorted_ok": sorted_ok, "current_step": 0, "is_playing": True}
    visualizer_html = render_visualizer(arr, target, steps, sorted_ok, 0, True)
    steps_df = steps_to_table(steps)

    return result_html, visualizer_html, steps_df, state, gr.update(active=True)



def timer_tick(state):
    arr = state.get("arr", [])
    target = state.get("target")
    steps = state.get("steps", [])
    sorted_ok = state.get("sorted_ok", True)
    current_step = state.get("current_step", 0)
    is_playing = state.get("is_playing", False)

    if not arr or target is None or not steps:
        return "<div style='padding:16px;border-radius:14px;background:#fff7ed;color:#9a3412;font-weight:700;'>Run a search first.</div>", state, gr.update(active=False)

    if not is_playing:
        html = render_visualizer(arr, target, steps, sorted_ok, current_step, False)
        return html, state, gr.update(active=False)

    if current_step < len(steps) - 1:
        current_step += 1
        state["current_step"] = current_step
        html = render_visualizer(arr, target, steps, sorted_ok, current_step, True)
        return html, state, gr.update(active=True)

    state["is_playing"] = False
    html = render_visualizer(arr, target, steps, sorted_ok, current_step, False)
    return html, state, gr.update(active=False)



def pause_animation(state):
    state["is_playing"] = False
    arr = state.get("arr", [])
    target = state.get("target")
    steps = state.get("steps", [])
    sorted_ok = state.get("sorted_ok", True)
    current_step = state.get("current_step", 0)
    html = render_visualizer(arr, target, steps, sorted_ok, current_step, False) if steps else "<div style='padding:16px;border-radius:14px;background:#fff7ed;color:#9a3412;font-weight:700;'>Run a search first.</div>"
    return html, state, gr.update(active=False)



def resume_animation(state):
    if not state.get("steps", []):
        return "<div style='padding:16px;border-radius:14px;background:#fff7ed;color:#9a3412;font-weight:700;'>Run a search first.</div>", state, gr.update(active=False)
    state["is_playing"] = True
    arr = state.get("arr", [])
    target = state.get("target")
    steps = state.get("steps", [])
    sorted_ok = state.get("sorted_ok", True)
    current_step = state.get("current_step", 0)
    html = render_visualizer(arr, target, steps, sorted_ok, current_step, True)
    return html, state, gr.update(active=True)



def previous_step(state):
    if not state.get("steps", []):
        return "<div style='padding:16px;border-radius:14px;background:#fff7ed;color:#9a3412;font-weight:700;'>Run a search first.</div>", state, gr.update(active=False)
    state["is_playing"] = False
    state["current_step"] = max(0, state.get("current_step", 0) - 1)
    arr = state.get("arr", [])
    target = state.get("target")
    steps = state.get("steps", [])
    sorted_ok = state.get("sorted_ok", True)
    html = render_visualizer(arr, target, steps, sorted_ok, state["current_step"], False)
    return html, state, gr.update(active=False)



def next_step(state):
    if not state.get("steps", []):
        return "<div style='padding:16px;border-radius:14px;background:#fff7ed;color:#9a3412;font-weight:700;'>Run a search first.</div>", state, gr.update(active=False)
    state["is_playing"] = False
    state["current_step"] = min(len(state.get("steps", [])) - 1, state.get("current_step", 0) + 1)
    arr = state.get("arr", [])
    target = state.get("target")
    steps = state.get("steps", [])
    sorted_ok = state.get("sorted_ok", True)
    html = render_visualizer(arr, target, steps, sorted_ok, state["current_step"], False)
    return html, state, gr.update(active=False)



def start_challenge(mode, size):
    numbers_text, target = generate_example_input(mode, size)
    arr = parse_numbers(numbers_text)
    sorted_arr = sorted(arr)
    target = random.choice(sorted_arr)
    _, _, steps = binary_search_steps(sorted_arr, target)
    binary_steps = len(steps)
    state = {
        "arr": sorted_arr,
        "target": target,
        "revealed": [],
        "clicks_used": 0,
        "binary_steps": binary_steps,
        "feedback": "Pick an index and reveal it.",
        "game_over": False
    }
    board = render_game_board(state)
    status_text = f"Binary search benchmark: {binary_steps} steps"
    choices = [str(i) for i in range(len(sorted_arr))]
    first_choice = choices[0] if choices else None
    return board, status_text, state, gr.update(choices=choices, value=first_choice), gr.update(interactive=True)



def reveal_human_choice(index_text, state):
    arr = state.get("arr", [])
    target = state.get("target")
    revealed = set(state.get("revealed", []))
    binary_steps = state.get("binary_steps", 0)

    def finish_response():
        choices = [str(i) for i in range(len(arr)) if i not in revealed]
        next_value = choices[0] if choices else None
        return render_game_board(state), f"Binary search benchmark: {binary_steps} steps", state, gr.update(choices=choices, value=next_value), gr.update(interactive=not state.get("game_over", False))

    if not arr or target is None:
        return finish_response()

    if state.get("game_over", False):
        return finish_response()

    if index_text is None or str(index_text).strip() == "":
        state["feedback"] = "Choose an index to reveal."
        return finish_response()

    try:
        idx = int(index_text)
    except Exception:
        state["feedback"] = "Invalid reveal index."
        return finish_response()

    if idx < 0 or idx >= len(arr):
        state["feedback"] = "That index is out of range."
        return finish_response()

    if idx in revealed:
        state["feedback"] = f"Index {idx} is already revealed. Pick a different one."
        return finish_response()

    revealed.add(idx)
    state["revealed"] = sorted(revealed)
    state["clicks_used"] = state.get("clicks_used", 0) + 1

    value = arr[idx]
    if value == target:
        state["game_over"] = True
        if state["clicks_used"] < binary_steps:
            state["feedback"] = f"You revealed index {idx} and found {target}. You beat binary search."
        elif state["clicks_used"] == binary_steps:
            state["feedback"] = f"You revealed index {idx} and found {target}. You tied binary search."
        else:
            state["feedback"] = f"You revealed index {idx} and found {target}, but binary search was faster."
    else:
        if value < target:
            hint = "That value is lower than the target."
        else:
            hint = "That value is higher than the target."
        state["feedback"] = f"You revealed index {idx} = {value}. {hint}"

    return finish_response()


with gr.Blocks(title="Broken Search: When Binary Search Works and Fails") as demo:
    state = gr.State({"arr": [], "target": None, "steps": [], "sorted_ok": True, "current_step": 0, "is_playing": False})
    game_state = gr.State({"arr": [], "target": None, "revealed": [], "clicks_used": 0, "binary_steps": 0, "feedback": "Start a challenge to play.", "game_over": False})

    gr.Markdown(
        """
        # Broken Search: Binary Search Visualizer
        This app shows **when binary search works** and **why it can fail**.
        Use the visualizer tab to study the algorithm, then switch to the challenge tab to test whether you can predict the next move before revealing the midpoint.
        """
    )

    with gr.Tabs():
        with gr.Tab("Visualizer"):
            with gr.Row():
                with gr.Column(scale=5):
                    numbers_input = gr.Textbox(
                        label="Enter a list of integers",
                        placeholder="Example: 1, 3, 5, 7, 9, 11",
                        lines=3
                    )
                    target_input = gr.Number(label="Target number", precision=0)
                    run_button = gr.Button("Run Binary Search", variant="primary")
                with gr.Column(scale=4):
                    demo_mode = gr.Dropdown(
                        choices=["Working Example (Sorted)", "Broken Example (Unsorted)"],
                        value="Working Example (Sorted)",
                        label="Example mode"
                    )
                    demo_size = gr.Slider(minimum=10, maximum=25, value=12, step=1, label="Example list size")
                    generate_button = gr.Button("Generate Example Input")

            result_output = gr.HTML(label="Result")

            with gr.Row():
                pause_button = gr.Button("⏸ Pause")
                resume_button = gr.Button("▶ Resume")
                prev_button = gr.Button("⏮ Previous")
                next_button = gr.Button("⏭ Next")

            visualizer_output = gr.HTML(label="Visualizer")
            steps_output = gr.Dataframe(label="Step-by-Step Search Trace", interactive=False)
            timer = gr.Timer(value=3.0, active=False)

            run_button.click(
                fn=run_search,
                inputs=[numbers_input, target_input],
                outputs=[result_output, visualizer_output, steps_output, state, timer]
            )

            timer.tick(
                fn=timer_tick,
                inputs=[state],
                outputs=[visualizer_output, state, timer]
            )

            pause_button.click(
                fn=pause_animation,
                inputs=[state],
                outputs=[visualizer_output, state, timer]
            )

            resume_button.click(
                fn=resume_animation,
                inputs=[state],
                outputs=[visualizer_output, state, timer]
            )

            prev_button.click(
                fn=previous_step,
                inputs=[state],
                outputs=[visualizer_output, state, timer]
            )

            next_button.click(
                fn=next_step,
                inputs=[state],
                outputs=[visualizer_output, state, timer]
            )

            generate_button.click(
                fn=generate_example_for_ui,
                inputs=[demo_mode, demo_size],
                outputs=[numbers_input, target_input]
            )

        with gr.Tab("Challenge Mode"):
            gr.Markdown(
                """
                In this mode, the whole array starts hidden. The computer already knows how many steps binary search needs. You can keep revealing values until you find the target, then compare your total reveals against the binary search benchmark.
                """
            )

            with gr.Row():
                game_mode = gr.Dropdown(
                    choices=["Working Example (Sorted)", "Broken Example (Unsorted)"],
                    value="Working Example (Sorted)",
                    label="Challenge mode"
                )
                game_size = gr.Slider(minimum=10, maximum=25, value=12, step=1, label="Challenge list size")
                start_game_button = gr.Button("Start Challenge", variant="primary")

            game_board_output = gr.HTML(label="Challenge Board")
            score_output = gr.Markdown("Binary search benchmark: 0 steps")
            reveal_index_dropdown = gr.Dropdown(choices=[], label="Choose an index to reveal")
            reveal_button = gr.Button("Reveal Selected Index", interactive=False)

            gr.Markdown("Pick an unrevealed index, reveal it, and compare your total reveals with binary search when you eventually find the target.")

            start_game_button.click(
                fn=start_challenge,
                inputs=[game_mode, game_size],
                outputs=[game_board_output, score_output, game_state, reveal_index_dropdown, reveal_button]
            )

            reveal_button.click(
                fn=reveal_human_choice,
                inputs=[reveal_index_dropdown, game_state],
                outputs=[game_board_output, score_output, game_state, reveal_index_dropdown, reveal_button]
            )


demo.launch()
