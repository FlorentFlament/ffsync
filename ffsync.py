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

def find_roms(data, roms_dir):
    """data is a list of dictionaries containing a rom_name field.
    The function will add a rom_path field.

    """
    # First index our structure by rom_name
    data_h = {rom_data["rom_name"]: rom_data for rom_data in data}

    for dirpath, dirnames, filenames in os.walk(roms_dir, followlinks=True):
        for f in filenames:
            if f in data_h.keys():
                data_h[f]["rom_path"] = os.path.join(dirpath, f)
    return data

def copy_roms(data, target_dir):
    dir_files = os.listdir(target_dir)

    for e in data:
        source = e["rom_path"]
        fname = e["file_name"]
        target = os.path.join(target_dir, fname)
        prefix = e["file_name"].split("_")[0]

        if (os.path.exists(target)):
            print(f"{fname} [skipping] Already there")
            continue

        for f in dir_files:
            if f.startswith(prefix):
                print(f"{f} [removing] Matching prefix")
                os.remove(os.path.join(target_dir, f))

        print(f"{e['file_name']} <- {source}")
        shutil.copy(source, target)
        os.chmod(target, 0o444) # Set files in read-only mode

def process_prune(data, target_dir):
    target_files = os.listdir(target_dir)
    specif_files = set([e["file_name"] for e in data])
    for tf in target_files:
        if tf.startswith("DSKA") and tf not in specif_files:
            print(f"{tf} [pruning]")
            os.remove(os.path.join(target_dir, tf))

def check_rom_paths(data):
    return [e["rom_name"] for e in data if "rom_path" not in e]

@click.command()
@click.option("--config-file", default="./ffsync.yaml",
              help="The YAML configuration file specifying the roms to synchronize.")
@click.option("--roms-dir", default=".",
              help="The path to the TOSEC directory where the roms are to be copied from. Defaults to \".\".")
@click.option("--target-dir", required=True,
              help="The target directory; typically a mounted USB key to be inserted into a Gotek drive flashed with flashfloppy.")
@click.option("--prune/--no-prune",
              help="Remove DSKA* files not specified in the configuration file. Defaults to False.")
def main(config_file, roms_dir, target_dir, prune):
    """Copy roms to the target directory in accordance with the
    configuration file.

    """
    print(f"""Using parameters:
config-file: {config_file}
roms-dir: {roms_dir}
target-dir: {target_dir}
""")
    try:
        data = process_yaml(config_file)
    except FileNotFoundError as e:
        print("[Error] while processing configuration file.")
        print(e)
        return

    roms_not_found = check_rom_paths(find_roms(data, roms_dir))
    if roms_not_found:
        print("[Error] Some roms could not be found:")
        for r in roms_not_found: print(r)
        return

    try:
        copy_roms(data, target_dir)
    except FileNotFoundError as e:
        print("[Error] while copying roms.")
        print(e)
        return

    if prune: process_prune(data, target_dir)

if __name__ == "__main__":
    main(auto_envvar_prefix='FFSYNC')
