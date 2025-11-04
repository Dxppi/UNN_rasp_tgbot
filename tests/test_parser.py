import json
from parser.parseData import fetch_group_id, make_schedule
import pytest


def test_fetch_group_id(mocker):
    group_name = "test_name"
    fake_response_data = [
        {"number": "other_group", "groupOid": "99999"},
        {"number": "test_name", "groupOid": "11111"},
    ]

    mock_urlopen = mocker.patch("urllib.request.urlopen", autospec=True)

    mock_response = mocker.Mock()
    mock_response.read.return_value = json.dumps(fake_response_data).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_response

    result = fetch_group_id(group_name)

    assert result == "11111"


def test_fetch_group_not_found():
    group_name = "nonexistent_group"

    with pytest.raises(Exception, match="Группа не найдена"):
        fetch_group_id(group_name)


def test_make_schedule():
    fake_response_data = [
        {
            "date": "2025-11-04",
            "discipline": "Math",
            "auditorium": "101",
            "building": "A",
            "beginLesson": "09:00",
            "endLesson": "10:30",
            "lecturer": "Dr. Smith",
        },
        {
            "date": "2025-11-04",
            "discipline": "Physics",
            "auditorium": "202",
            "building": "B",
            "beginLesson": "11:00",
            "endLesson": "12:30",
            "lecturer": "Dr. Johnson",
        },
        {
            "date": "2025-11-05",
            "discipline": "Chemistry",
            "auditorium": "303",
            "building": "C",
            "beginLesson": "13:00",
            "endLesson": "14:30",
            "lecturer": "Dr. Brown",
        },
    ]

    expected_result = {
        "04-11-2025": [
            {
                "discipline": "Math",
                "auditorium": "101",
                "building": "A",
                "beginLesson": "09:00",
                "endLesson": "10:30",
                "lecturer": "Dr. Smith",
            },
            {
                "discipline": "Physics",
                "auditorium": "202",
                "building": "B",
                "beginLesson": "11:00",
                "endLesson": "12:30",
                "lecturer": "Dr. Johnson",
            },
        ],
        "05-11-2025": [
            {
                "discipline": "Chemistry",
                "auditorium": "303",
                "building": "C",
                "beginLesson": "13:00",
                "endLesson": "14:30",
                "lecturer": "Dr. Brown",
            },
        ],
    }

    result = make_schedule(fake_response_data)

    assert result == expected_result
