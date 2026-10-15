#!/bin/bash

SCRIPTDIR=$(dirname "$(realpath "$0")")
PROJDIR=$(realpath "$SCRIPTDIR/..")
LOCALEDIR=$(realpath "$PROJDIR/locales")

PROJ=$(cat "$PROJDIR/pyproject.toml" | grep ^name | head -1 | sed -E 's/^.+\"(.+)\".*/\1/')

for PO in `ls "$LOCALEDIR"/*/LC_MESSAGES/*.po`; do
    PODIR=$(dirname "$PO")
    msgfmt "$PO" -o "$PODIR/$PROJ.mo"
done
