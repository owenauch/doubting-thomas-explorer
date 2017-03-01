# Doubting Thomas Explorer:
# A set of scripts to explore the bible through cross references
# runstepper.py -- a runner for thomasstepper.py
#
# Author: Owen Auch
# Matthew 28:17 -- "When they saw him, they worshiped him; but some doubted."
import thomasstepper

start_verse = thomasstepper.get_start_verse()
thomasstepper.crossref_stepper(start_verse)
