#!/bin/python3

import argparse


def switch_theme(theme, verbose=0):
    if verbose == 1:
        print("Switching to {}...".format(theme))

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
