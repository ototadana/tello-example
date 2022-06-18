class Info:
    def __init__(self):
        self.__state = {}
        self.__is_active = True
        self.__image = None
        self.__command = ""
        self.__sent_command = ""
        self.__result = ""

    def set_states(self, states):
        self.__state = states

    def get_states(self):
        return self.__state

    def get_state(self, name):
        return self.__state.get(name, 0.0)

    def is_active(self):
        return self.__is_active

    def stop(self):
        self.__is_active = False

    def set_image(self, image):
        self.__image = image

    def get_image(self):
        return self.__image

    def entry_command(self, command):
        self.__command = command

    def pick_command(self):
        command = self.__command
        self.__command = ""
        return command

    def set_sent_command(self, command):
        self.__sent_command = command

    def get_sent_command(self):
        return self.__sent_command

    def set_command_result(self, result):
        self.__result = result

    def get_command_result(self):
        return self.__result
