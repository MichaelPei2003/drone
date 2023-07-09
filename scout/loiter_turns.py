from dronekit import connect, VehicleMode

from pymavlink import mavutil


def loiter_turns(self,location):
    if not self.home_location:
        self.commands.download()
        self.commands.wait_ready()
    alt = location.alt - self.home_location.alt


    self._master.mav.command_int_send(0, 0, 0, 0,
                                           mavutil.mavlink.MAV_CMD_NAV_LOITER_TURNS, 2, 0, 2,
                                           1, 2, 0, location.lat, location.lon,
                                           alt)
    # if airspeed is not None:
    #     self.airspeed = airspeed
    # if groundspeed is not None:
    #     self.groundspeed = groundspeed