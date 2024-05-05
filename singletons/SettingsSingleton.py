from singletons.SingletonMeta import SingletonMeta


# TODO: Stworzyć klase, która będzie takim utils dla settingów wybranych przez usera
#  (np. będzie wyciągać z sesji jakieś rzeczy i walidować itd.)
class SettingsSingleton(metaclass=SingletonMeta):
    def __init__(self):
        pass
