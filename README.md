## 25w21a update
The tool just defaults to using the new clouds.png, if you'd like to use clouds_old.png you can just rename the files for now (or edit cf.py's line 99).

## General info
This prints all matching patterns for all 4 different orientations, it wraps the cloud grid around corners, lets you choose whether to search the pattern from the bottom or from the top, supports both fast and fancy clouds and given a block range automatically generates all the possible z coordinates within it.

## Running the code
It's Python, so you download Python, open the cmd prompt, execute cd to the dir with the file like `cd 'C:\Users\YourName\Documents'` or something and then `python cf.py`.

pattern.txt is the pattern, 1 means cloud, 0 means no cloud, you can also write a question mark to express you don't know for sure whether a zone is 1 or 0, this is particularly useful to space out the pattern since it needs to be a rectangle (all rows must have the same number of columns and all columns the same number of rows).

Like:
```
11????
?1??00
```

You should also open cf.py with a text editor and modify it if you need to.

There's an option to find clouds from the bottom or from the top, one for fast clouds and a couple others.
