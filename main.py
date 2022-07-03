import argparse
from runner import Runner
from drone_command_requester import DroneCommandRequester
from drone_state_receiver import DroneStateReceiver
from drone_video_receiver import DroneVideoReceiver
from dashboard import Dashboard
from stub_command_requester import StubCommandRequester
from stub_state_receiver import StubStateReceiver
from stub_video_receiver import StubVideoReceiver

parser = argparse.ArgumentParser()
parser.add_argument(
    "-s", "--stub", help="use stubs instead of a drone", action="store_true"
)
parser.add_argument(
    "-w", "--webcam", help="webcam device id (for stub)", type=int, default=0
)
args = parser.parse_args()

if args.stub:
    startables = [
        StubCommandRequester(),
        StubStateReceiver(),
        StubVideoReceiver(args.webcam),
    ]
else:
    startables = [DroneCommandRequester(), DroneStateReceiver(), DroneVideoReceiver()]

dashboard = Dashboard()
runner = Runner()

runner.run(startables, dashboard)
