import enum

class StateEnumMeta(enum.EnumMeta):
    def __contains__(self, item):
        try:
            self(item)
        except ValueError:
            return False
        else:
            return True


class BaseState(enum.Enum, metaclass=StateEnumMeta):
    pass

def states_as_list(state_type: BaseState):
    return list(map(lambda c: (c.value, c.name), state_type))

class UserState(str, BaseState):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class UserGenderType(str, BaseState):
    MALE = "Male"
    FEMALE = "Female"
    PREFER_NOT_TO_SAY = "Prefer not to say"