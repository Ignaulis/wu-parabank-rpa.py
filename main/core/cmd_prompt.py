from dataclasses import replace


def _ask_choice(title: str, options: list[str], default: str) -> str:
    default_value = default.strip().lower()
    normalized_options = [option.strip().lower() for option in options]
    options_text = "/".join(normalized_options)
    default_index = normalized_options.index(default_value) + 1
    while True:
        print(f"\n{title}:")
        for index, option in enumerate(normalized_options, start=1):
            print(f"  {index}. {option}")
        value = input(f"Choose number or text [default: {default_index} - {default_value}]: ").strip().lower()
        if not value:
            return default_value
        if value.isdigit():
            selected_index = int(value)
            if 1 <= selected_index <= len(normalized_options):
                return normalized_options[selected_index - 1]
        if value in normalized_options:
            return value
        print(f"Invalid choice. Use number or one of: {options_text}")


def _ask_bool(title: str, default: bool) -> bool:
    return _ask_choice(title, ["yes", "no"], "yes" if default else "no") == "yes"


def prompt_runtime_settings(base_settings):
    mode = _ask_choice("Choose mode", ["default", "custom"], "default")
    if mode == "default":
        return base_settings, mode

    kill_on_start = _ask_bool("Kill browser on start", base_settings.kill_on_start)
    browser = _ask_choice("Browser", ["chrome", "edge", "firefox", "safari"], base_settings.browser)
    browser_visible = _ask_bool("Browser visible", base_settings.browser_visible)
    desktop_report = _ask_bool("Save report to Desktop", base_settings.desktop_report)
    report_type = _ask_choice("Report type", ["xlsx", "csv"], base_settings.report_type)

    runtime_settings = replace(
        base_settings,
        kill_on_start=kill_on_start,
        browser=browser,
        browser_visible=browser_visible,
        desktop_report=desktop_report,
        report_type=report_type,
    )
    return runtime_settings, mode
