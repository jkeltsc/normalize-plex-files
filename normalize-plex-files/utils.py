import glob
import os
import sys
from pathlib import Path
from types import SimpleNamespace


def resolutionstring(height: int, width: int) -> str:
    """returns a string of the form " [{width}x{height}]".
    The space at the beginning is intentional, so the string can easily be
    appended to filenames.
    If width is not available, returns " [{height}]" instead.
    If also height is not available, returns an empty string."""
    if height:
        if width:
            return f" [{width}x{height}]"
        else:
            return f" [{height}]"
    else:
        return ""


def deserializefilenames(serializedfilenames: str) -> list[str]:
    r"""deserializes and unescapes filename lists previously serialised in the
    SQL query:
    - unescapes filenames:
      "file\|name1" will become ["file|name1"],
    - deserializes lists:
      "file\|name1||file\|\|name2" will become ["file|name1","file||name2"]."""
    # split files at filename separator || (inserted above in SQL code)
    # and unescape all occurances of \| in filenames to | (escaped above)

    files = [f.replace(r'\|', '|') for f in serializedfilenames.split('||')]
    files.sort()  # sort it - SQlite adds it in arbitrary order

    return files


def basedir(configuredbase: str, currentfile: str, depth: int = 1) -> str:
    """ensures that path of {currentfile} is below path {configuredbase},
    adds {depth} path elements from {currentfile} to {configuredbase}
    and returns that to be used as the base path for the movie/series."""
    base_dir = os.path.commonpath([configuredbase, currentfile])

    if base_dir != os.path.normpath(configuredbase):
        raise ValueError(f'media file outside of configured base dir, file: {currentfile}, configured base dir: {configuredbase}')

    # get subdir(s) up to depth {depth} below configuredbase
    relpath = os.path.relpath(os.path.dirname(currentfile), start=base_dir)
    subdirs = Path(relpath).parts[0:depth]
    
    return(os.path.join(base_dir, *subdirs))



def movemedia(old_file:str, new_file:str, config:SimpleNamespace) -> None:
    """Moves all files with basename {old_file} and arbitrary extensions
    to {new_file} retaining the extensions when {config.armed} is true.
    {old_file} must not contain an filename-extension.
    Does not overwrite existing files. Removes the old directory if empty after
    operation.
    Forcefully removes dot-files from the old directory to allow for directory
    removal if {config.rmdotfiles} is true."""
    # old_file and new_file are basenames without file extensions.
    # The move concerns all files with these basenames, regardless of extension.

    # check if file should be actually moved
    if old_file != new_file:
        # yes!
        if not config.armed:
            print(f"would move: {old_file} --> {new_file}")
        else:
            # seek all extensions of old_file (e.g. .m4v, .srt, ...)
            for file in glob.glob(glob.escape(old_file)+'.*'):
                ext = file.replace(old_file, "")
                try:
                    # move without overwriting
                    os.link(file, new_file+ext)
                except Exception as e:
                    print(e, file=sys.stderr)
                else:
                    # link worked, now unlink old instance
                    try:
                        os.unlink(file)
                    except Exception as e:
                        print(e, file=sys.stderr)
                    else:
                        # try to remove old dir
                        # (will fail, if this is not the last movie file)
                        # prereq: remove dot files in dir, if config.rmdotfiles
                        old_base_dir = os.path.dirname(old_file)
                        if config.rmdotfiles:
                            dotfiles = glob.glob(os.path.join(
                                glob.escape(old_base_dir), '.??*'))
                            for dotfile in dotfiles:
                                print(f"removing {dotfile}")
                                try:
                                    os.unlink(dotfile)
                                except Exception as e:
                                    print(e, file=sys.stderr)
                        # actual rmdir:
                        # ignore if not empty (this only indicates that this file
                        # was not the last movie file. Removal will be successful
                        # after last movie file has been removed.^
                        try:
                            os.rmdir(old_base_dir)
                        except OSError:
                            pass  # not empty (expected)
                        except Exception as e:
                            print(e, file=sys.stderr)  # real error
                        else:
                            print(f"removed {old_base_dir}")
