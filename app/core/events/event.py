from typing import Optional, Callable

from app.core.settings.setting import AppSettings


def startup_app_event(setting: AppSettings) -> Optional[Callable]:
    print(f"================================\n"
          f"Server Starting...\n"
          f"env : {setting.app_env}\n"
          f"version : {setting.version}\n"
          f"================================")
    return None


def shutdown_app_event() -> Optional[Callable]:
    print("================================\n"
          "Server Shutdown...\n"
          "================================")
    return None