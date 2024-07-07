#!/bin/python3

import argparse
import re
import shutil
from tempfile import mkstemp


"""Script to switch themes for different applications at once

The data structures are split into Themes and App.
A Theme stores the data: the used theme for each application
An App stores the action: what must be done to change the theme for this application.

"""


class Theme:
    """Base class for themes

    This class includes fallback themes. Don't use it directly.
    """

    alacritty = None
    gtk = None
    gnome_color_scheme = None
    rofi = "spotlight-dark"
    speedcrunch = None
    vscode = None


class DarkTheme(Theme):
    """Base class for dark themes

    This class includes fallback themes. Don't use it directly.
    """

    alacritty = "ayu-dark"
    gtk = "Adwaita-dark"
    gnome_color_scheme = "prefer-dark"
    speedcrunch = "Tomorrow Night"
    vscode = "Default Dark Modern"


class LightTheme(Theme):
    """Base class for light themes

    This class includes fallback themes. Don't use it directly.
    """

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


def print_error(*args):
    print("{}error:{}".format("\033[1;91m", "\033[0m"), *args)


def sed(pattern, replace, file, count=0):
    """Replace certain pattern in a file.

    In each line, replaces 'pattern' with 'replace'.

    Args:
        pattern (str): the pattern to match (can be re.pattern)
        replace (str): the replacement string
        file (str):    the path to file
        count (int):   the number of occurrences to replace
    """

    num_replaced = count
    source_fd = open(file, "r")

    _, temp = mkstemp()
    dest_fd = open(temp, "w")

    for line in source_fd:
        new_line = re.sub(pattern, replace, line)
        dest_fd.write(new_line)

        if new_line != line:
            num_replaced += 1
        if count and num_replaced > count:
            break

    dest_fd.writelines(source_fd.readlines())

    source_fd.close()
    dest_fd.close()

    shutil.move(temp, file)


class Replacement:
    file = None
    pattern = None
    replace = None

    def __init__(self, file, pattern, replace):
        self.file = file
        self.pattern = pattern
        self.replace = replace


class App:
    name = None
    replacement = None


class Alacritty(App):
    name = "Alacritty"
    replacement = Replacement(
        file="/home/mlu/.config/alacritty/alacritty.toml",
        pattern='^(import = \\[".*)\\/.*.toml*',
        replace="\\1/{}.toml",
    )


class CodeOSS(App):
    name = "Code OSS"
    replacement = Replacement(
        file="/home/mlu/.config/Code - OSS/User/settings.json",
        pattern='"workbench.colorTheme":.*',
        replace='"workbench.colorTheme": "{}"',
    )


class VSCode(App):
    name = "Visual Studio Code"
    replacement = Replacement(
        file="/home/mlu/.config/Code/User/settings.json",
        pattern='"workbench.colorTheme":.*',
        replace='"workbench.colorTheme": "{}"',
    )


def switch_app_theme(app, theme, verbose=0, suppress_errors=False):
    """Switch the theme of an application.

    Args:
        app (str):              the application
        theme (str):            the theme to switch to
        verbose (int):          the verbosity level with 0 for no messages
        suppress_errors (bool): supress error messages
    """

    ret = 0

    if verbose >= 2:
        print("setting {} to {}...".format(app.name, theme))

    if app.replacement:
        file = app.replacement.file
        pattern = app.replacement.pattern
        replace = app.replacement.replace.format(theme)

        if verbose >= 3:
            print("  file:    {}".format(file))
            print('  pattern: "{}"'.format(pattern))
            print('  replace: "{}"'.format(replace))

        try:
            sed(pattern, replace, file)
        except FileNotFoundError:
            if not suppress_errors:
                print_error(
                    "couldn't set {} to {}: {} not found".format(app.name, theme, file)
                )
            ret = 1

    return ret


def switch_theme(input_theme, verbose=0):
    """Switch the theme to input_theme.

    Args:
        input_theme (str): the theme to switch to
        verbose (int):     the verbosity level with 0 for no messages
    """

    theme = input_to_theme_map[input_theme]
    if verbose >= 1:
        print("switching to {}...".format(theme.__name__))

    ret = 0
    ret += switch_app_theme(Alacritty, theme.alacritty, verbose)
    ret += switch_app_theme(CodeOSS, theme.vscode, verbose)
    ret += switch_app_theme(VSCode, theme.vscode, verbose)

    return 1 if ret > 0 else 0


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
