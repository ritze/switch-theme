#!/bin/python3

import argparse
import pprint
import re
import shutil
import subprocess
import tomllib
from os.path import expanduser
from tempfile import mkstemp


"""Script to switch themes for different applications at once

The data structures are split into Themes and App.
A Theme stores the data: the used theme for each application
An App stores the action: what must be done to change the theme for this application.

"""


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


def switch_app_theme(app, theme, strategy, verbose=0, suppress_errors=False):
    """Switch the theme of an application.

    Args:
        app (str):              the application name
        theme (str):            the theme to switch to
        strategy (dict):        the strategy how to change the theme
        verbose (int):          the verbosity level with 0 for no messages
        suppress_errors (bool): supress error messages
    """

    ret = 0

    if verbose >= 2:
        print("setting {} to {}...".format(app, theme))

    if "file" in strategy and "pattern" in strategy and "replace" in strategy:
        file = expanduser(strategy["file"])
        pattern = strategy["pattern"]
        replace = strategy["replace"].format(theme)

        if verbose >= 3:
            print("  file:    {}".format(file))
            print('  pattern: "{}"'.format(pattern))
            print('  replace: "{}"'.format(replace))

        try:
            sed(pattern, replace, file)
        except FileNotFoundError:
            if not suppress_errors:
                print_error(
                    "couldn't set {} to {}: {} not found".format(app, theme, file)
                )
            ret = 1

    if "command" in strategy:
        command = strategy["command"].split(" ") + [theme]
        error = False

        try:
            ps = subprocess.run(command)
            if ps.returncode:
                error = True
        except FileNotFoundError:
            error = True
        if error and not suppress_errors:
            print_error("couldn't successfully run: {}".format(command))
            ret = 1

    return ret


def switch_theme(apps, themes, verbose=0):
    """Switch the theme to input_theme.

    Args:
        apps (dict):   the applications
        themes (dict): the themes
        verbose (int): the verbosity level with 0 for no messages
    """

    ret = 0

    if verbose >= 4:
        print("used apps configuration:")
        pprint.pprint(apps)
        print("used themes configuration:")
        pprint.pprint(themes)

    for app, strategy in apps.items():
        ret += switch_app_theme(app, themes[app], strategy, verbose)

    return 1 if ret > 0 else 0


def validate_config(config, verbose=0):
    """Validate if config only includes the categories as first level fields
       and all fields of aliases point to an available theme.

    Args:
        config (dict):     the config
        verbose (int):     the verbosity level with 0 for no messages
    """

    categories = ["aliases", "apps", "themes"]

    ret = True

    for key in categories:
        if key not in config.keys():
            if verbose >= 1:
                print('config invalid: "{}" not found'.format(key))
            ret = False

    for key in config.keys():
        if not key in categories:
            if verbose >= 1:
                print('config invalid: unknown field "{}"'.format(key))
            ret = False

    if "aliases" in config.keys() and "themes" in config.keys():
        for alias in config["aliases"].keys():
            theme = config["aliases"][alias]
            if not theme in config["themes"]:
                if verbose >= 1:
                    print(
                        'config invalid: unknown theme "{}" provided by alias "{}"'.format(
                            theme, alias
                        )
                    )
                ret = False

    return ret


def validate_theme_config(config, apps, verbose=0):
    """Validate if each theme covers each application

    Args:
        config (dict): the config
        apps (dict):   the applications
        verbose (int): the verbosity level with 0 for no messages
    """

    ret = True

    for key in apps.keys():
        if not key in config.keys():
            if verbose >= 1:
                print('config invalid: theme for "{}" not found'.format(key))
            ret = False

    return ret


def get_theme_config(config, theme, verbose=0):
    """Return the theme from config as a dict.

    If a field is not set, the value of the fallback theme will be taken. This behavior is not transitive.

    Args:
        config (dict): the config
        theme:         the theme name
        verbose (int): the verbosity level with 0 for no messages
    """

    theme_config = config["themes"][theme]

    if "fallback" in theme_config.keys():
        fallback_config = config["themes"][theme_config["fallback"]]
        for key, value in fallback_config.items():
            if not key in theme_config:
                theme_config[key] = value
        del theme_config["fallback"]

    return theme_config


def main():
    prog = __file__.split("/")[-1]

    parser = argparse.ArgumentParser(
        prog=prog, description="Set the themes for Gtk and specific applications."
    )
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="increase verbosity"
    )

    config = expanduser("~/.config/switch-theme/switch-theme.toml")
    with open(config, "rb") as file:
        config = tomllib.load(file)

    # Set verbose to 1 since the arguments cannot be parsed at this point
    if not validate_config(config, verbose=1):
        print_error("invalid config: missing fields")
        exit(1)

    themes = list(config["aliases"])
    [themes.append(x) for x in list(config["themes"]) if x not in themes]
    themes.sort()

    parser.add_argument("theme", choices=themes)

    try:
        args = parser.parse_args()
    except argparse.ArgumentTypeError as e:
        parser.print_help()
        exit(9)

    if args.verbose >= 5:
        print("parsed config:")
        pprint.pprint(config)

    theme = args.theme
    if theme in config["aliases"]:
        theme = config["aliases"][theme]

    theme_config = get_theme_config(config, theme, args.verbose)

    if not validate_theme_config(theme_config, config["apps"], verbose=args.verbose):
        print_error('invalid config: missing fields for theme "{}"'.format(theme))
        exit(1)

    if args.verbose >= 1:
        print("switching to {}...".format(theme))

    ret = switch_theme(config["apps"], theme_config, verbose=args.verbose)

    exit(ret)


if __name__ == "__main__":
    main()
