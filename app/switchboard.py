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

        if not isinstance(raw_call, str):
            raise TypeError('Входные данные должны быть типом str')

        all_info = raw_call.split(",")
        if len(all_info) != 6:
            raise ValueError('Введенные данные не соответствуют, требуется 6 элементов')

        caller_id, receiver_id = self._id_check(all_info[0], all_info[3])
        self._name_check(all_info[1], all_info[4])
        self._phone_check(all_info[2], all_info[5])

        caller = self._create_user(caller_id, all_info[1], all_info[2])
        receiver = self._create_user(receiver_id, all_info[4], all_info[5])

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


    def _id_check(self, caller_id: str, receiver_id: str) -> tuple[int, int]:
        try:
            caller_id = int(caller_id)
            receiver_id = int(receiver_id)
            return caller_id, receiver_id
        except ValueError:
            raise ValueError('id должен быть числом')


    def _name_check(self, caller_name: str, receiver_name: str) -> None:
        if not caller_name.strip() or not receiver_name.strip():
            raise ValueError('Поле "Имя Фамилия" не должно быть пустым')

        if not caller_name.replace(" ", "").isalpha() or not receiver_name.replace(" ", "").isalpha():
            raise ValueError('Поле "Имя Фамилия" должно состоять только из букв (пробелы допустимы)')


    def _phone_check(self, caller_phone: str, receiver_phone: str) -> None:
        if not caller_phone.strip() or not receiver_phone.strip():
            raise ValueError('Номер телефона не должен быть пустым')

        if not caller_phone.strip().startswith('+') or not receiver_phone.strip().startswith('+'):
            raise ValueError('Номер телефона должен начинаться с "+"')

        if not caller_phone.strip()[1:].isdigit() or not receiver_phone.strip()[1:].isdigit():
            raise ValueError('Номер телефона должен содержать только цифры после "+"')


    def _create_user(self, id_user: int, name: str, phone: str) -> User:
        if phone.startswith("+7"):
            return LocalUser(id_user, name, phone)
        else:
            return ForeignUser(id_user, name, phone)
