#!/usr/bin/env bash

APP_NAME="osdag"
PREFIX="$( cd "$( dirname "$(readlink -f "$0")" )" && pwd )"

read -p "Are you sure you want to uninstall osdag? [y/N]: " confirm
[[ "$confirm" == "y" || "$confirm" == "Y" ]] || exit 0

echo "Removing osdag shortcuts..."

rm -f "$HOME/.local/share/applications/osdag.desktop" 2>/dev/null
rm -f "$HOME/Desktop/osdag.desktop"  2>/dev/null
rm -f "$HOME/.local/share/applications/Uninstall-osdag.desktop" 2>/dev/null


update-desktop-database ~/.local/share/applications 2>/dev/null || true

rm -rf "$PREFIX"

echo "osdag cleanup complete."
read -p "Press Enter to close this window..."