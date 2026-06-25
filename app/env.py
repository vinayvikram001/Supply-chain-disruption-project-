import os
import sys
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"
CREWAI_APPDATA_PATH = PROJECT_ROOT / ".crewai"
CREWAI_DB_PATH = CREWAI_APPDATA_PATH / "CrewAI" / PROJECT_ROOT.name

CREWAI_APPDATA_PATH.mkdir(exist_ok=True)
CREWAI_DB_PATH.mkdir(parents=True, exist_ok=True)
os.environ["LOCALAPPDATA"] = str(CREWAI_APPDATA_PATH)

load_dotenv(dotenv_path=ENV_PATH)
os.environ.setdefault("LITELLM_DROP_PARAMS", "true")

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

try:
    import crewai_core.paths

    crewai_core.paths.db_storage_path = lambda: str(CREWAI_DB_PATH)
except ImportError:
    pass

try:
    import litellm

    litellm.drop_params = True
    _litellm_completion = litellm.completion

    def _remove_cache_breakpoints(value):
        if isinstance(value, dict):
            value.pop("cache_breakpoint", None)
            for item in value.values():
                _remove_cache_breakpoints(item)
        elif isinstance(value, list):
            for item in value:
                _remove_cache_breakpoints(item)
        return value

    def _completion_without_cache_breakpoints(*args, **kwargs):
        _remove_cache_breakpoints(args)
        _remove_cache_breakpoints(kwargs)
        return _litellm_completion(*args, **kwargs)

    litellm.completion = _completion_without_cache_breakpoints
    if hasattr(litellm, "acompletion"):
        _litellm_acompletion = litellm.acompletion

        async def _acompletion_without_cache_breakpoints(*args, **kwargs):
            _remove_cache_breakpoints(args)
            _remove_cache_breakpoints(kwargs)
            return await _litellm_acompletion(*args, **kwargs)

        litellm.acompletion = _acompletion_without_cache_breakpoints
except ImportError:
    pass


def require_env(name: str) -> str:
    value = os.getenv(name)
    placeholder_values = {
        f"your_actual_{name.lower()}",
        "gsk_your_real_key_here",
    }
    if not value or value in placeholder_values:
        raise RuntimeError(
            f"{name} is missing. Add it to {ENV_PATH} like: {name}=your_real_key"
        )
    return value
