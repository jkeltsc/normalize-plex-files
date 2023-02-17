import getopt
import sys
import os
from types import SimpleNamespace


def getconfig() -> SimpleNamespace:
    """Gets various config variables from the environment or from the commandline."""

    def usage():
        print(f"""usage: normalize-plex-files {{-m [-T] | -T [-m]}} [--armed] [-d] [-D database] \\
                [-b moviedir] [-l libraryname] [-s #subdirs] [-o] \\
                [-B seriesdir] [-L libraryname] [-S #subdirs] [-O]

    Arguments and Environment Variables:
             --armed                                     run armed, default: unarmed (no files touched)
        -r | --rmdotfiles           PLEX_RMDOTFILES      remove dotfiles in media dirs before rmdir, env/default: {config.rmdotfiles}
        -m | --movies                                    process movie files, default: do not process movies
        -b | --moviesbase dir       PLEX_MOVIESBASE      movie files directory, env/default: {config.moviesbase}
        -l | --movieslibrary name   PLEX_MOVIESLIBRARY   movies library name, eenv/default: {config.movieslibrary}
        -s | --moviessubdirs #      PLEX_MOVIESSUBDIRS   levels of subdirs to retain, env/default: {config.moviessubdirs}
        -o | --ownmoviefolder       PLEX_OWNMOVIEFOLDER  pack each movie in its own movie folder, env/default: {config.ownmoviefolder}
        -T | --tvseries                                  process tv series, default: do not process tv series
        -B | --seriesbase dir       PLEX_SERIESBASE      series files directory, env/default: {config.seriesbase}
        -L | --serieslibrary name   PLEX_SERIESLIBRARY   series library name, env/default: {config.serieslibrary}
        -S | --serieessubdirs #     PLEX_SERIESSUBDIRS   levels of subdirs to retain, env/default: {config.moviessubdirs}
        -O | --ownseasonfolder      PLEX_OWNSEASONFOLDER pack each season in its own season folder, env/default: {config.ownseasonfolder}
        -d | --debug                                     turn on debug messages, default: no debug messages
        -D | --database file        PLEX_DATABASE        database file, env/default: {config.database}
    """, file=sys.stderr)
        sys.exit(2)

    config = SimpleNamespace()

    config.armed = False
    config.debug = False

    config.rmdotfiles = os.environ.get('PLEX_RMDOTFILES', "False").lower() in ("true", "1", "yes")

    config.database = os.environ.get(
        'PLEX_DATABASE', '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db')

    config.movies = False
    config.moviesbase = os.environ.get('PLEX_MOVIESBASE', '/data/plex/Filme/')
    config.movieslibrary = os.environ.get('PLEX_MOVIESLIBRARY', "Filme")
    config.moviessubdirs = abs(int(os.environ.get('PLEX_MOVIESSUBDIRS', 1)))
    config.ownmoviefolder = os.environ.get('PLEX_OWNMOVIEFOLDER', "False").lower() in ("true", "1", "yes")

    config.series = False
    config.seriesbase = os.environ.get(
        'PLEX_SERIESBASE', '/data/plex/Serien/')
    config.serieslibrary = os.environ.get('PLEX_SERIESLIBRARY', "Serien")
    config.seriessubdirs = abs(int(os.environ.get('PLEX_SERIESSUBDIRS', 1)))
    config.ownseasonfolder = os.environ.get('PLEX_OWNSEASONFOLDER', "False").lower() in ("true", "1", "yes")

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "mb:l:s:oTB:L:S:OdD:", [
                "armed",
                "rmdotfiles",
                "movies",
                "moviesbase=",
                "movieslibrary=",
                "moviessubdirs=",
                "ownmoviefolder",
                "tvseries",
                "seriesbase=",
                "serieslibrary=",
                "serieessubdirs=",
                "ownseasonfolder",
                "debug",
                "database="
            ])
    except getopt.GetoptError as err:
        usage()

    for o, a in opts:
        if o == "--armed":
            config.armed = True
        if o in ("-r", "--rmdotfiles"):
            config.rmdotfiles = True

        if o in ("-m", "--movies"):
            config.movies = True
        if o in ("-b", "--moviesbase"):
            config.moviesbase = a
        if o in ("-l", "--movieslibrary"):
            config.movieslibrary = a
        if o in ("-s", "--moviessubdirs"):
            config.moviessubdirs = abs(int(a))
        if o in ("-o", "--ownmoviefolder"):
            config.ownmoviefolder = True

        if o in ("-T", "--tvseries"):
            config.series = True
        if o in ("-B", "--seriesbase"):
            config.seriesbase = a
        if o in ("-L", "--serieslibrary"):
            config.seriesbase = a
        if o in ("-S", "--serieessubdirs"):
            config.seriessubdirs = abs(int(a))
        if o in ("-O", "--ownseasonfolder"):
            config.ownseasonfolder = True

        if o in ("-d", "--debug"):
            config.debug = True
        if o in ("-D", "--database"):
            config.database = a

    if not config.movies and not config.series:
        usage()

    return config
