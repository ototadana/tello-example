import socket


class DroneStateReceiver:
    def start(self, info):
        state_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        state_sock.bind(("", 8890))

        while info.is_active():
            try:
                data, _ = state_sock.recvfrom(1024)
                info.set_states(self.__get_drone_state(data))
            except Exception:
                print("\nExit . . .\n")
                break

    def __get_drone_state(self, data):
        s = data.decode(errors="replace")
        values = s.split(";")
        state = {}
        for v in values:
            kv = v.split(":")
            if len(kv) > 1:
                state[kv[0]] = float(kv[1])
        return state
