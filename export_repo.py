"""Скрипт для экспорта структуры и содержимого репозитория в один файл Markdown.

Собирает все файлы исходного кода, конфигурации и документации, исключая
системные директории (виртуальные окружения, базы данных, кэш), и объединяет
их в структурированный .md файл для удобного анализа или резервного копирования.
"""

import os
from pathlib import Path

# Список папок, которые нужно полностью игнорировать при экспорте
IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "postgres_data",
    "redis_data",
    ".idea",
    "logs",
    "temp",
    "pg_data",
    "qdrant_data",
    "redis_data",
}

# Список расширений файлов, которые мы берем для экспорта
ALLOWED_EXTENSIONS = {
    ".py",
    ".toml",
    ".ini",
    ".example",
    ".yml",
    ".yaml",
    ".md",
    ".mako",
    ".json",
    ".txt",
    ".gitignore",
    ".env",
    ".env.example"
}

# Файлы, которые полностью игнорируем
IGNORE_FILES = {
    ".env",
    ".env.local",
    ".env.production",
    "repository_export.md",
    "export_repo.py",
    "poetry.lock",
    "package-lock.json",
    "yarn.lock",
    "Thumbs.db",
}

ALLOWED_FILENAMES = {
    "Dockerfile",
    ".gitignore",
    ".env.example",
    ".env"
}


def build_tree(dir_path: Path, prefix: str = "") -> list[str]:
    """Рекурсивно строит текстовое дерево файлов и папок.

    Args:
        dir_path: Путь к текущей сканируемой папке.
        prefix: Отступ для визуализации вложенности.

    Returns:
        Список строк, представляющих дерево проекта.
    """
    tree = []
    # Фильтруем и сортируем содержимое папки
    items = sorted(
        [
            p
            for p in dir_path.iterdir()
            if p.name not in IGNORE_DIRS
               and (
                       not p.name.startswith(".")
                       or p.name in ALLOWED_FILENAMES
               )
        ],
        key=lambda x: (not x.is_dir(), x.name.lower()),
    )

    count = len(items)
    for i, item in enumerate(items):
        is_last = i == count - 1
        connector = "└── " if is_last else "├── "

        if item.is_dir():
            tree.append(f"{prefix}{connector}{item.name}/")
            new_prefix = prefix + ("    " if is_last else "│   ")
            tree.extend(build_tree(item, new_prefix))
        else:
            if item.suffix in ALLOWED_EXTENSIONS or item.name == ".gitignore":
                tree.append(f"{prefix}{connector}{item.name}")

    return tree


def get_syntax_highlight(extension: str) -> str:
    """Определяет язык для подсветки синтаксиса в Markdown.

    Args:
        extension: Расширение файла.

    Returns:
        Строковое обозначение языка для блока кода Markdown.
    """
    mapping = {
        ".py": "python",
        ".toml": "toml",
        ".ini": "ini",
        ".yml": "yaml",
        ".yaml": "yaml",
        ".md": "markdown",
    }
    return mapping.get(extension, "text")


def export_repository():
    """Собирает структуру и файлы проекта в единый Markdown файл."""
    root_dir = Path(__file__).parent.resolve()
    output_file = root_dir / "repository_export.md"

    # Не включаем сам файл экспорта и этот скрипт в результат
    ignore_files = {"repository_export.md", "export_repo.py", "list.md"}

    print("🔍 Сканирую репозиторий...")

    with open(output_file, "w", encoding="utf-8") as out:
        # Пишем заголовок
        out.write("# Экспорт Репозитория: fani-agent\n\n")

        # 1. Записываем дерево структуры проекта
        out.write("## 📂 Структура проекта\n")
        out.write("```text\n")
        out.write(f"{root_dir.name}/\n")
        tree_lines = build_tree(root_dir)
        out.write("\n".join(tree_lines))
        out.write("\n```\n\n")
        out.write("---\n\n")

        # 2. Обходим файлы и записываем их содержимое
        out.write("## 📝 Содержимое файлов\n\n")

        for root, dirs, files in os.walk(root_dir):
            # Отсекаем игнорируемые папки
            dirs[:] = [
                d
                for d in dirs
                if d not in IGNORE_DIRS and not d.startswith(".")
            ]

            for file in sorted(files):
                file_path = Path(root) / file
                rel_path = file_path.relative_to(root_dir)

                # Пропускаем сам скрипт, выходной файл и скрытые файлы
                if (
                        file in ignore_files
                        or file.startswith(".")
                        or (
                        file_path.suffix not in ALLOWED_EXTENSIONS
                        and file != "Dockerfile"
                )
                ):
                    continue

                print(f"📄 Добавляю: {rel_path}")

                out.write(f"### Файл: `{rel_path}`\n\n")

                # Определяем подсветку синтаксиса
                lang = get_syntax_highlight(file_path.suffix)
                out.write(f"```{lang}\n")

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Количество символов в файле
                    char_count = len(content)

                    print(f"   └── {char_count:,} символов")

                    out.write(content)

                except Exception as e:
                    out.write(f"[Ошибка чтения файла: {e}]")
                    print(f"   ⚠️ Ошибка чтения: {e}")

                out.write("\n```\n\n")
                out.write("---\n\n")

    print(f"✅ Готово! Весь проект сохранен в файл: {output_file.name}")


if __name__ == "__main__":
    export_repository()
