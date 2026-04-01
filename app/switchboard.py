from __future__ import annotations

from dataclasses import dataclass

from app.users import LocalUser, ForeignUser
from app.users import User


LOCAL_PHONE_PREFIX = "+7"


@dataclass(slots=True)
class ActiveCall:
    caller: User
    receiver: User

    @property
    def is_cross_border(self) -> bool:
        return type(self.caller) is not type(self.receiver)


class Switchboard:
    def __init__(self) -> None:
        self._active_calls: list[ActiveCall] = []
        self._active_calls_count = 0
        self._cross_border_calls_count = 0

    def register_call(self, raw_call: str) -> ActiveCall:

        all_info = raw_call.split(",")

        if all_info[2].startswith("+7"):
            caller = LocalUser(int(all_info[0]), all_info[1], all_info[2])
        else:
            caller = ForeignUser(int(all_info[0]), all_info[1], all_info[2])

        if all_info[5].startswith("+7"):
            receiver = LocalUser(int(all_info[3]), all_info[4], all_info[5])
        else:
            receiver = ForeignUser(int(all_info[3]), all_info[4], all_info[5])

        call = ActiveCall(caller, receiver)

        self._active_calls.append(call)

        self._active_calls_count += 1

        if call.is_cross_border:
            self._cross_border_calls_count += 1

        return call

    def get_active_calls_count(self) -> int:
        return self._active_calls_count

    def get_cross_border_calls_count(self) -> int:
        return self._cross_border_calls_count
