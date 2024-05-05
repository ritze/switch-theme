#!/bin/python3

import argparse


# This theme includes fallback themes and shouldn't be used directly.
class Theme:
    alacritty = None
    gtk = None
    gnome_color_scheme = None
    rofi = "spotlight-dark"
    speedcrunch = None
    vscode = None


# This theme includes fallback themes and shouldn't be used directly.
class DarkTheme(Theme):
    alacritty = "ayu-dark"
    gtk = "Adwaita-dark"
    gnome_color_scheme = "prefer-dark"
    speedcrunch = "Tomorrow Night"
    vscode = "Default Dark Modern"


# This theme includes fallback themes and shouldn't be used directly.
class LightTheme(Theme):
    alacritty = "onehalf-light"
    gtk = "Adwaita"
    gnome_color_scheme = "prefer-light"
    speedcrunch = "Standard"
    vscode = "Atom One Light"


# This theme includes fallback themes and shouldn't be used directly.
# class DimmedDarkTheme(DarkTheme):
#     alacritty = "onehalf-dark"  # fallback


# This theme includes fallback themes and shouldn't be used directly.
# class DimmedLightTheme(LightTheme):
#     alacritty = "gruvbox-light"  # fallback


class AyuDarkTheme(DarkTheme):
    alacritty = "ayu-dark"

    def __str__(self):
        return "Ayu Dark"

    def __repr__(self):
        return "REPR: Ayu Dark"


class AyuLightTheme(LightTheme):
    alacritty = "ayu-light"


# class AyuMirageTheme:
#    alacritty = "ayu-mirage"


class GruvboxDarkTheme(DarkTheme):
    alacritty = "gruvbox-dark"
    vscode = "Gruvbox Material Dark"


class GruvboxLightTheme(LightTheme):
    alacritty = "gruvbox-light"
    vscode = "Gruvbox Material Light"


class OnehalfDarkTheme(DarkTheme):
    alacritty = "onehalf-dark"
    vscode = "Atom One Dark"


class OnehalfLightTheme(LightTheme):
    alacritty = "onehalf-light"
    vscode = "Atom One Light"


# Don't use the directly the (Dimmed) DarkTheme or (Dimmed) LightTheme. Those are used
# for fallback values for the actual themes. Only map concrete themes here.
input_to_theme_map = {
    # dark mode
    "d": AyuDarkTheme,
    "dark": AyuDarkTheme,
    # dimmed light mode
    "L": GruvboxLightTheme,
    "dimmed-light": GruvboxLightTheme,
    # light mode
    "l": OnehalfLightTheme,
    "light": OnehalfLightTheme,
    # dimmed dark mode
    "D": OnehalfDarkTheme,
    "dimmed-dark": GruvboxDarkTheme,
    # themes
    "ayu-dark": AyuDarkTheme,
    "gruvbox-dark": GruvboxDarkTheme,
    "gruvbox-light": GruvboxLightTheme,
    "onehalf-dark": OnehalfDarkTheme,
    "onehalf-light": OnehalfLightTheme,
}


def switch_theme(input_theme, verbose=0):
    theme = input_to_theme_map[input_theme]
    if verbose == 1:
        print("Switching to {}...".format(theme.__name__))

    return 0


def main():
    prog = __file__.split("/")[-1]

    parser = argparse.ArgumentParser(
        prog=prog, description="Set the themes for Gtk and specific applications."
    )
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="increase verbosity"
    )

    # TODO: Add better usage text
    parser.add_argument(
        "theme",
        choices=[
            # light mode
            "l",
            "light",
            # dimmed light mode
            "L",
            "dimmed-light",
            # dimmed dark mode
            "D",
            "dimmed-dark",
            # dark mode
            "d",
            "dark",
            # themes
            "ayu-dark",
            "gruvbox-light",
            "onehalf-dark",
            "onehalf-light",
        ],
        help="test",
    )

    try:
        args = parser.parse_args()
    except argparse.ArgumentTypeError as e:
        parser.print_help()
        exit(9)

    ret = switch_theme(args.theme, verbose=args.verbose)

    exit(ret)


if __name__ == "__main__":
    main()
