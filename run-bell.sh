#!/bin/bash
cd "$(dirname "$0")"
export QT_QPA_PLATFORM=xcb
exec ./bell-env/bin/python simple_timer.py
