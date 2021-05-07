# aortacomp

What?

This program works with the Leaderboards.txt from Art of Rally. It reports times that are slower than a corresponding time (same stage, direction and grip level) for a slower group. Group A is considered fastest, and group 2 is considered slowest. 

Cars aren't compared, but their numbers are displayed nevertheless. They are counting from the default onward, with 2 being the one you get after changing the car one step in the game menu.

How?

You need either python 2.7 or python 3. You need to either give the location of Leaderboards.txt on the command line, or change the directory first and give no argument:
python aortacomp.py ~/.config/unity3d/Funselektor\ Labs/art\ of\ rally/Save

python aortacomp.py AppData\LocalLow\Funselektor Labs\art of rally\Save

python aortacomp.py ~/Library/Application Support/Funselektor Labs/art of rally/Save

If you get a long list, you can redirect it to a text file.
python aortacomp.py > raceherenext.txt
