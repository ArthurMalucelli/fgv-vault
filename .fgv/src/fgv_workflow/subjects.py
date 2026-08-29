import json
from dataclasses import dataclass
from pathlib import Path
import unicodedata


CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "subjects.json"


def normalize(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.strip().casefold())
    return "".join(
        character
        for character in decomposed
        if not unicodedata.combining(character)
    )


@dataclass(frozen=True)
class Subject:
    id: str
    display_name: str
    folder: str
    path: str
    task_tag: str
    aliases: tuple[str, ...]


class SubjectRegistry:
    def __init__(self, subjects: tuple[Subject, ...], semester: str) -> None:
        self.subjects = subjects
        self.semester = semester
        aliases: dict[str, Subject] = {}
        for subject in subjects:
            for alias in (
                subject.id,
                subject.display_name,
                subject.folder,
                *subject.aliases,
            ):
                key = normalize(alias)
                if key in aliases and aliases[key] != subject:
                    raise ValueError(f"duplicate subject alias: {alias}")
                aliases[key] = subject
        self._aliases = aliases

    @classmethod
    def load_default(cls) -> "SubjectRegistry":
        payload = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        return cls(
            tuple(
                Subject(
                    id=item["id"],
                    display_name=item["display_name"],
                    folder=item["folder"],
                    path=item["path"],
                    task_tag=item["task_tag"],
                    aliases=tuple(item["aliases"]),
                )
                for item in payload["subjects"]
            ),
            semester=payload["semester"],
        )

    def resolve(self, value: str) -> Subject:
        key = normalize(value)
        if key in self._aliases:
            return self._aliases[key]
        prefix_matches = {
            subject
            for alias, subject in self._aliases.items()
            if len(key) >= 4 and alias.startswith(key)
        }
        if len(prefix_matches) == 1:
            return next(iter(prefix_matches))
        raise KeyError(f"unknown or ambiguous subject: {value}")
