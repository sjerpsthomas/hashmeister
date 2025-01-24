import json


# (Loads a hashed content file)
def load_hash(filename: str) -> dict[str, str]:
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


# (Prints the difference of two hashes content files)
def print_difference(first: str, second: str) -> None:
    # Load both hashes
    first_data: dict[str, str] = load_hash(first)
    second_data: dict[str, str] = load_hash(second)

    # Transform into sets
    first_items: set[tuple[str, str]] = set(first_data.items())
    second_items: set[tuple[str, str]] = set(second_data.items())

    # Get set difference
    diff: set[tuple[str, str]] = first_items ^ second_items
    
    # Short-circuit when no differences found
    if len(diff) == 0:
        print("No differences found!")
        return

    # Print
    print(f"{len(diff)} differences found")

    # Print all differences
    for folder, _ in diff:
        # TODO take out duplicates if hash is different

        # Determine where the difference is
        first_has: bool = folder in first_data
        second_has: bool = folder in second_data

        # Print accordingly
        message: str
        match (first_has, second_has):
            case (False, False): raise Exception(f"Unknown difference {folder}")
            case (False, True): message = f"{first} misses folder {folder}"
            case (True, False): message = f"{second} misses folder {folder}"
            case (True, True): message = f"Hash differs in folder {folder}"
        
        print("- " + message)

