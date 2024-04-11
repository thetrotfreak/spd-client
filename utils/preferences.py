from copy import deepcopy
from json import JSONDecodeError, dump, load
from pathlib import Path
from typing import Literal, NamedTuple, TypedDict

from flet_core import Page, Theme, ThemeMode, colors
from jsonschema import ValidationError, validate


class PreferenceSchema(TypedDict):
    theme: str
    accent: str


class Configuration(NamedTuple):
    path: Path
    schema: PreferenceSchema
    default: PreferenceSchema


class Preference:
    __config__ = Configuration(
        path=Path(__file__).parent.parent.joinpath(".config", "config.json"),
        schema={
            "type": "object",
            "properties": {
                "theme": {"type": "string", "minLength": 4, "maxLength": 6},
                "accent": {"type": "string", "minLength": 3},
            },
        },
        default=PreferenceSchema(
            {"theme": ThemeMode.SYSTEM.value, "accent": colors.BLUE}
        ),
    )

    __PROPERTY__ = Literal["theme", "accent"]

    __COLORS__ = sorted(
        [
            "RED",
            "PINK",
            "PURPLE",
            "INDIGO",
            "BLUE",
            "CYAN",
            "TEAL",
            "GREEN",
            "LIME",
            "YELLOW",
            "AMBER",
            "ORANGE",
            "BROWN",
        ]
    )

    config = deepcopy(__config__.default)
    page: Page = None

    def __init__(self, page: Page):
        Preference.page = page

    @staticmethod
    def __valid__(config: dict):
        """
        Validate config.json on disk; ill-formatted JSON will result in the
        config.json being overwritten with the default configuration.
        """
        try:
            validate(instance=config, schema=Preference.__config__.schema)
        except ValidationError:
            return False
        else:
            return True

    @staticmethod
    def load():
        """
        Load config.json from disk if found; otherwise load the default
        configuration and save it to disk.
        """
        if not Preference.__config__.path.exists():
            Preference.__config__.path.parent.mkdir(exist_ok=True)
            Preference.__config__.path.touch()
            Preference.__save__()
        else:
            try:
                with open(Preference.__config__.path, "r") as f:
                    Preference.config = load(f)
            except OSError:
                # TODO AlertDialog
                pass
            except JSONDecodeError:
                # thrown for an empty JSON on disk
                Preference.__save__()
            else:
                if Preference.__valid__(Preference.config):
                    Preference.__load__(Preference.config)
                else:
                    Preference.__save__()

    @staticmethod
    def __load__(config):
        """
        Configures the Page to reflect the config
        """
        Preference.config.update(config)
        Preference.page.theme_mode = config.get("theme")
        Preference.page.theme = Theme(color_scheme_seed=config.get("accent"))
        Preference.page.dark_theme = Theme(color_scheme_seed=config.get("accent"))
        Preference.page.update()

    @staticmethod
    def update(k: __PROPERTY__, v: str):
        """
        Call this to persist changes by writing it to config.json
        Also updates the page
        """
        # TODO
        # should {k:v} be validated?
        Preference.config.update({k: v})
        Preference.__save__()
        Preference.load()

    @staticmethod
    def __save__():
        """
        Save the current configuration on disk
        """
        try:
            with open(Preference.__config__.path, "w") as f:
                dump(obj=Preference.config, fp=f)
        except OSError:
            # TODO AlertDialog
            pass
