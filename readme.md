# spofiyart

Spofiyart is a small application written in Python3 for retreiving album art automagically for the music you're currently listening to.

## What?

When you run spofiyart, spofiyart will read player information from [MPRIS](https://specifications.freedesktop.org/mpris-spec/latest/). Then:

- If your music has album art already attached, spofiyart will find it. 
- If it doesn't, spofiyart will retreive some from Musicbrainz. 
- It will then save it to its cache folder (~/.cache/spofiyart)
- If you specify the -b option, it will also pipe to STDOUT.

## Why is it 'spofiyart'?

The Spotify Linux client implements the MPRIS interface. However, it provides a URL for album art from Spotify's CDN. The quality of this image is poor - low resolution, with artifacts and the spotify logo overlayed. 

I use Spotify a lot, but for my personal local music library I meticulously keep album art attached.

Spofiyart will retreive the album art from Musicbrainz. But when I'm using my local files with Clementine it won't waste bandwidth retreiving Musicbrainz art. Spofiyart allows for this flexibility.

## Isn't this all sort of pointless?

Yes.

## Why?

I wanted an album art popup in the top left corner of my desktop environment. Like I say...

# Usage

```
python __main__.py -b >> test.jpeg
```

For more options, try:
```
python __main__.py --help
```

# Todo List

- Spofiyart should cache artworks more permenantly to avoid redownloading wherever possible.
