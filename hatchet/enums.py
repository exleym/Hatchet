

# TODO: should this be an actual Enum?
class LocationTypeEnum:
    HOME = 1
    AWAY = 2
    NEUTRAL = 3

    @classmethod
    def from_id(cls, id):
        type_map = {1: 'HOME', 2: 'AWAY', 3: 'NEUTRAL'}
        return type_map.get(id)
