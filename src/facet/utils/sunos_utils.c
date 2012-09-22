// utils.c: 
#include <Python.h>
#include <stdio.h>
#include <sys/mnttab.h>
#include <sys/param.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <string.h>
#include <strings.h>
#include <libdevinfo.h>
#include <dirent.h>
#include <sys/dkio.h>

#define DEFAULT_PARTITION_FILENAME "/etc/mnttab"

/**
 * Return information about the given physical disk
 *
 * Arguments:
 *  device path (e.g /dev/rdsk/c3t0d0s0)
 *
 * Returns:
 *  Python tuple (media type, logical block size, disk capacity) 
 */
static PyObject * get_physical_disk_info(PyObject *self, PyObject *args) {
    char *physical_disk_path = NULL;
    struct dk_minfo minfo; 
    struct dk_minfo_ext minfo_ext;
    int fd;

    // Parse Python Arguments
    if (!PyArg_ParseTuple(args, "s", &physical_disk_path))
        return NULL;

    // Open Device
    fd = open(physical_disk_path, O_RDONLY);
    if (fd < 0) 
        return PyErr_SetFromErrno(PyExc_OSError); 
    
    // Get Media Info    
    if (ioctl(fd, DKIOCGMEDIAINFO, &minfo) < 0) {
        close(fd); 
        return PyErr_SetFromErrno(PyExc_OSError); 
    }

    // Get Media Info    
    if (ioctl(fd, DKIOCGMEDIAINFOEXT, &minfo_ext) < 0) {
        close(fd); 
        return PyErr_SetFromErrno(PyExc_OSError); 
    }

    // Close disk 
    close(fd);
    
    // Return physical disk path 
    return Py_BuildValue("(iil)", minfo.dki_media_type, minfo.dki_lbsize, minfo.dki_capacity);
}

/**
 * Return the physical disk path for the given logical device using the specified driver.
 *
 * Arguments: 
 *  device name (e.g. sd0)
 *  driver name (e.g. sd)
 *
 * Returns:
 *  Python string 
 */
static PyObject * get_physical_disk_path(PyObject *self, PyObject *args) {
    char *logical_disk_name;
    char *logical_disk_driver;
    char tmp_logical_disk_name[MAXPATHLEN];
    char *device_path;
    char *device_minor;
    int device_instance;
    char tmp_path[MAXPATHLEN];
    char physical_disk_path[MAXPATHLEN];
    di_node_t root_node;
    di_node_t node;
    di_minor_t minor = DI_MINOR_NIL;

    bzero(physical_disk_path, MAXPATHLEN); 

    // Parse Python Arguments    
    if (!PyArg_ParseTuple(args, "ss", &logical_disk_name, &logical_disk_driver))
        return NULL;

    // Get Device Tree Root
    if ((root_node = di_init("/", DINFOCPYALL)) == DI_NODE_NIL) 
        return PyErr_Format(PyExc_OSError, "Unable to retreive devinfo device tree");

    // Traverse Device Tree
    node = di_drv_first_node(logical_disk_driver, root_node);
    while (node != DI_NODE_NIL) {
        if ((minor = di_minor_next(node, DI_MINOR_NIL)) != DI_MINOR_NIL) {
            device_instance = di_instance(node);
            device_path = di_devfs_path(node);
            device_minor = di_minor_name(minor);

            // Logical Device is is "<driver><instance>"
            strcpy(tmp_logical_disk_name, logical_disk_driver);
            sprintf(tmp_logical_disk_name, "%s%d", tmp_logical_disk_name, device_instance);

            if (strcmp(tmp_logical_disk_name, logical_disk_name) == 0) {

                // build a path in /devices using device path
                strcpy(tmp_path, "/devices");
                strcat(tmp_path, device_path);
                strcat(tmp_path, ":");
                strcat(tmp_path, device_minor);

                // lookup symlink in /dev/dsk for pointing to device path
                if (lookup_physical_device_symlink(tmp_path, &physical_disk_path) != 0) {
                    PyErr_SetString(PyExc_OSError, "Unable to lookup device symlink");
                }

                di_devfs_path_free(device_path);
                break;
            }

            di_devfs_path_free(device_path);
            node = di_drv_next_node(node);
        } else {
            node = di_drv_next_node(node);
        }
    }

    // Close device tree
    di_fini(root_node);
        
    // Return physical disk path 
    return Py_BuildValue("s", physical_disk_path);
}

/**
 * Returns symlink in /dev/dsk for the given physical device path
 */
int lookup_physical_device_symlink(char * physical_device_path, char * device_symlink) {
    DIR     *dirp;
    struct  dirent *dp;
    struct  stat stbuf;
    char    current_dir[MAXPATHLEN];
    char    file_name[MAXPATHLEN];
    char    temp_name[MAXPATHLEN];
    char    symlink_name[MAXPATHLEN];

    strcpy(current_dir, "/dev/dsk");

    if ((dirp = opendir(current_dir)) != NULL)
    {
        while ((dp = readdir(dirp)) != NULL)
        {
            sprintf(temp_name,"../..%s",physical_device_path);
            sprintf(symlink_name,"/dev/dsk/%s",dp->d_name);
            stat(symlink_name,&stbuf);

            if (S_ISBLK(stbuf.st_mode)) {

                readlink(symlink_name, file_name, sizeof(file_name));

                if (strcmp(file_name, temp_name) == 0) {
                    strcpy(device_symlink, symlink_name);
                    closedir(dirp);
                    return 0;
                }
            }

            bzero(file_name,MAXPATHLEN);
            bzero(temp_name,MAXPATHLEN);
            bzero(symlink_name,MAXPATHLEN);
        }
        closedir(dirp);
    }

    return 1;
}

/**
 *
 */
static PyObject * get_mounts(PyObject *self, PyObject *args) {
    char *path = NULL;
    FILE *fp = NULL; 
    struct mnttab mt;
    PyObject *partinfo;
    PyObject *parts = PyList_New(0);
 
    if (!PyArg_ParseTuple(args, "|s", &path)) 
        return NULL;
    if (!path) 
        path = DEFAULT_PARTITION_FILENAME;

    // Open Mount File 
    if ((fp = fopen(path, "r")) == NULL) 
        return PyErr_SetFromErrno(PyExc_OSError); 

    // Read Mount File
    while (getmntent(fp, &mt) == 0) {
        partinfo = Py_BuildValue("(sssss)", mt.mnt_mountp, mt.mnt_fstype, mt.mnt_mntopts, mt.mnt_special, mt.mnt_time);
        PyList_Append(parts, partinfo);
    }

    fclose(fp);
    return parts; 
}

// Module functions table
static PyMethodDef
module_functions[] = {
    { "get_physical_disk_info", get_physical_disk_info, METH_VARARGS, "Return disk info for the given physical device"},
    { "get_physical_disk_path", get_physical_disk_path, METH_VARARGS, "Return the physical device path for the given logical device using the specified driver." },
    { "get_mounts", get_mounts, METH_VARARGS, "Return a list of tuples containing info about the currently mounted filesystems." },
    { NULL }
};

// Module initialiation 
void
initsunos_utils(void)
{
    Py_InitModule3("sunos_utils", module_functions, "SunOS utils extension");
}
