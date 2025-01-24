# Hashmeister

A tool for comparing two large folders. The tool takes each subdirectory of the given folder, and keeps track of a hash of its direct subdirectories and the (contents/sizes of) the files it contains.

## Usage
Firstly, use the `hash` command to create `.hm` files for the folders you would like to compare:

`python hashmeister.py hash -d [Directory] -o [Output file] (-t)`  

This command hashes the given directory into the output file. Hashes files according to their size by default. Use the `-t` (--thorough) flag for byte-level file comparison.

Next, use the `compare` command to compare the `.hm` files you generated:

`python hashmeister.py compare [First file] [Second file]`

This command compares the Hashmeister-generated files, and prints the differences it finds.
