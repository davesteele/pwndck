#!/bin/bash


SCRIPTDIR=$(dirname "$(realpath "$0")")
PROJDIR=$(realpath "$SCRIPTDIR/..")
LOCALEDIR=$(realpath "$PROJDIR/locales")

PROJ=$(cat "$PROJDIR/pyproject.toml" | grep ^name | head -1 | sed -E 's/^.+\"(.+)\".*/\1/')
VER=$(cat "$PROJDIR/pyproject.toml" | grep version | head -1 | sed -E 's/^.+\"(.+)\".*/\1/')

SRCDIR=$(realpath "$PROJDIR/src/$PROJ")

touch "$LOCALEDIR/$PROJ.pot"
find "$SRCDIR" -name "*.py" | xgettext -f - --no-wrap --package-name "$PROJ" --package-version "$VER" -o "$LOCALEDIR/$PROJ.pot"
