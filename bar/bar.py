import math
from fabric.hyprland.widgets import ActiveWindow, WorkspaceButton, Workspaces
from fabric import Application, Fabricator
from fabric.widgets.label import Label
from fabric.widgets.box import Box
from fabric.utils import get_relative_path
from fabric.widgets.datetime import DateTime
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.widgets.centerbox import CenterBox
from fabric.audio.service import Audio
from plyer import battery


class VolumeWidget(Label):
    def __init__(self) -> None:
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

        self.set_label(str(math.floor(round(self.audio.speaker.volume))) + "%")


class BatteryWidget(Label):
    bat_percent: int = 0

    def update_bat_percent(self, v):
        # Update the percentage
        self.bat_percent = math.floor(round(v))
        self.set_label(str(self.bat_percent) + "%")
        # print(self.bat_percent)

        # On Low Battery
        self.on_battery_low()

    def on_battery_low(self):
        pass

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
                children=Workspaces(
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
                children=[ActiveWindow()],
            ),
            end_children=Box(
                orientation="h",
                spacing=10,
                children=[VolumeWidget(), BatteryWidget(), DateTime("%a %d %H:%M")],
            ),
        )

        self.add(self.header)
        self.show_all()


if __name__ == "__main__":
    app = Application("top-bar", Bar())
    app.set_stylesheet_from_file(get_relative_path("./style.css"))
    BatteryWidget()
    VolumeWidget()
    app.run()
