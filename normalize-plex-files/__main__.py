#!/usr/bin/env python3
import sqlite3
import os.path
import sys
from sqlsearchmovies import moviessearch
from sqlsearchseries import seriessearch
import utils
from config import getconfig

def main():

    config = getconfig()
        
    if not config.armed:
        print("Simulation only.")

    try:
        con = sqlite3.connect(config.database)
    except sqlite3.OperationalError as e:
        print(f"{e}: {config.database}")
        sys.exit(1)

    cur = con.cursor()

    if config.movies:
        if config.debug:
            print("Searching database.", file=sys.stderr)

        res = cur.execute(moviessearch, {"movies_section_name": config.movieslibrary})

        if config.debug:
            print("Parsing result.", file=sys.stderr)

        for row in res:
            title, year, edition, db_ref, width, height, files = row

            parts = utils.deserializefilenames(files)

            if config.debug:
                print(title, parts, file=sys.stderr)

            for idx, part in enumerate(parts):

                try:
                    base_dir = utils.basedir(config.moviesbase, part, config.moviessubdirs)
                except ValueError as e:
                    print(e, file=sys.stderr)
                    continue    # skip this file and continue with next

                resolution = utils.resolutionstring(height, width)

                if config.ownmoviefolder:
                    base_dir = os.path.join(base_dir, f"{title} ({year})")

                    if edition:
                        base_dir += f" {{edition-{edition}}}"

                    if db_ref:
                        base_dir += f" {{{db_ref}}}"

                    new_file = os.path.join(
                        base_dir, f"{title} ({year}){resolution}")

                    if config.armed:
                        try:
                            os.mkdir(base_dir)
                        except FileExistsError:
                            pass
                        except Exception as e:
                            print(e, file=sys.stderr)

                else:
                    if config.debug:
                        print(f"base_dir: {base_dir}", file=sys.stderr)

                    new_file = os.path.join(base_dir, f"{title} ({year})")

                    if edition:
                        new_file += f" {{edition-{edition}}}"

                    if db_ref:
                        new_file += f" {{{db_ref}}}"

                    new_file += resolution

                if len(parts) > 1:
                    # multipart
                    new_file += f" - part{idx+1}"


                # old filename without extension
                old_file = os.path.splitext(part)[0]

                utils.movemedia(old_file, new_file, config)


    if config.series:
        if config.debug:
            print("Searching database.", file=sys.stderr)

        res = cur.execute(seriessearch, {"series_section_name": config.serieslibrary})

        if config.debug:
            print("Parsing result.", file=sys.stderr)

        for row in res:
            series, year, db_ref, season, episode, title, width, height, files = row

            parts = utils.deserializefilenames(files)

            if not title:
                title = f"Folge {episode}"

            if config.debug:
                print(title, parts, file=sys.stderr)

            for idx, part in enumerate(parts):

                try:
                    base_dir = utils.basedir(config.seriesbase, part, config.seriessubdirs)
                except ValueError as e:
                    print(e, file=sys.stderr)
                    continue    # skip this file and continue with next

                resolution = utils.resolutionstring(height, width)

                base_dir = os.path.join(base_dir, f"{series} ({year})")
                if db_ref:
                    base_dir += f" {{{db_ref}}}"

                if config.ownseasonfolder:
                    base_dir = os.path.join(base_dir, f"Season {season}")

                if config.armed:
                    try:
                        os.mkdir(base_dir)
                    except FileExistsError:
                        pass
                    except Exception as e:
                        print(e, file=sys.stderr)

                new_file = os.path.join(
                    base_dir, f"{season:02}x{episode:02} {series} - {title}{resolution}")

                if len(parts) > 1:
                    # multipart
                    new_file += f" - part{idx+1}"

                # old filename without extension
                old_file = os.path.splitext(part)[0]

                utils.movemedia(old_file, new_file, config)


    con.close()

    if not config.armed:
        print("End simulation only.")


if __name__ == "__main__":
    main()
