import pytest
from bot.handlers.start_handler import StartHandler
from tests.mocks import create_fake_update
from bot.handler_result import HandlerStatus


@pytest.fixture
def handler():
    """Фикстура для создания хендлера"""
    return StartHandler()


@pytest.fixture
def mocks(mocker):
    """Фикстура для создания моков"""
    return {"messenger": mocker.Mock(), "database": mocker.Mock()}


@pytest.mark.parametrize(
    "text,expected",
    [
        ("/start", True),
        ("/start 123", True),
        ("  /start  123 23", True),
        ("/help", False),
        ("/change", False),
    ],
)
def test_can_handle(handler, text, expected):
    """Тест can_handle для разных команд"""
    update = create_fake_update(text, 123456789)
    assert handler.can_handle(update, None, {}) == expected


def test_can_handle_without_message(handler):
    """Тест can_handle без поля message"""
    assert not handler.can_handle({"update_id": 0}, None, {})


def test_handle_without_group(handler, mocks):
    """Тест handle без group_id - запрашивает группу"""
    update = create_fake_update("/start", 123456789)
    data = {}

    result = handler.handle(update, None, data, mocks["messenger"], mocks["database"])

    assert result == HandlerStatus.STOP
    assert data["state"] == "WAITING_FOR_GROUP"
    mocks["messenger"].send_message.assert_called_once_with(
        123456789, "Вас приветствует бот расписания ННГУ, введите номер группы"
    )


def test_handle_with_group(handler, mocks):
    update = create_fake_update("/start", 123456789)
    data = {"group_id": "12345", "group_number": "test"}

    result = handler.handle(update, None, data, mocks["messenger"], mocks["database"])

    assert result == HandlerStatus.STOP
    assert data["state"] is None
    mocks["messenger"].send_message.assert_called_once()
    call_args = mocks["messenger"].send_message.call_args
    assert call_args[0][1] == "Добро пожаловать! Ваша группа: test"
    assert "reply_markup" in call_args[1]
