// utils.c: 
#include <Python.h>
#include <stdio.h>
#include <sys/mnttab.h>
//#include <sys/types.h>
//#include <sys/dkio.h>
#include <sys/param.h>
#include <sys/stat.h>
#include <string.h>
#include <strings.h>
//#include <unistd.h>
//#include <stdlib.h>
//#include <ctype.h>
//#include <fcntl.h>
//#include <sys/fcntl.h>
#include <libdevinfo.h>
#include <dirent.h>


#define DEFAULT_PARTITION_FILENAME "/etc/mnttab"

/*
 * Return the physical device path for the given logical device using the specified driver.
 *
 * Arguments: 
 *  - device name (e.g. sd0)
 *  - driver name (e.g. sd) 
 */
static PyObject * get_physical_device_path(PyObject *self, PyObject *args) {
    char *logical_device_name;
    char *logical_device_driver;
    char tmp_logical_device_name[MAXPATHLEN]; 
    char *physical_device_path;
    char *physical_device_minor_name;
    char *physical_device_name;
    int physical_device_instance;
    char tmp_path[MAXPATHLEN];
    char device_symlink[MAXPATHLEN];
    di_node_t root_node;
    di_node_t node;
    di_minor_t minor = DI_MINOR_NIL;

    bzero(device_symlink, MAXPATHLEN); 

    // Parse Python Arguments    
    if (!PyArg_ParseTuple(args, "ss", &logical_device_name, &logical_device_driver)) 
        return NULL;

    // Get Device Tree Root
    if ((root_node = di_init("/", DINFOCPYALL)) == DI_NODE_NIL) {
        PyErr_SetString(PyExc_OSError, "Unable to retreive devinfo device tree");
        return NULL;
    }

    // Traverse Device Tree
    node = di_drv_first_node(logical_device_driver, root_node);
    while (node != DI_NODE_NIL) {
        if ((minor = di_minor_next(node, DI_MINOR_NIL)) != DI_MINOR_NIL) {
            physical_device_instance = di_instance(node);
            physical_device_path = di_devfs_path(node);
            physical_device_minor_name = di_minor_name(minor);

            // Logical Device is is "<driver><instance>"
            strcpy(tmp_logical_device_name, logical_device_driver);
            sprintf(tmp_logical_device_name, "%s%d", tmp_logical_device_name, physical_device_instance);

            if (strcmp(tmp_logical_device_name, logical_device_name) == 0) {
                //printf("found logical device: %s path: %s\n", tmp_logical_device_name, physical_device_path);

                strcpy(tmp_path, "/devices");
                strcat(tmp_path, physical_device_path);
                strcat(tmp_path, ":");
                strcat(tmp_path, physical_device_minor_name);

                // lookup symlink in /dev/dsk for physical device path
                if (lookup_physical_device_symlink(tmp_path, &device_symlink) != 0) {
                    PyErr_SetString(PyExc_OSError, "Unable to lookup device symlink");
                }

                di_devfs_path_free(physical_device_path);
                break;
            }

            di_devfs_path_free(physical_device_path);
            node = di_drv_next_node(node);
        } else {
            node = di_drv_next_node(node);
        }
    }

    // Close device tree
    di_fini(root_node);
        
    // return symlink location 
    return Py_BuildValue("s", device_symlink);
}

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

/*
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
    fp = fopen(path, "r");
    if (!fp) 
        return NULL;

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
    { "get_physical_device_path", get_physical_device_path, METH_VARARGS, "Return the physical device path for the given logical device using the specified driver." },
    { "get_mounts", get_mounts, METH_VARARGS, "Return a list of tuples containing info about the currently mounted filesystems." },
    { NULL }
};

// Module initialiation 
void
initsunos_utils(void)
{
    Py_InitModule3("sunos_utils", module_functions, "SunOS utils extension");
}
