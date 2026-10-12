from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from content import LESSONS, TASKS, LEVEL_NAMES


def main_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📚 Теория", callback_data="menu:theory")
    kb.button(text="🎯 Практика", callback_data="menu:practice")
    kb.button(text="👤 Досье", callback_data="menu:profile")
    kb.adjust(1)
    return kb.as_markup()


def back_to_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🏠 В главное меню", callback_data="menu:main")
    return kb.as_markup()


def theory_levels_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🟢 Начальный", callback_data="theory:list:beginner")
    kb.button(text="🟡 Средний", callback_data="theory:list:intermediate")
    kb.button(text="🔴 Профессиональный", callback_data="theory:list:pro")
    kb.button(text="🏠 В главное меню", callback_data="menu:main")
    kb.adjust(1)
    return kb.as_markup()


def lessons_list_kb(level: str, completed: set) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for lesson in LESSONS:
        if lesson["level"] != level:
            continue
        mark = "✅" if lesson["id"] in completed else "📖"
        kb.button(
            text=f"{mark} {lesson['id']}. {lesson['title']}",
            callback_data=f"theory:open:{lesson['id']}"
        )
    kb.button(text="⬅️ К уровням", callback_data="menu:theory")
    kb.button(text="🏠 В меню", callback_data="menu:main")
    kb.adjust(1)
    return kb.as_markup()


def lesson_view_kb(lesson_id: str, is_completed: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if not is_completed:
        kb.button(text="✅ Отметить как пройденный", callback_data=f"theory:done:{lesson_id}")
    kb.button(text="⬅️ К урокам", callback_data="theory:back")
    kb.button(text="🏠 Меню", callback_data="menu:main")
    kb.adjust(1)
    return kb.as_markup()


def practice_levels_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🟢 Начальный", callback_data="practice:list:beginner")
    kb.button(text="🟡 Средний", callback_data="practice:list:intermediate")
    kb.button(text="🔴 Профессиональный", callback_data="practice:list:pro")
    kb.button(text="🏠 В главное меню", callback_data="menu:main")
    kb.adjust(1)
    return kb.as_markup()


def tasks_list_kb(level: str, completed: dict) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for i, task in enumerate(TASKS[level]):
        if task["id"] in completed:
            mark = "✅" if completed[task["id"]] else "❌"
        else:
            mark = "🎯"
        kb.button(
            text=f"{mark} {i+1}. {task['title']}",
            callback_data=f"practice:open:{level}:{i}"
        )
    kb.button(text="⬅️ К уровням", callback_data="menu:practice")
    kb.button(text="🏠 В меню", callback_data="menu:main")
    kb.adjust(1)
    return kb.as_markup()


def task_options_kb(level: str, idx: int):
    builder = InlineKeyboardBuilder()
    for i, letter in enumerate(["A", "B", "C", "D"]):
        builder.button(
            text=letter,
            callback_data=f"practice:answer:{level}:{idx}:{i}"
        )
    builder.adjust(4)
    builder.row(InlineKeyboardButton(text="« К списку заданий", callback_data=f"practice:list:{level}"))
    return builder.as_markup()


def after_answer_kb(level: str, idx: int, has_next: bool, is_correct: bool = True):
    builder = InlineKeyboardBuilder()

    if has_next:
        builder.button(
            text="Следующая задача →",
            callback_data=f"practice:open:{level}:{idx + 1}"
        )

    # Кнопка только при неправильном ответе
    if not is_correct:
        builder.button(
            text="🔄 Решить заново",
            callback_data=f"practice:retry:{level}:{idx}"
        )

    builder.button(text="« К списку заданий", callback_data=f"practice:list:{level}")
    builder.button(text="« В меню", callback_data="menu:main")

    builder.adjust(1)
    return builder.as_markup()
