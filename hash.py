from xxhash import xxh32
import os


# (Hashes the given directory)
def _hash_directory(dirpath: str, dirnames: list[str], filenames: list[str], thorough: bool) -> str:
    # Create hash
    hash_fn: xxh32 = xxh32()
    
    # Hash the names of all (non-recursive) subdirectories
    for dirname in sorted(dirnames):
        hash_fn.update(dirname)
    
    # Hash files
    for filename in sorted(filenames):
        filepath: str = os.path.join(dirpath, filename)

        if thorough:
            # Hash the raw contents of all files
            with open(filepath, 'rb') as f:
                while chunk := f.read(8192):
                    hash_fn.update(chunk)
        else:
            # Hash the size of all files
            stat: os.stat_result = os.stat(filepath)
            hash_fn.update(filename + str(stat.st_size))
    
    # Return digest
    return hash_fn.hexdigest()


# (Tuple version of _hash_directory)
def _hash_directory_tuple(tuple: tuple[str, list[str], list[str]], dir: str) -> tuple[str, str]:
    dirpath, dirnames, filenames = tuple
    print(dirpath)
    return (os.path.relpath(dirpath, dir), _hash_directory(dirpath, dirnames, filenames, True))


# (Hashes and saves the given directory)
def hash_and_save(dir: str, out: str, thorough: bool) -> None:
    import json

    # TODO add parallel flag
    parallel = True

    # Get all directory data
    walk = list(os.walk(dir))

    data: dict[str, str]

    if parallel:
        from multiprocessing import Pool
        import functools

        # Create pool, map over directory data, hash
        with Pool(10) as p:
            data_list: list[tuple[str, str]] = p.map(functools.partial(_hash_directory_tuple, dir=dir), walk)

        data = dict(data_list)
    else:
        from tqdm import tqdm

        # Map over directory data, hash
        data = {
            os.path.relpath(dirpath, dir): _hash_directory(dirpath, dirnames, filenames, thorough)
            for (dirpath, dirnames, filenames) in tqdm(walk)
        }

    # Serialize to file
    with open(out, "w") as file:
        json.dump(data, file, indent=3)
