from runner import Runner
from drone_command_requester import DroneCommandRequester
from drone_state_receiver import DroneStateReceiver
from drone_video_receiver import DroneVideoReceiver
from dashboard import Dashboard

dashboard = Dashboard()
startables = [DroneCommandRequester(), DroneStateReceiver(), DroneVideoReceiver()]
runner = Runner()

runner.run(startables, dashboard)
