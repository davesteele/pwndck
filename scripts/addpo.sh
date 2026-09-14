#!/bin/bash
#
# addpo.sh
#
# Add a locale-specific po file under the locales directory.
#

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <locale>" >&2
    exit 1
fi

LANG=$1

SCRIPTDIR=$(dirname "$(realpath "$0")")
PROJDIR=$(realpath "$SCRIPTDIR/..")
LOCALEDIR=$(realpath "$PROJDIR/locales")

PROJ=$(cat "$PROJDIR/pyproject.toml" | grep ^name | head -1 | sed -E 's/^.+\"(.+)\".*/\1/')

LANGDIR="$LOCALEDIR/$LANG/LC_MESSAGES"
mkdir -p "$LANGDIR"
msginit --locale=$LANG --no-wrap --input="$LOCALEDIR/$PROJ.pot" --output="$LANGDIR/$PROJ.po"
