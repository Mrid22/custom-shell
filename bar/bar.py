import math
from fabric.hyprland.widgets import (
    HyprlandActiveWindow,
    WorkspaceButton,
    HyprlandWorkspaces,
)
from fabric import Application, Fabricator
from fabric.widgets.eventbox import EventBox
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
        track = f" {title} - {artist}" if artist else ""
        self.set_label(track)


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
        if v <= 25:
            self.on_battery_low()
        else:
            BatteryWidget.remove_style_class(self, "low-battery")

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


player = PlayerWidget()


class PopupWindow(Window):
    def __init__(
        self,
        parent: Window,
        pointing_to: player,
        margin: tuple[int, ...] | str = "0px 0px 0px 0px",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.exclusivity = "none"

        self._parent = parent
        self._pointing_widget = pointing_to
        self._base_margin = self.extract_margin(margin)
        self.margin = self._base_margin.values()

        self.connect("notify::visible", self.do_update_handlers)

    def get_coords_for_widget(self, widget: Gtk.Widget) -> tuple[int, int]:
        if not ((toplevel := widget.get_toplevel()) and toplevel.is_toplevel()):  # type: ignore
            return 0, 0
        allocation = widget.get_allocation()
        x, y = widget.translate_coordinates(toplevel, allocation.x, allocation.y) or (
            0,
            0,
        )
        return round(x / 2), round(y / 2)

    def set_pointing_to(self, widget: Gtk.Widget | None):
        if self._pointing_widget:
            try:
                self._pointing_widget.disconnect_by_func(self.do_handle_size_allocate)
            except Exception:
                pass
        self._pointing_widget = widget
        return self.do_update_handlers()

    def do_update_handlers(self, *_):
        if not self._pointing_widget:
            return

        if not self.get_visible():
            try:
                self._pointing_widget.disconnect_by_func(self.do_handle_size_allocate)
                self.disconnect_by_func(self.do_handle_size_allocate)
            except Exception:
                pass
            return

        self._pointing_widget.connect("size-allocate", self.do_handle_size_allocate)
        self.connect("size-allocate", self.do_handle_size_allocate)

        return self.do_handle_size_allocate()

    def do_handle_size_allocate(self, *_):
        return self.do_reposition(self.do_calculate_edges())

    def do_calculate_edges(self):
        move_axe = "x"
        parent_anchor = self._parent.anchor

        if len(parent_anchor) != 3:
            return move_axe

        if (
            GtkLayerShell.Edge.LEFT in parent_anchor
            and GtkLayerShell.Edge.RIGHT in parent_anchor
        ):
            # horizontal -> move on x-axies
            move_axe = "x"
            if GtkLayerShell.Edge.TOP in parent_anchor:
                self.anchor = "left top"
            else:
                self.anchor = "left bottom"
        elif (
            GtkLayerShell.Edge.TOP in parent_anchor
            and GtkLayerShell.Edge.BOTTOM in parent_anchor
        ):
            # vertical -> move on y-axies
            move_axe = "y"
            if GtkLayerShell.Edge.RIGHT in parent_anchor:
                self.anchor = "top right"
            else:
                self.anchor = "top left"

        return move_axe

    def do_reposition(self, move_axe: str):
        parent_margin = self._parent.margin
        parent_x_margin, parent_y_margin = parent_margin[0], parent_margin[3]

        height = self.get_allocated_height()
        width = self.get_allocated_width()

        if self._pointing_widget:
            coords = self.get_coords_for_widget(self._pointing_widget)
            coords_centered = (
                round(coords[0] + self._pointing_widget.get_allocated_width() / 2),
                round(coords[1] + self._pointing_widget.get_allocated_height() / 2),
            )
        else:
            coords_centered = (
                round(self._parent.get_allocated_width() / 2),
                round(self._parent.get_allocated_height() / 2),
            )

        self.margin = tuple(
            a + b
            for a, b in zip(
                (
                    (
                        0,
                        0,
                        0,
                        round((parent_x_margin + coords_centered[0]) - (width / 2)),
                    )
                    if move_axe == "x"
                    else (
                        round((parent_y_margin + coords_centered[1]) - (height / 2)),
                        0,
                        0,
                        0,
                    )
                ),
                self._base_margin.values(),
            )
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
                    player,
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
