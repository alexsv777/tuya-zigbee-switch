
from pathlib import Path
import re

path = Path("device_db.yaml")
target = "MODULE_HOBEIAN_TS0001_2"

text = path.read_text(encoding="utf-8")

pattern = re.compile(
    r"(?m)^([A-Z][A-Z0-9_]*):\n(.*?)(?=^[A-Z][A-Z0-9_]*:\n|\Z)",
    re.S
)

found = False

def update(match):
    global found
    key = match.group(1)
    block = match.group(2)

    if key == target:
        found = True
        value = "yes"
    else:
        value = "no"

    block, count = re.subn(
        r"(?m)^  build:\s*(?:yes|no)\s*$",
        f"  build: {value}",
        block,
        count=1
    )

    if count != 1:
        raise RuntimeError(f"Не найдена строка build в записи {key}")

    return f"{key}:\n{block}"

result = pattern.sub(update, text)

if not found:
    raise RuntimeError(f"Устройство {target} не найдено")

path.write_text(result, encoding="utf-8")
print("Готово. Остальные устройства отключены.")
