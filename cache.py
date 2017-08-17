import os
import errno


class Cache:
    """Class for cache."""

    def __init__(self, cache_path):
        self.cache_path = cache_path
        self.cache_file = cache_path + '/cache'

        # Create cache file if does not exist.
        if not os.path.exists(self.cache_file):
            open(self.cache_file, 'w+').close()

        # Create cache folder if does not exist.
        if not os.path.exists(self.cache_path):
            try:
                os.makedirs(self.cache_path)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

    def save_art(self, art):
        """Save art to cache folder."""
        f = open(self.cache_path + '/cover.jpg', 'wb')
        f.write(art)
        f.close()

    def get_art_from_cache(self):
        """Retreive art from the cache folder."""
        f = open(self.cache_path + '/cover.jpg', 'rb')
        art = f.read()
        f.close()
        return art

    def is_cache_consistent(self):
        """Checks if the cache is corrupt."""
        if not os.path.exists(self.cache_file):
            return True

    def has_album_changed(self, player):
        """Check if the album has changed since last run.
        This saves redownloading album art, except for in a few edge cases"""
        if not self.is_cache_consistent():
            # We will need to redownload anyway.
            return True

        album = player.get_album()
        artist = player.get_artist()

        # Check our cache
        cache = open(self.cache_file, 'r')
        cache_artist = cache.readline().rstrip()
        cache_album = cache.readline().rstrip()

        if (cache_artist == artist and cache_album == album):
            return False
        else:
            return True

    def update_cache(self, player):
        """Update the cache."""
        album = player.get_album()
        artist = player.get_artist()
        # Update cache
        os.remove(self.cache_file)
        new_cache = open(self.cache_file, 'w+')
        new_cache.write(artist + '\n' + album + '\n')
