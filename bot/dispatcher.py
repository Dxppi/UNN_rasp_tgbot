from enum import Enum
from bot.config import WAITING_FOR_GROUP, CONVERSATION_END


class State(Enum):
    IDLE = 0
    WAITING_FOR_GROUP = 1


class Update:
    def __init__(self, update_data):
        self.update_data = update_data
        self.message = update_data.get("message", {})

    @property
    def update_id(self):
        return self.update_data.get("update_id", 0)

    @property
    def text(self):
        return self.message.get("text") if self.message else None

    @property
    def chat_id(self):
        return self.message.get("chat", {}).get("id") if self.message else None

    @property
    def user_id(self):
        return self.message.get("from", {}).get("id") if self.message else None

    @property
    def first_name(self):
        return self.message.get("from", {}).get("first_name") if self.message else None

    def is_command(self):
        return self.text and self.text.startswith("/")


class Context:
    def __init__(self, telegram_api, user_states, user_data):
        self.telegram_api = telegram_api
        self.user_states = user_states
        self.user_data = user_data

    def get_user_state(self, user_id):
        return self.user_states.get(user_id, State.IDLE)

    def set_user_state(self, user_id, state):
        self.user_states[user_id] = state

    def clear_user_state(self, user_id):
        if user_id in self.user_states:
            del self.user_states[user_id]

    def get_user_data(self, user_id):
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        return self.user_data[user_id]


class Dispatcher:
    def __init__(self, telegram_api):
        self.telegram_api = telegram_api
        self.user_states = {}
        self.user_data = {}
        self.command_handlers = {}
        self.message_handlers = []
        self.state_handlers = {}

    def register_command(self, command, handler):
        self.command_handlers[command] = handler

    def register_message_handler(self, handler):
        self.message_handlers.append(handler)

    def register_state_handler(self, state, handler):
        if state not in self.state_handlers:
            self.state_handlers[state] = []
        self.state_handlers[state].append(handler)

    def _create_context(self, user_id):
        return Context(self.telegram_api, self.user_states, self.user_data)

    def _handle_result(self, result, context, user_id):
        if isinstance(result, State):
            context.set_user_state(user_id, result)
        elif result == WAITING_FOR_GROUP:
            context.set_user_state(user_id, State.WAITING_FOR_GROUP)
        elif result == CONVERSATION_END:
            context.clear_user_state(user_id)

    def process_update(self, update):
        if not update.chat_id or not update.user_id:
            return

        user_id = update.user_id
        context = self._create_context(user_id)
        current_state = context.get_user_state(user_id)

        if update.is_command():
            command = update.text.split()[0].lower().lstrip("/")
            if command in self.command_handlers:
                result = self.command_handlers[command](update, context)
                self._handle_result(result, context, user_id)
                return

        if current_state != State.IDLE and current_state in self.state_handlers:
            for handler in self.state_handlers[current_state]:
                result = handler(update, context)
                self._handle_result(result, context, user_id)
                return

        if update.text and not update.is_command():
            for handler in self.message_handlers:
                handler(update, context)
                return
