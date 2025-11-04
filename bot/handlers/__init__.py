from bot.handlers.user_data_handler import UserDataHandler
from bot.handlers.group_guard_handler import GroupGuardHandler
from bot.handlers.start_handler import StartHandler
from bot.handlers.change_handler import ChangeHandler
from bot.handlers.group_input_handler import GroupInputHandler
from bot.handlers.today_handler import TodayHandler
from bot.handlers.tomorrow_handler import TomorrowHandler
from bot.handlers.week_handler import WeekHandler
from bot.handlers.cancel_handler import CancelHandler
from bot.handlers.help_handler import HelpHandler


def get_handlers():
    return [
        UserDataHandler(),
        GroupGuardHandler(),
        StartHandler(),
        ChangeHandler(),
        CancelHandler(),
        HelpHandler(),
        TodayHandler(),
        TomorrowHandler(),
        WeekHandler(),
        GroupInputHandler(),
    ]
