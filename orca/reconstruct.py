from xarray import open_mfdataset, open_dataset


def reconstruct_dataset(temp_files, outfile):
    dataset = (
        open_mfdataset(temp_files, combine="nested", concat_dim="time")
        if len(temp_files) > 1
        else open_dataset(temp_files[0])
    )
    dataset.to_netcdf(outfile)

    return outfile
