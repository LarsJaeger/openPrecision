import json


class Model:
    def to_dict(self) -> dict[str, any]:
        """Get a name-to-value dictionary of instance attributes of an arbitrary object."""
        try:
            print("d1")
            return vars(self)
        except TypeError:
            pass

        # object doesn't have __dict__, try with __slots__
        try:
            print("d2")
            slots = self.__slots__
        except AttributeError:
            # doesn't have __dict__ nor __slots__, probably a builtin like str or int
            return {}
        # collect all slots attributes (some might not be present)
        attrs = {}
        for name in slots:
            try:
                attrs[name] = getattr(self, name)
            except AttributeError:
                continue
        return attrs

    def to_json(self):
        return json.dumps(self.to_dict())
