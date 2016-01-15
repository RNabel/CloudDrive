# CloudDrive Documentation

## Path resolution
Google Drive uses tagging for paths.
2 options available to use encode paths in CloudDrive:
1. Encode entire path
2. Break up path into folders, create these remotely and encode each name.

Considerations for options 1:

- Very fast to encode and upload file name
- Less logic required as folders are only relevant on client-side's FUSE code
- Downloading of all meta-data required to list all contents of every folder

Considerations for option 2:

- More logic required to upload files, as has to be able to create new folders etc.
- Closer to actual representation and thus querying meta-data of individual folders easier
- Allows for pagination, meaning less of the file-structure has to be held in memory

### Path storage

Options for storage:

1. SQL-type database
0. DBFS - Database File System, [sourceforge](http://dbfs.sourceforge.net/), [python interface on GitHub](https://github.com/mitjat/dbfs)
0. Other database format


## File eviction policies

 - LRU cache to evict files:
   - [python lib](https://pypi.python.org/pypi/pylru)
   - [functools](https://docs.python.org/3/library/functools.html#functools.lru_cache)
 - General python cache library:
   - [HermesCache](https://pypi.python.org/pypi/HermesCache)