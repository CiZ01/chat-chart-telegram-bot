class ContextApi():
    msg_text = {}
    btn_text = {}

    userid = None
    user_lang = None
    social = None

    def __init__(self):
        return

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __delitem__(self, key):
        setattr(self, key, None)

    def __contains__(self, key):
        return hasattr(self, key)

    def __repr__(self) -> str:
        return str(self.__dict__)
