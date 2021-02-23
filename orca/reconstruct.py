from xarray import open_mfdataset, open_dataset


def reconstruct_dataset(temp_files, outfile):
    temp_paths = [temp.name for temp in temp_files]
    dataset = (
        open_mfdataset(temp_paths, combine="nested", concat_dim="time")
        if len(temp_files) > 1
        else open_dataset(temp_paths[0])
    )
    (temp.close for temp in temp_files)
    dataset.to_netcdf(outfile)

    return outfile
