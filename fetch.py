import musicbrainzngs
import urllib.parse as urlparse
import urllib.request as urlreq


def fetch_art(player, musicbrainz=False, art_size=None):
    """Fetches album art the best way possible"""
    album = player.get_album()
    artist = player.get_artist()
    art = False

    if musicbrainz is True:
        # Attempt using musicbrainz first.
        art = fetch_from_musicbrainz(album, artist, art_size)

    if art is not False:
        return art
    else:
        # Attempt using url.
        try:
            metadata = player.get_property('metadata')
            url = metadata['mpris:artUrl']
            art = fetch_from_url(url)
        except KeyError:
            art = False

    if art is not False:
        return art
    else:
        # Failover attempt with musicbrainz.
        art = fetch_from_musicbrainz(album, artist, art_size)
    return art


def fetch_from_musicbrainz(search_album, search_artist, art_size):
    """Fetches album art from musicbrainz."""
    try:
        musicbrainzngs.set_useragent('Spofiyart',
                                     '0.1')
        search_result = musicbrainzngs.search_releases(artist=search_artist,
                                                       release=search_album)
        song_id = search_result['release-list'][0]['release-group']['id']
        data = musicbrainzngs.get_release_group_image_front(song_id,
                                                            size=art_size)
        return data
    except (musicbrainzngs.ResponseError,
            musicbrainzngs.NetworkError,
            ValueError) as e:
        # Broadly catch failures as we just want to return false for them.
        return False


def fetch_from_url(url):
    """Fetches album art from url"""
    # Which protocol? Http or file
    protocol = url.split(':')[0]

    if protocol == 'http' or protocol == 'https':
        return urlreq.urlopen(url).read()
    elif protocol == 'file':
        p = urlparse.urlparse(url)
        # Need this to remove character encoding e.g. %20
        file_name = urlreq.url2pathname(p.path)
        f = open(file_name, 'rb')
        data = f.read()
        f.close()
        return data
    else:
        return False
