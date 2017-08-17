import sys
import os
import cache
import fetch
import argparse
import gi
gi.require_version('Playerctl', '1.0')
from gi.repository import Playerctl


def main():
    """Jumping off point"""
    # Set up argument parser.
    parser = argparse.ArgumentParser(description='Gives you album art for' +
                                     ' currently playing music')
    parser.add_argument('-b', '--binary', dest='binary',
                        action='store_const', const=1,
                        help='Push binary to stdout.')
    parser.add_argument('-c', '--cache', dest='cache', action='store',
                        help='Specify a path to use as a cache.' +
                        ' The default is ~/.cache/spofiyart')
    parser.add_argument('-m', '--mbrainz', dest='mbrainz',
                        action='store_const', const=1,
                        help='Prefer musicbrainz for all art.')
    parser.add_argument('-f', '--fallback', dest='fallback', action='store',
                        help='Use specified fallback art.')
    parser.add_argument('-s', '--size', dest='size', action='store',
                        help='Specify the size of downloaded' +
                        ' musicbrainz art - either 250 or 500')
    args = parser.parse_args()

    # Musicbrainz image size
    if args.size is not None:
        if args.size != '250' and args.size != '500':
            print('Invalid size given')
            sys.exit(1)
        brainz_size = int(args.size)
    else:
        brainz_size = None

    # Set up playerctl mpris interface and needed vars.
    player = Playerctl.Player()
    player_name = player.get_property('player-name')

    # And set up cache dir
    cache_path = os.getenv("HOME") + '/.cache/spofiyart'
    my_cache = cache.Cache(cache_path)

    # Main tasks.
    if not my_cache.has_album_changed(player):
        # Just retreive from cache.
        if args.binary == 1:
            art = my_cache.get_art_from_cache()
        else:
            sys.exit()
    else:
        my_cache.update_cache(player)

    if player_name == 'spotify' or args.mbrainz == 1:
        # Art that spotify provides is garbage.
        art = fetch.fetch_art(player, musicbrainz=True, art_size=brainz_size)
    else:
        art = fetch.fetch_art(player)

    # Check for failure.
    if art is False:
        if args.fallback is not None:
            f = open(args.fallback, 'rb')
            art = f.read()
            f.close()
        else:
            print('Failed to get art for the currently playing song.',
                  file=sys.stderr)
            print('1. Ensure that your songs have album art attached.',
                  file=sys.stderr)
            print('2. Ensure that your songs are properly' +
                  ' labeled for Musicbrainz',
                  file=sys.stderr)
            print('3. Use the -f flag to return a fallback' +
                  ' image for exceptions.',
                  file=sys.stderr)
            sys.exit(1)

    if args.binary == 1:
        sys.stdout.buffer.write(art)
    my_cache.save_art(art)


main()
