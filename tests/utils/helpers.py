"""
Хелперы для тестов: преобразование строк в UUID.
"""

import uuid


def to_uuid(value: str) -> str:
    """
    Конвертация строки в UUID5.
    """
    value = value.strip()
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, value)).lower()
