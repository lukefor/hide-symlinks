hide-symlinks
=============

A simple FUSE filesystem that makes symlinks look like actual files.

This fork changes:
- ctime/mtime taken from symlink rather than file pointed to (unique behaviour needed for my use case)
- Chroot-like protection to ensure symlink points within a given path, otherwise there is nothing stopping you symlinking to anywhere
- Imports changed for Debian (fuse->fusepy)

Compile
-------

You can compile the package into an executabe by running *make*. The output is
titled 'hide-symlinks'. The idea is based on [this blog
post](http://blog.ablepear.com/2012/10/bundling-python-files-into-stand-alone.html
"Bundling Python Files").

Run
---

You can run it by calling the executable like so: `./hide-symlinks <root>
<mount-point> <chroot>`, where `<root>` is the directory to be mirrored or looped, and
`<mount-point>` is the (empty) directory to mount the new fuse filesystem, and
`<chroot>` is the parent 'chroot' directory that symlinks are allowed to point
to. It does not have to be within the other two directories.


How It Works
------------

The filesystem relies on [fusepy](https://github.com/terencehonles/fusepy), and
uses the Loopback example included with fusepy as a base class. It simply
changes the getattr operation to use the os.stat call instead of the os.lstat
call, effectively hiding symlinks. I also removed the symlink operation (which
seems to have issues, though it does work). Otherwise, all operations work as
normal for a loopback filesystem (e.g. writes and reads defer to the `<root>`
directory).
