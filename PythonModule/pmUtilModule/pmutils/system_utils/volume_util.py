# coding:utf-8
from ctypes import cast

import comtypes
from _ctypes import POINTER
from pycaw.api.endpointvolume import IAudioEndpointVolume
from pycaw.utils import AudioUtilities


class VolumeUtil:
    def __init__(self):
        self.volumeInterface = self.getVolumeInterface()

    def getVolumeInterface(self):
        """ get volume interface"""
        try:
            devices = AudioUtilities.GetSpeakers()
            # noinspection PyProtectedMember
            interface = devices.Activate(IAudioEndpointVolume._iid_, 1, None)
            return cast(interface, POINTER(IAudioEndpointVolume))
        except comtypes.COMError:
            return None

    def getVolumeLevel(self):
        """ get volume level """
        return f"{self.volumeInterface.GetMasterVolumeLevelScalar()*100:.2f}"

    def clearMute(self):
        """ clear mute """
        volume = self.volumeInterface
        if volume is not None:
            volume.SetMute(0, None)
        return self

    def setMute(self):
        """ set mute """
        volume = self.volumeInterface
        if volume is not None:
            volume.SetMute(1, None)
        return self

    def setVolumeLevel(self, level: int):
        """ set volume level, range 0-100 """
        self.volumeInterface.SetMasterVolumeLevelScalar(level / 100, None)
        return self
