"""Simple FUSE filesystem that mirrors a dir but hides symlinks."""
import os
import os.path
import errno

from loopback import Loopback
import fusepy as fuse


class HideSymlinks(Loopback):
    """A loopback filesystem that overrides geattr to hide symlinks."""
    
    chroot = ""
    
    def __init__(self, root, chroot):
        self.chroot = chroot
        super(HideSymlinks, self).__init__(root)
        
    symlink = None

    def getattr(self, path, fh=None):
        if not os.path.islink(path) or os.path.realpath(path).startswith(self.chroot):
            stat = os.stat(path)
            lstat = os.lstat(path)
            keys = ('st_atime', 'st_gid', 'st_mode',
                    'st_nlink', 'st_size', 'st_uid')
            lkeys = ('st_mtime', 'st_ctime')
            result = dict((key, getattr(stat, key)) for key in keys)
            lresult = dict((key, getattr(lstat, key)) for key in lkeys)
            return {**result, **lresult}
        else:
            raise fuse.FuseOSError(errno.EACCES)
            
