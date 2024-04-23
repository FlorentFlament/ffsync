#!/usr/bin/env python3
import os
import shutil
import click
import yaml

def cleaned_name(fname):
    return ''.join(c if c.isalnum() or c=='.' else '_' for c in fname)

def process_yaml(filename):
    with open(filename) as fd:
        data = yaml.full_load(fd)

        rv = []
        for title, roms_d in data.items():
            c_title = cleaned_name(title)
            if len(roms_d) > 1:
                for disk_i, (usbkey_i, fname) in enumerate(roms_d.items(), 1):
                    rv.append({
                        "file_name": f"DSKA{usbkey_i:04d}_{c_title}_{disk_i}.st",
                        "rom_name": fname,
                    })
            elif len(roms_d) == 1:
                usbkey_i, fname = list(roms_d.items())[0]
                rv.append({
                    "file_name": f"DSKA{usbkey_i:04d}_{c_title}.st",
                    "rom_name": fname,
                })
            # Don't do anything if no roms specified for the title
        return rv

def find_roms(data, roms_path):
    """data is a list of dictionaries containing a rom_name field.
    The function will add a rom_path field.

    """
    # First index our structure by rom_name
    data_h = {rom_data["rom_name"]: rom_data for rom_data in data}

    for dirpath, dirnames, filenames in os.walk(roms_path):
        for f in filenames:
            if f in data_h.keys():
                data_h[f]["rom_path"] = os.path.join(dirpath, f)
    return data

def copy_roms(data, dest_dir):
    dir_files = os.listdir(dest_dir)

    for e in data:
        source = e["rom_path"]
        fname = e["file_name"]
        dest = os.path.join(dest_dir, fname)
        prefix = e["file_name"].split("_")[0]

        if (os.path.exists(dest)):
            print(f"{fname} [skipping] Already there")
            continue

        for f in dir_files:
            if f.startswith(prefix):
                print(f"{f} [removing] Matching prefix")
                os.remove(os.path.join(dest_dir, f))

        print(f"{e['file_name']} <- {source}")
        shutil.copy(source, dest)
        os.chmod(dest, 0o444)

def process_prune(data, dest_dir):
    target_files = os.listdir(dest_dir)
    specif_files = set([e["file_name"] for e in data])
    for tf in target_files:
        if tf.startswith("DSKA") and tf not in specif_files:
            print(f"{tf} [pruning]")
            os.remove(os.path.join(dest_dir, tf))

@click.command()
@click.option("--config-file", required=True,
              help="The YAML configuration file specifying the roms to synchronize.")
@click.option("--roms-path", required=False,
              help="The path to the TOSEC directory where the roms are to be copied from. Defaults to \".\".")
@click.option("--dest-dir", required=True,
              help="The target directory; typically a mounted USB key to be inserted into a Gotek drive flashed with flashfloppy.")
@click.option("--prune", required=False,
              help="Remove DSKA* files not specified in the configuration file. Defaults to False.")
def main(config_file, roms_path, dest_dir, prune):
    """Copy roms to dest_dir according to specifications provided in
    the configuration file.

    """
    print(f"""Using parameters:
config-file: {config_file}
roms-path: {roms_path}
dest-dir: {dest_dir}
""")
    data = process_yaml(config_file)
    search_paths = ["."]
    if roms_path:
        search_paths.append(roms_path)
    for path in search_paths:
        find_roms(data, path)
    copy_roms(data, dest_dir)
    if prune: process_prune(data, dest_dir)

if __name__ == "__main__":
    main(auto_envvar_prefix='TOSYNC')
