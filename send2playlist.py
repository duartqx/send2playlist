#!/usr/bin/env python3

""" Send2playlist is a script that takes the url of a video streaming service
as a parameter. With this URL, the script uses requests.get and re.search to
grab the URL's page title. With the URL and title stored in memory, it writes
both to a playlist file. The titles on the playlist file serve the purpose of
knowing at first glance what videos are on the playlist. This script is used in
conjunction with pdlnmpv. pdlnmpv is a dmenu and bash script with options to
execute send2playlist, check the contents of the playlist, and start playing
the it with mpv, plus others."""

from sys import argv, exit as _exit
from urllib.request import urlopen, Request
from re import search, sub
from typing import Match


PLAYLIST_FILE = ".local/share/playlist"
# The playlist file to be appended with open()


class NoTitleError(Exception):
    pass


def get_title(url: str) -> str:
    """urllib.request.urlopen is used to get the url html content. With
    re.search the script scrapes and finds the page's title"""
    # Request with headers was required because odysee links would throw 403
    # error when urlopen tryied to open them
    r: Request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        content: str = urlopen(r).read().decode("UTF-8")
        title: Match[str] | None = search(r"<\W*title\W*(.*)</title", content)
        if title:
            return title.group(1)
        else:
            raise NoTitleError
    except UnicodeDecodeError:
        raise NoTitleError


def yewtube_to_youtube(url: str) -> str:
    """Converts yewtu.be url to youtube.com url to avoid any connection pro-
    blem that yewtube might have on a random day . Yewtu.be is an invidious
    instance, basically an alternative open source front end to youtube.com.
    Anyone can host their own instance of invidious, and many do. This function
    can be used with any other invidious instances other than yewtu.be, but the
    original url must end in a valid youtube's url"""
    return f'https://youtube.com/{url.split("/")[-1]}'


def clean_title(title: str) -> str:
    """requests from google sites returns html with bad encoding in
    ISO-8859-1. So characters like ' and " are shown as &#39; and &quot; I
    haven't found a solution to force the right utf-8 encoding so for now the
    script substitutes those two problems with their right character, using
    re.sub. Since a title can have simutaniously ' and ", the script uses two
    if statements instead of one if and one elif."""
    for pattern, repl in zip(["&#39;|&quot;", "&amp;"], ["'", "&"]):
        title = sub(pattern, repl, title)
    return title


def main() -> None:

    # Gets the url that was passed as an argument
    if len(argv) > 1:
        url: str = argv[1]
    else:
        print("You need to pass an url as first argument!")
        _exit(1)

    if "yewtu" in url:
        url = yewtube_to_youtube(url)

    # Get's and cleans the title
    title: str = clean_title(get_title(url))

    if title.endswith("- YouTube"):
        # All youtube titles have '- Youtube' as a suffix, using find to get
        # the index of were the suffix is and with this index slicing the str
        # we clean the titles from it
        title = title[: title.find("- YouTube")]

    if title != "YouTube":
        # First checks if the title is not just 'Youtube'
        # (If it is just 'Youtube' it means the video had a problem, like a url
        # still marked as premiere or a live stream link to youtube that hasn't
        # started yet. So these kinds of links would fail silently and just send a
        # 'Youtube' as their title)
        # only after this check the title and url is written to the playlist file

        with open(PLAYLIST_FILE, "a") as fh:
            # Appends title + url + newline to the playlist file
            # If the file doens't exists open() with the 'a' arg creates and
            # writes the new file, if it exists open() + fh.write appends the
            # title + url to the end of the file
            fh.write(f"{title} - {url}\n")
    else:
        # Exists with return value of 1 so that it can be captured by bash and
        # the script send2notify executes the notification of an error, or
        # success if the url and title were appended to the playlist file
        _exit(1)


if __name__ == "__main__":

    try:
        main()
    except NoTitleError:
        _exit(1)
