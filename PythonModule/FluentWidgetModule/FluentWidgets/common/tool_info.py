# coding:utf-8
from typing import List

from PySide6.QtWidgets import QWidget
from ..components import ToolTipFilter, ToolTipPosition

def setToolTipInfo(widget: QWidget, info: str, time: int, position=ToolTipPosition.TOP_LEFT):
    """ 设置工具提示信息 """
    widget.setToolTip(info)
    widget.setToolTipDuration(time)
    widget.installEventFilter(ToolTipFilter(widget, 300, position))

def setToolTipInfos(
        widgets: List[QWidget],
        infos: List[str],
        time: List[int] | int,
        position: List[ToolTipPosition] | ToolTipPosition = ToolTipPosition.TOP_LEFT
):
    """ 设置多个工具提示信息 """
    time = [time for _ in range(len(widgets))] if type(time) is int else time
    position = [position for _ in range(len(widgets))] if type(position) is ToolTipPosition else position
    for widget, info, time, pos in zip(widgets, infos, time, position):
        setToolTipInfo(widget, info, time, pos)