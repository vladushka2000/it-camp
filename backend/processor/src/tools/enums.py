import enum
import uuid

from interfaces import base_enum


class StructuralUnit(base_enum.AbstractIdNameEnum):
    """
    Enum для структурных элементов
    """

    ABSENCE = (uuid.UUID("7d2a4cf4-0c2e-446b-bfc3-c11aed172725"), "Отсутствие")
    JOINT = (uuid.UUID("3e058c22-8452-4a0a-b0fa-368f5e205912"), "Сварной шов")
    BEND = (uuid.UUID("94950972-c06f-4bc0-92b7-76c23b8a5295"), "Изгиб")
    BRANCHING = (uuid.UUID("a16b87aa-b6ed-4910-8412-8adb37ad943d"), "Разветвление")
    PATCH = (uuid.UUID("dc3690d8-b52d-4cd3-829a-2e2223813e40"), "Заплатка")


class Defect(base_enum.AbstractIdNameEnum):
    """
    Enum для дефектов
    """

    ABSENCE = (uuid.UUID("985c9151-5446-4130-ae65-755baef7ac63"), "Отсутствие")
    PRESENCE = (uuid.UUID("e817ad05-c8b6-4f26-be95-ce9bf20b7822"), "Присутствие")


class HistoryAction(base_enum.AbstractIdNameEnum):
    """
    Enum для действий пользователя
    """

    UPLOAD = (uuid.UUID("7fefea33-46f6-4b63-986b-4184742efd6a"), "Загрузка магнитограммы")
    EDIT = (uuid.UUID("5b329d90-98aa-49ed-b01a-f7d85c0b17c6"), "Редактирование магнитограммы")


class RepositoryName(enum.Enum):
    """
    Enum названий репозиториев
    """

    MAGNETOGRAM_REPOSITORY = "magnetogram_repository"
    HISTORY_REPOSITORY = "history_repository"
