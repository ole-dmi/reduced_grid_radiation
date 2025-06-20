import pygrib
import numpy as np
import glob
import hashlib

def md5_hash_file(file_path):
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()



def load_files(path):
    files = sorted(glob.glob(path + "GRIB*.sfx"))
    return files

ref_dir = "/scratch/dnk5089/deode/RADIATION_REF_CY49t2_AROME_nwp_DEMO_60x80_2500m_20240916/archive/2024/09/16/00/"
dev_dir = "/scratch/dnk5089/deode/RADIATION_DEV_CY49t2_AROME_nwp_DEMO_60x80_2500m_20240916/archive/2024/09/16/00/"

files_ref = load_files(ref_dir)
files_dev = load_files(dev_dir)
print(files_ref)
print(files_dev)

rel_err_sum = 0.0
# Åbn GRIB-fil
for file_ref,file_dev in zip(files_ref, files_dev):
    print(file_ref)
    print(file_dev)
    grbs_ref = pygrib.open(file_ref)
    grbs_dev = pygrib.open(file_dev)

    for grb_ref, grb_dev in zip(grbs_ref, grbs_dev):
        data_ref, lats, lons = grb_ref.data()
        data_dev, lats, lons = grb_dev.data()
        rms_ref = np.sqrt(np.mean((data_ref)**2))
        rms_dev = np.sqrt(np.mean((data_dev)**2))
        if (rms_ref>0):
            rel_err = np.sqrt(np.mean((data_ref - data_dev)**2))/rms_ref
            rel_err_sum = rel_err_sum + rel_err
            print("{:<60} {:<60} {:10.10f}  {:10.10f}  {:10.10f}".format(grb_ref.name,grb_ref.name, rms_ref, rms_dev, rel_err))
    grbs_ref.close()
    grbs_dev.close()
    
print(" ")
print("Sum of all relative errors: ",str(rel_err_sum))
print(" ")

print("Comparing md5 checksums ...")
for file_ref,file_dev in zip(files_ref, files_dev):
    
    md5_ref = md5_hash_file(file_ref)
    md5_dev = md5_hash_file(file_dev)

    print(file_ref + " " + md5_ref)
    print(file_dev + " " + md5_dev)
    
    if (md5_dev == md5_ref):
        print("md5 checksum comparison OK")
    else:
        print("md5 checksum comparison failed") 
    print(" ")

