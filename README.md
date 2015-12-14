
# CloudDrive
## Why is CloudDrive developed?
Even new laptops have relatively small hard drives, but there is vast amounts of space available on Google Drive (in my case ~10TB). Most software used with cloud storage copies ALL files to the computer.

What I am proposing is:

 * a FUSE based file system which makes ALL files available, but only caches those files which are used
 * Encrypts all files to ensure higher levels of security of confidential files

## Current stage: *early development*
