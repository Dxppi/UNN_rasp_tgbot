def create_fake_update(text: str, user_id: int):
    """Создает стандартный update для тестов"""
    return {
        "update_id": 0,
        "message": {
            "message_id": 1,
            "from": {
                "id": user_id,
                "is_bot": False,
                "first_name": "Test",
                "username": "test_user",
                "language_code": "ru",
            },
            "chat": {
                "id": user_id,
                "first_name": "Test",
                "username": "test_user",
                "type": "private",
            },
            "date": 1730754000,
            "text": text,
        },
    }
