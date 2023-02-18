# Normalize-Plex-Files <!-- omit in toc -->

- [1. Rationale](#1-rationale)
- [2. Installation](#2-installation)
  - [2.1. Linux/UNIX](#21-linuxunix)
  - [2.2. Windows](#22-windows)
- [3. Typical Usage (Quickstart)](#3-typical-usage-quickstart)
  - [3.1. Define Your Local Plex Setup](#31-define-your-local-plex-setup)
  - [3.2. Preflight Checks](#32-preflight-checks)
  - [3.3. Reorganize Your Files](#33-reorganize-your-files)
- [4. Variants](#4-variants)
  - [4.1. Retain Levels of Subdirectories](#41-retain-levels-of-subdirectories)
  - [4.2. Store Each Movie in its own Subdirectory](#42-store-each-movie-in-its-own-subdirectory)
  - [4.3. Store Each Season of a TV Show in its own Subdirectory](#43-store-each-season-of-a-tv-show-in-its-own-subdirectory)
- [5. Config File](#5-config-file)
- [6. All Commandline-Options](#6-all-commandline-options)
- [7. Debugging](#7-debugging)
  - [7.1. Python Debugging in VS Code](#71-python-debugging-in-vs-code)
  - [7.2. SQLite3 Debugging](#72-sqlite3-debugging)
    - [7.2.1. SQLite3 Command Line](#721-sqlite3-command-line)
    - [7.2.2. VS Code Formatter: Prettier-SQL](#722-vs-code-formatter-prettier-sql)
    - [7.2.3. VS Code SQL Execution: SQLite](#723-vs-code-sql-execution-sqlite)


# 1. Rationale
This is a tiny python application that normalizes the filenames in your [Plex](https://app.plex.tv) media library after [Plex](https://app.plex.tv) has scraped your files and downloaded corresponding metadata, and after you manually corrected some possibly midguides matches in [Plex](https://app.plex.tv).

The idea is that - **after [Plex](https://app.plex.tv) has matched your files** - this application renames the files coherently with the data [Plex](https://app.plex.tv) has found in [IMDB](https://www.imdb.com/), [TMDB](https://www.themoviedb.org/), or [TVDB](https://thetvdb.com/) databases. This has two advantages:
- aesthetics: uniform filenames within your library
- pragmatism: if you ever have to rebuild your library, all movies will be matched as they were before.

# 2. Installation
## 2.1. Linux/UNIX
- Make sure you have `python3` installed and it's in your path.
- Go to [Releases](https://github.com/jkeltsc/normalize-plex-files/releases), open the assets, download `normalize-plex-files`.
- Make `normalize-plex-files` executable:
  ```Shell
  chmod a+rx normalize-plex-files
  ```  
- Run the application:
  ```Shell
  ./normalize-plex-files
  ```  
- The application will display its help text.

## 2.2. Windows
The package has not been tested on Windows. Chances are good it works, though. To try your luck,
- Make sure you have `python3` installed and it's in your path.
- Go to [Releases](./releases), open the assets, download `normalize-plex-files.zip`.
- Run the application:
  ```Shell
  python3 normalize-plex-files.zip
  ```  
- The application will display its help text.

# 3. Typical Usage (Quickstart)

## 3.1. Define Your Local Plex Setup
Describe your Plex setup in environment variables. Set them as described in the table below:

| Variable           | Meaning                               | Default              |
| ------------------ | ------------------------------------- | -------------------- |
| PLEX_MOVIESBASE    | Base directory for your movie files   | `/data/plex/Filme/`  |
| PLEX_MOVIESLIBRARY | Name of your movies library           | Filme                |
| PLEX_SERIEESSBASE  | Base directory for your TV show files | `/data/plex/Serien/` |
| PLEX_SERIESLIBRARY | Name of your TV shows library         | Serien               |

(New to environment variables? Read this: [Linux](https://unix.stackexchange.com/questions/117467/how-to-permanently-set-environmental-variables), [Windows](https://stackoverflow.com/questions/5898131/set-a-persistent-environment-variable-from-cmd-exe)):


## 3.2. Preflight Checks
Before you actually rename all your files and move them in place, you should check how `normalize-plex-files` intents to shuffle around your media files.
- To display what `normalize-plex-files` would do to your movies library, run
  ```Shell
  normalize-plex-files -m
  ```
- To display what `normalize-plex-files` would do to your TV shows library, run
  ```Shell
  normalize-plex-files -T
  ```

## 3.3. Reorganize Your Files
Check these conditions:
- You are fine with the modifications `normalize-plex-files` would apply (see Preflight Checks in the previous section).
- You are not running `normalize-plex-files` as a scheduled job (cron job), because then you would skip the pre-flight check (see previous section).
- You have a current backup of all your files with your current naming scheme available.

If all three are true, you may run `normalize-plex-files` in `--armed` mode to reorganize you media files:
- To reorganize your movie files, run
  ```Shell
  normalize-plex-files -m --armed
  ```
- To reorganize your TV show files, run
  ```Shell
  normalize-plex-files -T --armed
  ```
- To reorganize both, your TV show files and your movie files, run
  ```Shell
  normalize-plex-files -Tm --armed
  ```

# 4. Variants

## 4.1. Retain Levels of Subdirectories
The application can retain a number of subdirectory levels. The default is to guard one level.
The intention is to leave manual sorting criteria untouched that you applied to your paths.
This behaviour can be adjusted using variables or command line options: 

| Variable           | Long Option      | Short | Meaning                                                      | Default |
| ------------------ | ---------------- | ----- | ------------------------------------------------------------ | ------- |
| PLEX_MOVIESSUBDIRS | --moviessubdirs  | -s    | Number of subdirs to leave untouched for movie libraries     | `1`     |
| PLEX_SERIESSUBDIRS | --serieessubdirs | -S    | Number of subdirs to leave untouched for TV series libraries | `1`     |


Assume your movie library is at
- `PLEX_MOVIESBASE=/data/plex/movies`

and you distinguish between
- Donald's movies in `/data/plex/movies/donald` and
- Mickey's movies in `/data/plex/movies/mickey`,

then the default of retaining one subdirectory level will perfectly match your needs. `normalize-plex-files` will name your files similar to this:

```
/data/plex/movies/
                  mickey/
                         Casino Royale (1967) {tmdb-12208} [720x336].m4v
                         Chasing Amy (1997) {tmdb-2255} [704x384].de.srt'
                         Chasing Amy (1997) {tmdb-2255} [704x384].m4v'
                         James Bond 007 - Casino Royale (2006) {tmdb-36557} [1280x528].m4v
                  donald/
                         23 (1999) {tmdb-1557} [720x592].m4v
                         Cowboys & Aliens (2011) {tmdb-49849} [1920x800].m4v
                         Happy Hour (2015) {tmdb-354759} [1280x720] - part1.m4v
                         Happy Hour (2015) {tmdb-354759} [1280x720] - part2.m4v
                         Happy Hour (2015) {tmdb-354759} [1280x720] - part3.m4v
```

Using `--moviessubdirs 0` would condense your media files into one directory, as shown below:
```
/data/plex/movies/
                  23 (1999) {tmdb-1557} [720x592].m4v
                  Casino Royale (1967) {tmdb-12208} [720x336].m4v
                  Chasing Amy (1997) {tmdb-2255} [704x384].de.srt'
                  Chasing Amy (1997) {tmdb-2255} [704x384].m4v'
                  Cowboys & Aliens (2011) {tmdb-49849} [1920x800].m4v
                  Happy Hour (2015) {tmdb-354759} [1280x720] - part1.m4v
                  Happy Hour (2015) {tmdb-354759} [1280x720] - part2.m4v
                  Happy Hour (2015) {tmdb-354759} [1280x720] - part3.m4v
                  James Bond 007 - Casino Royale (2006) {tmdb-36557} [1280x528].m4v
```

## 4.2. Store Each Movie in its own Subdirectory
The application can create indiviual subdirectories per movie. The default is to not create individual directories per movie.

The intention of this option is to group together multiple media files belonging to the same movie. This makes sense if you have multipart movie files or external subtitles. 

This behaviour can be adjusted using variables or command line options: 

| Variable            | Long Option      | Short | Meaning                                                                                | Default |
| ------------------- | ---------------- | ----- | -------------------------------------------------------------------------------------- | ------- |
| PLEX_OWNMOVIEFOLDER | --ownmoviefolder | -o    | If the option is present or the variable set to `True`, individual folders are created | `False` |


The effect of this option is as follows:

```
/data/plex/movies/
                  mickey/
                         Casino Royale (1967) {tmdb-12208}/
                                               Casino Royale (1967) [720x336].m4v
                         Chasing Amy (1997) {tmdb-2255}/
                                               Chasing Amy (1997) [704x384].de.srt
                                               Chasing Amy (1997) [704x384].m4v
                         James Bond 007 - Casino Royale (2006) {tmdb-36557}/
                                               James Bond 007 - Casino Royale (2006) [1280x528].m4v
                  donald/
                         23 (1999) {tmdb-1557}/
                                               23 (1999) [720x592].m4v
                         Cowboys & Aliens (2011) {tmdb-49849}/
                                               Cowboys & Aliens (2011) [1920x800].m4v
                         Happy Hour (2015) {tmdb-354759}/
                                               Happy Hour (2015) [1280x720] - part1.m4v
                                               Happy Hour (2015) [1280x720] - part2.m4v
                                               Happy Hour (2015) [1280x720] - part3.m4v
```

## 4.3. Store Each Season of a TV Show in its own Subdirectory

The application can create indiviual subdirectories per season of a TV show. The default is to not create individual directories per season.

This behaviour can be adjusted using variables or command line options: 

| Variable             | Long Option       | Short | Meaning                                                                                | Default |
| -------------------- | ----------------- | ----- | -------------------------------------------------------------------------------------- | ------- |
| PLEX_OWNSEASONFOLDER | --ownseasonfolder | -O    | If the option is present or the variable set to `True`, individual folders are created | `False` |

Example with `PLEX_SERIEESSBASE=/data/plex/tv-shows/` and `PLEX_OWNSEASONFOLDER=False`:
```
/data/plex/tv-shows/
                    donald/
                           Doctor Who (2005) {tvdb-78804}/
                                               01x01 Doctor Who - Rose [1920x1080].m4v
                                               01x02 Doctor Who - Das Ende der Welt [1920x1080].m4v
                                               [...]
                                               01x13 Doctor Who - Getrennte Wege (2) [1920x1080]
                                               01x14 Doctor Who - Die Weihnachtsinvasion [1920x1080].m4v
                                               02x01 Doctor Who - Die neue Erde [1920x1080].m4v
                                               02x02 Doctor Who - Mit Zähnen und Klauen [1920x1080].m4v
                                               [...]
```

Example with `PLEX_SERIEESSBASE=/data/plex/tv-shows/` and `PLEX_OWNSEASONFOLDER=True`:
```
/data/plex/tv-shows/
                    donald/
                           Doctor Who (2005) {tvdb-78804}/
                                               Season 1/
                                                        01x01 Doctor Who - Rose [1920x1080].m4v
                                                        01x02 Doctor Who - Das Ende der Welt [1920x1080].m4v
                                                        [...]
                                                        01x13 Doctor Who - Getrennte Wege (2) [1920x1080]
                                                        01x14 Doctor Who - Die Weihnachtsinvasion [1920x1080].m4v
                                               Season 2/
                                                        02x01 Doctor Who - Die neue Erde [1920x1080].m4v
                                                        02x02 Doctor Who - Mit Zähnen und Klauen [1920x1080].m4v
                                                        [...]
```

# 5. Config File

`normalize-plex-files` supports rudimentary config-file support.
If `~/.plex` exists, it will be read onstartup and the content interpreted as a JSON object.

If it is not a JSON object, an error is thrown. Unkown attributes are ignored.
Known attributes are listed in the table in the next section.

Example `~/.plex` file:
```JSON
{
  "rmdotfiles":       true
}
```
Defaults:
```JSON
{
  "rmdotfiles":       false,
  "database":         "/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db",
  "moviesbase":       "/data/plex/Filme/",
  "movieslibrary":    "Filme",
  "moviessubdirs":    1,
  "ownmoviefolder":   false,
  "seriesbase":       "/data/plex/Serien",
  "serieslibrary":    "Serien",
  "seriessubdirs":    1,
  "ownseasonfolder":  false
}
```

# 6. All Commandline-Options
| Category  | Long&nbsp;Option&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Short | Environment Variable   | Cfg-File Attribute | Meaning&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Default                                                                                                                           |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------- | ----- | ---------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| general   | `--armed`                                                                                                                          |       |                        |                    | run armed, do actually move files                                                                                                                                                                                                                                                                                                                                                                                                     | run unarmed (simulation only)                                                                                                     |
| general   | `--rmdotfiles`                                                                                                                     | `-r`  | `PLEX_RMDOTFILES`      | `rmdotfiles`       | allow removal of dotfiles in directories prior to directory removal                                                                                                                                                                                                                                                                                                                                                                   | do not allow removal of dotfiles                                                                                                  |
| general   | `--debug`                                                                                                                          | `-d`  |                        |                    | print debug messages                                                                                                                                                                                                                                                                                                                                                                                                                  | do not print debug messages                                                                                                       |
| general   | `--database`                                                                                                                       | `-D`  | `PLEX_DATABASE`        | `database`         | Path to Plex' SQLite3 database file                                                                                                                                                                                                                                                                                                                                                                                                   | `/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db` |
| movies    | `--movies`                                                                                                                         | `-m`  |                        |                    | process movie library                                                                                                                                                                                                                                                                                                                                                                                                                 | don't process movie library                                                                                                       |
| movies    | `--moviesbase`                                                                                                                     | `-b`  | `PLEX_MOVIESBASE`      | `moviesbase`       | movie files directory                                                                                                                                                                                                                                                                                                                                                                                                                 | `/data/plex/Filme/`                                                                                                               |
| movies    | `--movieslibrary`                                                                                                                  | `-l`  | `PLEX_MOVIESLIBRARY`   | `movieslibrary`    | movies library name                                                                                                                                                                                                                                                                                                                                                                                                                   | `Filme`                                                                                                                           |
| movies    | `--moviessubdirs`                                                                                                                  | `-s`  | `PLEX_MOVIESSUBDIRS`   | `moviessubdirs`    | levels of subdirs to retain                                                                                                                                                                                                                                                                                                                                                                                                           | `1`                                                                                                                               |
| movies    | `--ownmoviefolder`                                                                                                                 | `-o`  | `PLEX_OWNMOVIEFOLDER`  | `ownmoviefolder`   | pack each movie in its own movie folder                                                                                                                                                                                                                                                                                                                                                                                               | `False`                                                                                                                           |
| tv-series | `--tvseries`                                                                                                                       | `-T`  |                        |                    | process tv series library                                                                                                                                                                                                                                                                                                                                                                                                             | don't process tv series library                                                                                                   |
| tv-series | `--seriesbase`                                                                                                                     | `-B`  | `PLEX_SERIESBASE`      | `seriesbase`       | tv series  directory                                                                                                                                                                                                                                                                                                                                                                                                                  | `/data/plex/Serien/`                                                                                                              |
| tv-series | `--serieslibrary`                                                                                                                  | `-L`  | `PLEX_SERIESLIBRARY`   | `serieslibrary`    | tv series library name                                                                                                                                                                                                                                                                                                                                                                                                                | `Serien`                                                                                                                          |
| tv-series | `--serieessubdirs`                                                                                                                 | `-S`  | `PLEX_SERIESSUBDIRS`   | `seriessubdirs`    | levels of subdirs to retain                                                                                                                                                                                                                                                                                                                                                                                                           | `1`                                                                                                                               |
| tv-series | `--ownseasonfolder`                                                                                                                | `-O`  | `PLEX_OWNSEASONFOLDER` | `ownseasonfolder`  | pack each season in its own season folder                                                                                                                                                                                                                                                                                                                                                                                             | `False`                                                                                                                           |

# 7. Debugging

## 7.1. Python Debugging in VS Code
In case you use VS Code: to start the application in the VS Code python debugger, copy `.vscode/launch.json.example` to `.vscode/launch.json` and adjust to your needs.

## 7.2. SQLite3 Debugging

The files [normalize-plex-files/sqlsearchmovies.py](./normalize-plex-files/sqlsearchmovies.py) and [normalize-plex-files/sqlsearchseries.py](./normalize-plex-files/sqlsearchseries.py) are formatted so that they are valid SQLite3 code, though at the same time being  valid python code.

This means while the files can be normally imported into the python application, they can also be normally used with SQLite3 tooling.

### 7.2.1. SQLite3 Command Line

You can directlty process the files using the SQLite3 commandline tool.

Be sure to replace the database path, movie section name and series section name with your values.

```
% sqlite3 '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db'
SQLite version 3.39.5 2022-10-14 20:58:05
Enter ".help" for usage hints.
sqlite> .parameter set :movies_section_name "'Filme'"
sqlite> .read normalize-plex-files/sqlsearchmovies.py
```

```
% sqlite3 '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db'
SQLite version 3.39.5 2022-10-14 20:58:05
Enter ".help" for usage hints.
sqlite> .parameter set :series_section_name "'Serien'"
sqlite> .read normalize-plex-files/sqlsearchseries.py
```

### 7.2.2. VS Code Formatter: Prettier-SQL
[Prettier-SQL](https://marketplace.visualstudio.com/items?itemName=inferrinizzard.prettier-sql-vscode) can handle the file as SQL. However, you need to manually switch the language in VS Code to SQLite, as the automatic language detecton will recognize the file as python.

### 7.2.3. VS Code SQL Execution: SQLite
[VS Code SQLite](https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite) can execute the files within VS Code.
However, you need to define `:movies_section_name` and `:series_section_name` named parameters, as in the SQLite Command Line example above.
To do so, copy the `.vscode/setting.json.example` to `.vscode/setting.json` and adjust accordingly. Additionally, you need to manually switch the language in VS Code to SQLite, as the automatic language detecton will recognize the file as python.
