{pkgs, ...}: {
  packages = with pkgs; [
    git
    gtk3
    cairo
    gtk-layer-shell
    meson
    go
    ninja
    gobject-introspection
    glib
    libffi
    libdbusmenu-gtk3
    gdk-pixbuf
    gnome-bluetooth
    cinnamon-desktop
    pkgconf
    pkg-config
    cmake
  ];

  enterTest = ''
    echo "Running tests"
    git --version | grep --color=auto "${pkgs.git.version}"
  '';

  languages.python = {
    enable = true;
    package = pkgs.python3.withPackages (ps:
      with ps; [
        pycairo
        setuptools
        cmake
        wheel
        psutil
      ]);
    venv = {
      enable = true;
      requirements = ''
        plyer
        wifi
        mypy
        git+https://github.com/Fabric-Development/fabric.git
      '';
    };
  };
}
