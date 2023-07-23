#!/usr/bin/env python3

""" Send2playlist is a script that takes the url of a video streaming service
as a parameter. With this URL, the script uses requests.get and re.search to
grab the URL's page title. With the URL and title stored in memory, it writes
both to a playlist file. The titles on the playlist file serve the purpose of
knowing at first glance what videos are on the playlist. This script is used in
conjunction with pdlnmpv. pdlnmpv is a dmenu and bash script with options to
execute send2playlist, check the contents of the playlist, and start playing
the it with mpv, plus others."""

from argparse import ArgumentParser, Namespace
from re import search, sub
from typing import Match, List
from urllib.request import urlopen, Request
import os
import sys


class NoTitleError(Exception):
    pass


def get_channel_name(url: str, content: str) -> str:
    """
    Scrapes a decoded content of a GET request result and scrapes the channel
    name from it using regex
    """
    channel_name: str = ""
    channel_name_match: Match[str] | None = None

    if "youtube" in url:
        channel_name_match = search(
            r'<link itemprop="name" content="([^"]*)">', content
        )
    elif "odysee" in url:
        channel_name_match = search(
            r'"author": {\n    "@type": "Person",\n    "name": "([^"]*)',
            content,
        )

    if channel_name_match:
        channel_name = channel_name_match.group(1)

    return channel_name


def get_title(url: str) -> str:
    """
    Makes a GET request to the url and scrapes the page title and channel name
    """
    # Request with headers was required because odysee links would throw 403
    # error when urlopen tryied to open them
    r = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        content: str = urlopen(r).read().decode()
        title: Match[str] | None = search(r"<\W*title\W*(.*)</title", content)

        channel_name: str = get_channel_name(url, content)

        if title and channel_name:
            return f"{channel_name} | {title.group(1)}"
        elif title:
            return title.group(1)
        else:
            raise NoTitleError
    except UnicodeDecodeError:
        raise NoTitleError


def yewtube_to_youtube(url: str) -> str:
    """
    Converts yewtu.be urls to youtube.com

    Avoid any connection problems that yewtube might have on a random day.
    Yewtu.be is an invidious instance, basically an alternative open source
    front end to youtube.com.

    """
    return f'https://youtube.com/{url.split("/")[-1]}'


def clean_title(title: str) -> str:
    """
    Cleans out bad encoding on quotation marks

    Requests from google sites returns html with bad encoding in
    ISO-8859-1. So characters like ' and " are shown as &#39; and &quot; I
    haven't found a solution to force the right utf-8 encoding so for now the
    script substitutes those two problems with their right character, using
    re.sub. Since a title can have simutaniously ' and ", the script uses two
    if statements instead of one if and one elif.
    """
    for pattern, repl in {"&#39;|&quot;": "'", "&amp;": "&"}.items():
        title = sub(pattern, repl, title)
    return title


def get_args() -> Namespace:
    parser = ArgumentParser(prog="send2playlist")
    options = [
        {
            "opt": ("urls",),
            "type": str,
            "nargs": "+",
            "help": "Urls to send to playlist",
        },
        {
            "opt": ("-p", "--playlist"),
            "help": "Urls to send to playlist",
            "default": os.environ["HOME"] + "/.local/share/playlist",
        },
    ]
    for option in options:
        parser.add_argument(*option.pop("opt"), **option)  # type: ignore
    return parser.parse_args()


def main() -> None:
    args: Namespace = get_args()

    lines: List[str] = []

    for url in args.urls:
        # url: str

        if "&pp=" in url:
            url = url[: url.find("&pp=")]

        if "yewtu" in url:
            url = yewtube_to_youtube(url)

        try:
            # Get's and cleans the title
            title: str = clean_title(get_title(url))
        except NoTitleError:
            continue

        if title.endswith("- YouTube"):
            # All youtube titles have '- Youtube' as a suffix, using find to get
            # the index of were the suffix is and with this index slicing the
            # str we clean the titles from it
            title = title[: title.find("- YouTube")]

        if title != "YouTube":
            # First checks if the title is not just 'Youtube'
            # (If it is just 'Youtube' it means the video had a problem, like a
            # url still marked as premiere or a live stream link to youtube that
            # hasn't started yet. So these kinds of links would fail silently
            # and just send a 'Youtube' as their title) only after this check
            # the title and url is appended to lines
            lines.append(f"{title.strip()} - {url}\n")

    if lines:
        with open(args.playlist, "a") as fh:
            # Appends title + url + newline to the playlist file
            # If the file doens't exists open() with the 'a' arg creates and
            # writes the new file, if it exists open() + fh.write appends the
            # title + url to the end of the file
            fh.write("".join(lines))
    else:
        # Exit with return value of 1 to let bash know something went wrong
        sys.exit(1)


if __name__ == "__main__":
    main()
