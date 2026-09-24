import math
from fabric.hyprland.widgets import (
    HyprlandActiveWindow,
    WorkspaceButton,
    HyprlandWorkspaces,
)
from fabric import Application, Fabricator
from fabric.widgets.label import Label
from fabric.widgets.box import Box
from fabric.utils import get_relative_path
from fabric.widgets.datetime import DateTime
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.widgets.centerbox import CenterBox
from fabric.audio.service import Audio
from plyer import battery, wifi
import gi

gi.require_version("Playerctl", "2.0")

from gi.repository import Playerctl


class PlayerWidget(Label):
    def __init__(self):
        super().__init__("")
        self.player = None
        self.manager = Playerctl.PlayerManager()
        self.manager.connect("name-appeared", self.on_name_appeared)
        self.manager.connect("player-vanished", self.on_player_vanished)
        self.manager.connect("name-vanished", self.on_name_vanished)
        for name in self.manager.props.player_names:
            self.on_name_appeared(self.manager, name)

    def on_name_appeared(self, manager, name):
        if self.player is not None:
            return
        self.player = Playerctl.Player.new_from_name(name)
        self.player.connect("playback-status::playing", self.on_playing)
        self.player.connect("playback-status::paused", self.on_paused)
        self.player.connect("playback-status::stopped", self.on_stopped)
        self.player.connect("metadata", self.on_metadata)
        manager.manage_player(self.player)
        self.update_label()

    def on_player_vanished(self, manager, player):
        if player is self.player:
            self.player = None
            self.set_label("")

    def on_name_vanished(self, manager, name):
        if self.player is None:
            return
        if self.player.props.player_name == getattr(name, "name", ""):
            self.player = None
            self.set_label("")

    def on_playing(self, player, status):
        self.update_label()

    def on_paused(self, player, status):
        self.update_label()

    def on_stopped(self, player, status):
        self.set_label("")

    def on_metadata(self, player, metadata):
        self.update_label()

    def update_label(self):
        if self.player is None:
            return
        title = self.player.get_title()
        artist = self.player.get_artist()
        status = self.player.props.playback_status
        if (
            status != Playerctl.PlaybackStatus.PLAYING
            and status != Playerctl.PlaybackStatus.PAUSED
        ):
            self.set_label("")
            return
        icon = "▶ " if status == Playerctl.PlaybackStatus.PLAYING else "⏸ "
        track = f"{artist} - {title}" if artist else title
        self.set_label(f"{icon}{track}")


class WifiWidget(Label):
    def __init__(self):
        super().__init__("")
        self.connected = wifi.is_connected()
        self.wifi_names = wifi.get_available_wifi()
        self.wifi_info = wifi.get_network_info(self.wifi_names[0])
        self.wifi_name = self.wifi_info["ssid"]
        self.set_label(self.wifi_name)

        self.wifi_fabricator = Fabricator(
            interval=500,
            default_value=100,
            poll_from=lambda _: self.wifi_info["ssid"],
            on_changed=lambda f, v: self.update_wifi_name(v),
        )

    def update_wifi_name(self, v):
        self.set_label(v)


class VolumeWidget(Label):
    def __init__(self):
        super().__init__("")

        self.audio = Audio(notify_speaker=self.on_speaker_changed)
        self.vol_fabricator = Fabricator(
            interval=500,
            default_value=100,
            poll_from=lambda _: self.audio,
            on_changed=lambda f, v: self.on_speaker_changed(),
        )

    def on_speaker_changed(self):
        if not self.audio.speaker:
            return
        volume = math.floor(round(self.audio.speaker.volume))
        mute_indicator = " (Muted)" if self.audio.speaker.muted else ""
        self.set_label(f"{volume}%{mute_indicator}")


class BatteryWidget(Label):
    bat_percent: int = 0

    def update_bat_percent(self, v):
        # Update the percentage
        self.bat_percent = math.floor(round(v))
        self.set_label(str(self.bat_percent) + "%")

        # On Low Battery
        if v <= 20:
            self.on_battery_low()

    def on_battery_low(self):
        BatteryWidget.add_style_class(self, "low-battery")

    def __init__(self) -> None:
        super().__init__("")
        self.battery_fabricator = Fabricator(
            interval=500,
            default_value=100,
            poll_from=lambda _: battery.status["percentage"],
            on_changed=lambda f, v: self.update_bat_percent(v),
        )


class Bar(Window):

    def __init__(self, **kwargs):
        super().__init__(
            layer="top",
            anchor="top right left",
            exclusivity="auto",
            **kwargs,
        )

        self.header = CenterBox(
            name="header",
            start_children=Box(
                orientation="h",
                spacing=10,
                children=HyprlandWorkspaces(
                    name="Workspaces",
                    spacing=10,
                    buttons_factory=lambda ws_id: WorkspaceButton(
                        id=ws_id, label=str(ws_id)
                    ),
                ),
            ),
            center_children=Box(
                orientation="h",
                spacing=10,
                children=[HyprlandActiveWindow()],
            ),
            end_children=Box(
                orientation="h",
                spacing=10,
                children=[
                    PlayerWidget(),
                    WifiWidget(),
                    VolumeWidget(),
                    BatteryWidget(),
                    DateTime("%a %d %H:%M"),
                ],
            ),
        )

        self.add(self.header)
        self.show_all()


if __name__ == "__main__":
    app = Application("top-bar", Bar())
    app.set_stylesheet_from_file(get_relative_path("./style.css"))
    BatteryWidget()
    WifiWidget()
    VolumeWidget()
    app.run()
