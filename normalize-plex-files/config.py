import getopt
import sys
import os
from types import SimpleNamespace
import json


def getconfig() -> SimpleNamespace:
    """Gets various config variables from the environment or from the commandline."""

    def usage(message):
        print(f"""usage: {sys.argv[0]} {{-m [-T] | -T [-m]}} [--armed] [-d] [-D database] \\
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

{message}
""", file=sys.stderr)
        sys.exit(2)

    forced_defaults = {
        "armed":    False,
        "debug":    False,
        "movies":   False,
        "series":   False,
    }

    defaults = {
        "rmdotfiles":       False,
        "database":         "/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db",

        "moviesbase":       "/data/plex/Filme/",
        "movieslibrary":    "Filme",
        "moviessubdirs":    1,
        "ownmoviefolder":   "False",

        "seriesbase":       "/data/plex/Serien/",
        "serieslibrary":    "Serien",
        "seriessubdirs":    1,
        "ownseasonfolder":  False,
    }

    try:
        cfg_file = os.path.expanduser("~/.plex")
        with open(cfg_file, "r") as f:
            config_from_file = json.load(f)
        if config_from_file.__class__ != dict:
            raise ValueError(f'Contents must be a dictionary.')
    except FileNotFoundError as e:
        config_from_file = {}
        pass
    except PermissionError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(cfg_file+" contains invalid JSON:", e, file=sys.stderr)
        sys.exit(1)

    env_keys = {
        "rmdotfiles":       'PLEX_RMDOTFILES',
        "database":         'PLEX_DATABASE',

        "moviesbase":       'PLEX_MOVIESBASE',
        "movieslibrary":    'PLEX_MOVIESLIBRARY',
        "moviessubdirs":    'PLEX_MOVIESSUBDIRS',
        "ownmoviefolder":   'PLEX_OWNMOVIEFOLDER',

        "seriesbase":       'PLEX_SERIESBASE',
        "serieslibrary":    'PLEX_SERIESLIBRARY',
        "seriessubdirs":    'PLEX_SERIESSUBDIRS',
        "ownseasonfolder":  'PLEX_OWNSEASONFOLDER',
    }

    config = SimpleNamespace(**{
        **defaults,
        **config_from_file,
        **forced_defaults,
    })

    for key, envkey in env_keys.items():
        if envkey in os.environ:
            config[key] = os.environ[envkey]

    # normalize types
    if config.rmdotfiles.__class__ != bool:
        config.rmdotfiles = str(
            config.rmdotfiles
        ).lower() in ("true", "1", "yes")
    if config.ownmoviefolder.__class__ != bool:
        config.ownmoviefolder = str(
            config.ownmoviefolder
        ).lower() in ("true", "1", "yes")
    if config.ownseasonfolder.__class__ != bool:
        config.ownseasonfolder = str(
            config.ownseasonfolder
        ).lower() in ("true", "1", "yes")
    if config.seriessubdirs.__class__ != int:
        try:
            config.seriessubdirs = abs(int(config.seriessubdirs))
        except:
            config.seriessubdirs = defaults["seriessubdirs"]

    if config.moviessubdirs.__class__ != int:
        try:
            config.moviessubdirs = abs(int(config.moviessubdirs))
        except:
            config.moviessubdirs = defaults["moviessubdirs"]

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "mb:l:s:oTB:L:S:OdD:r", [
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
        usage(str(err)+".")

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
            try:
                config.moviessubdirs = abs(int(a))
            except:
                usage(f"Argument to {o} must be of type int.")
        if o in ("-o", "--ownmoviefolder"):
            config.ownmoviefolder = True

        if o in ("-T", "--tvseries"):
            config.series = True
        if o in ("-B", "--seriesbase"):
            config.seriesbase = a
        if o in ("-L", "--serieslibrary"):
            config.seriesbase = a
        if o in ("-S", "--serieessubdirs"):
            try:
                config.seriessubdirs = abs(int(a))
            except:
                usage(f"Argument to {o} must be of type int.")
        if o in ("-O", "--ownseasonfolder"):
            config.ownseasonfolder = True

        if o in ("-d", "--debug"):
            config.debug = True
        if o in ("-D", "--database"):
            config.database = a

    if not config.movies and not config.series:
        usage("Either -m or -T must be specified.")

    return config
