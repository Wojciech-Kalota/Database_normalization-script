# Database_normalization-script
Simple "script" that for now checks if the database is in 2nf.

Input is provided either through standard input or a file:

-all the attributes separated by comma in the first line

-in the following lines provide all dependencies present in the database

Example:
```
A,B,C,D,E
A,C -> D
B   -> C
E   -> B
D   -> A
```

Will add checking for 3nf and conversion to 3nf through synthesis algorithm in the future.
