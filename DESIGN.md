# Design outline

## Module overview

- **Control**
Entry point package, system management, local storage location, encryption types, etc.
- **Cloud interface**
Package containing all code necessary to upload and download files, and retrieve metadata.
- **Encryption**
Package containing all encryption related functionality.
- **Filesystem**
Package containing the FUSE filesystem interface.

## Control

Package controlling:

Functionality:

- Fuse initilizer

Settings:

- Local storage location (encrypted and decrypted folder) 

## Cloud interface

Uses PyDrive library to upload and download files, fetch metadata, and build local file tree (currently entirely in memory)

## Encryption

Encryption key is created by hashing the password.
Files are encoded using AES with CBC mode, and random IVs.
File names are created by AES encryption and b64 encoding.

## Filesystem

Uses fusepy to create FUSE. Class enables representation of remote file system locally.