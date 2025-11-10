import csv

# Global BST root
ownerRoot = None

########################
# 0) Read from CSV -> HOENN_DATA
########################

def read_hoenn_csv(filename):
    """
    Reads 'hoenn_pokedex.csv' and returns a list of dicts:
      [ { "ID": int, "Name": str, "Type": str, "HP": int,
          "Attack": int, "Can Evolve": "TRUE"/"FALSE" },
        ... ]
    """
    data_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')  # Use comma as the delimiter
        first_row = True
        for row in reader:
            # It's the header row (like ID,Name,Type,HP,Attack,Can Evolve), skip it
            if first_row:
                first_row = False
                continue

            # row => [ID, Name, Type, HP, Attack, Can Evolve]
            if not row or not row[0].strip():
                break  # Empty or invalid row => stop
            d = {
                "ID": int(row[0]),
                "Name": str(row[1]),
                "Type": str(row[2]),
                "HP": int(row[3]),
                "Attack": int(row[4]),
                "Can Evolve": str(row[5]).upper()
            }
            data_list.append(d)
    return data_list


HOENN_DATA = read_hoenn_csv("hoenn_pokedex.csv")

########################
# 1) Helper Functions
########################

def read_int_safe(prompt):
    """
    Prompt the user for an integer, re-prompting on invalid input.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input.")

def get_poke_dict_by_id(poke_id):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by ID, or None if not found.
    """
    for pokemon in HOENN_DATA:
        if pokemon["ID"] == poke_id:
            return pokemon.copy()
    return None

def get_poke_dict_by_name(name):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by name, or None if not found.
    """
    for pokemon in HOENN_DATA:
        if pokemon["Name"].lower() == name.lower():
            return pokemon.copy()
    return None

def display_pokemon_list(poke_list):
    """
    Display a list of Pokemon dicts, or a message if empty.
    """
    if not poke_list:
        print("There are no Pokemons in this Pokedex that match the criteria.")
        return
    for pokemon in poke_list:
        print(f"ID: {pokemon['ID']}, Name: {pokemon['Name']}, Type: {pokemon['Type']}, "
              f"HP: {pokemon['HP']}, Attack: {pokemon['Attack']}, Can Evolve: {pokemon['Can Evolve']}")

########################
# 2) BST (By Owner Name)
########################

def create_owner_node(owner_name, first_pokemon=None):
    """
    Create and return a BST node dict with keys: 'owner', 'pokedex', 'left', 'right'.
    """
    return {
        "owner": owner_name,
        "pokedex": [] if first_pokemon is None else [first_pokemon],
        "left": None,
        "right": None
    }

def insert_owner_bst(root, new_node):
    """
    Insert a new BST node by owner_name (alphabetically). Return updated root.
    """
    if root is None:
        return new_node
    if new_node["owner"].lower() < root["owner"].lower():
        root["left"] = insert_owner_bst(root["left"], new_node)
    elif new_node["owner"].lower() > root["owner"].lower():
        root["right"] = insert_owner_bst(root["right"], new_node)
    return root

def find_owner_bst(root, owner_name):
    """
    Locate a BST node by owner_name. Return that node or None if missing.
    """
    if root is None or root["owner"].lower() == owner_name.lower():
        return root
    if owner_name.lower() < root["owner"].lower():
        return find_owner_bst(root["left"], owner_name)
    return find_owner_bst(root["right"], owner_name)

def min_node(node):
    """
    Return the leftmost node in a BST subtree.
    """
    while node and node["left"]:
        node = node["left"]
    return node

def delete_owner_bst(root, owner_name):
    """
    Remove a node from the BST by owner_name. Return updated root.
    """
    if root is None:
        return root
    if owner_name.lower() < root["owner"].lower():
        root["left"] = delete_owner_bst(root["left"], owner_name)
    elif owner_name.lower() > root["owner"].lower():
        root["right"] = delete_owner_bst(root["right"], owner_name)
    else:
        # Node with only one child or no child
        if root["left"] is None:
            return root["right"]
        elif root["right"] is None:
            return root["left"]
        # Node with two children: Get the inorder successor
        temp = min_node(root["right"])
        root["owner"] = temp["owner"]
        root["pokedex"] = temp["pokedex"]
        root["right"] = delete_owner_bst(root["right"], temp["owner"])
    return root

########################
# 3) BST Traversals
########################

def bfs_traversal(root):
    """
    BFS level-order traversal. Print each owner's name and # of pokemons.
    """
    if root is None:
        return
    queue = [root]  # Use list as a queue
    while queue:
        node = queue.pop(0)  # Dequeue the first element
        print(f"\nOwner: {node['owner']}")
        display_pokemon_list(node["pokedex"])
        if node["left"]:
            queue.append(node["left"])  # Enqueue left child
        if node["right"]:
            queue.append(node["right"])  # Enqueue right child

def pre_order(root):
    """
    Pre-order traversal (root -> left -> right). Print data for each node.
    """
    if root is None:
        return
    print(f"\nOwner: {root['owner']}")
    display_pokemon_list(root["pokedex"])
    pre_order(root["left"])
    pre_order(root["right"])

def in_order(root):
    """
    In-order traversal (left -> root -> right). Print data for each node.
    """
    if root is None:
        return
    in_order(root["left"])
    print(f"\nOwner: {root['owner']}")
    display_pokemon_list(root["pokedex"])
    in_order(root["right"])

def post_order(root):
    """
    Post-order traversal (left -> right -> root). Print data for each node.
    """
    if root is None:
        return
    post_order(root["left"])
    post_order(root["right"])
    print(f"\nOwner: {root['owner']}")
    display_pokemon_list(root["pokedex"])

########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner_node):
    """
    Prompt user for a Pokemon ID, find the data, and add to this owner's pokedex if not duplicate.
    """
    poke_id = read_int_safe("Enter Pokemon ID to add: ")
    pokemon = get_poke_dict_by_id(poke_id)
    if not pokemon:
        print(f"ID {poke_id} not found in Honen data.")
        return
    if pokemon in owner_node["pokedex"]:
        print("Pokemon already in the list. No changes made.")
        return
    owner_node["pokedex"].append(pokemon)
    print(f"Pokemon {pokemon['Name']} (ID {pokemon['ID']}) added to {owner_node['owner']}'s Pokedex.")

def release_pokemon_by_name(owner_node):
    """
    Prompt user for a Pokemon name, remove it from this owner's pokedex if found.
    """
    poke_name = input("Enter Pokemon Name to release: ").strip()
    pokemon = get_poke_dict_by_name(poke_name)
    if not pokemon or pokemon not in owner_node["pokedex"]:
        print(f"No Pokemon named '{poke_name}' in {owner_node['owner']}'s Pokedex.")
        return
    owner_node["pokedex"].remove(pokemon)
    print(f"Releasing {pokemon['Name']} from {owner_node['owner']}.")

def evolve_pokemon_by_name(owner_node):
    """
    Evolve a Pokémon by name:
    1) Check if it can evolve.
    2) Remove the original Pokémon from the list.
    3) Insert the evolved Pokémon in the same position in the list.
    4) If the evolved Pokémon is a duplicate, remove it immediately.
    """
    poke_name = input("Enter Pokemon Name to evolve: ").strip()
    pokemon = get_poke_dict_by_name(poke_name)  # Get the Pokémon by name

    # Check if the Pokémon is found and exists in the owner's Pokédex
    if not pokemon or pokemon not in owner_node["pokedex"]:
        print(f"No Pokemon named '{poke_name}' in {owner_node['owner']}'s Pokedex.")
        return

    # Check if the Pokémon can evolve
    if pokemon["Can Evolve"] != "TRUE":
        print(f"{poke_name} cannot evolve.")
        return

    # Remove the original Pokémon from the Pokédex
    owner_node["pokedex"].remove(pokemon)

    # Get the evolved Pokémon
    evolved_pokemon = get_poke_dict_by_id(pokemon["ID"] + 1)

    if evolved_pokemon:
        # Check if the evolved Pokémon is already in the owner's Pokédex
        if evolved_pokemon in owner_node["pokedex"]:
            print(f"Pokemon evolved from {pokemon['Name']} (ID {pokemon['ID']}) to {evolved_pokemon['Name']} (ID {evolved_pokemon['ID']}).")
            print(f"{evolved_pokemon['Name']} was already present; releasing it immediately.")
        else:
            print(f"Pokemon evolved from {pokemon['Name']} (ID {pokemon['ID']}) to {evolved_pokemon['Name']} (ID {evolved_pokemon['ID']}).")
            # Append the evolved Pokémon to the end of the Pokédex
            owner_node["pokedex"].append(evolved_pokemon)

    else:
        print(f"Evolution data for {poke_name} not found.")


########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    """
    Collect all BST nodes into a list (arr), to be sorted later:
    1) First by the number of Pokemons in ascending order.
    2) If there's a tie, by owner name alphabetically (ignoring case).
    3) Owners with no pokemons will always come first.
    """
    if root is None:
        return
    gather_all_owners(root["left"], arr)  # Traverse left subtree
    arr.append(root)  # Add the current node to the list
    gather_all_owners(root["right"], arr)  # Traverse right subtree

def sort_owners_by_num_pokemon():
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    owners = []
    gather_all_owners(ownerRoot, owners)

    # If there are no owners, display the message and return
    if not owners:
        print("No owners at all.")
        return

    """
    Sort owners:
    Owners with no Pokemons come first (using len(x["pokedex"]) == 0)
    Then by the number of Pokemon (ascending)
    If there's a tie, sort alphabetically by owner name regardless to to lower or upper case
    """
    owners.sort(key=lambda x: (len(x["pokedex"]) == 0, len(x["pokedex"]), x["owner"].lower()))

    print("=== The Owners we have, sorted by number of Pokemons ===")

    # Print the sorted list of owners with their Pokémon count
    for owner in owners:
        if len(owner["pokedex"]) == 0:
            print(f"Owner: {owner['owner']} (There are no Pokemons in this Pokedex that match the criteria.)")
        else:
            print(f"Owner: {owner['owner']} (has {len(owner['pokedex'])} Pokemon)")

########################
# 6) Print All
########################

def print_all_owners():
    """
    Let user pick BFS, Pre, In, or Post. Print each owner's data/pokedex accordingly.
    """
    print("1) BFS")
    print("2) Pre-Order")
    print("3) In-Order")
    print("4) Post-Order")
    choice = read_int_safe("Your choice: ")
    if choice == 1:
        bfs_traversal(ownerRoot)
    elif choice == 2:
        pre_order(ownerRoot)
    elif choice == 3:
        in_order(ownerRoot)
    elif choice == 4:
        post_order(ownerRoot)
    else:
        print("Invalid choice.")

########################
# 7) The Display Filter Sub-Menu
########################

def display_filter_sub_menu(owner_node):
    """
    1) Only type X
    2) Only evolvable
    3) Only Attack above
    4) Only HP above
    5) Only name starts with
    6) All
    7) Back
    """
    while True:
        print("\n-- Display Filter Menu --")
        print("1. Only a certain Type")
        print("2. Only Evolvable")
        print("3. Only Attack above __")
        print("4. Only HP above __")
        print("5. Only names starting with letter(s)")
        print("6. All of them!")
        print("7. Back")
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            poke_type = input("Which Type? (e.g. GRASS, WATER): ").strip()
            filtered = [p for p in owner_node["pokedex"] if p["Type"].lower() == poke_type.lower()]
        elif choice == 2:
            filtered = [p for p in owner_node["pokedex"] if p["Can Evolve"] == "TRUE"]
        elif choice == 3:
            attack_threshold = read_int_safe("Enter Attack threshold: ")
            filtered = [p for p in owner_node["pokedex"] if p["Attack"] > attack_threshold]
        elif choice == 4:
            hp_threshold = read_int_safe("Enter HP threshold: ")
            filtered = [p for p in owner_node["pokedex"] if p["HP"] > hp_threshold]
        elif choice == 5:
            prefix = input("Starting letter(s): ").strip().lower()
            filtered = [p for p in owner_node["pokedex"] if p["Name"].lower().startswith(prefix)]
        elif choice == 6:
            filtered = owner_node["pokedex"]
        elif choice == 7:
            print("Back to Pokedex Menu.")
            break
        else:
            print("Invalid choice.")
            continue
        display_pokemon_list(filtered)

########################
# 8) Sub-menu & Main menu
########################

def existing_pokedex():
    """
    Ask user for an owner name, locate the BST node, then show sub-menu:
    - Add Pokemon
    - Display (Filter)
    - Release
    - Evolve
    - Back
    """
    owner_name = input("Owner name: ").strip()
    owner_node = find_owner_bst(ownerRoot, owner_name)
    if not owner_node:
        print(f"Owner '{owner_name}' not found.")
        return
    while True:
        print(f"\n-- {owner_node['owner']}'s Pokedex Menu --")
        print("1. Add Pokemon")
        print("2. Display Pokedex")
        print("3. Release Pokemon")
        print("4. Evolve Pokemon")
        print("5. Back to Main")
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            add_pokemon_to_owner(owner_node)
        elif choice == 2:
            display_filter_sub_menu(owner_node)
        elif choice == 3:
            release_pokemon_by_name(owner_node)
        elif choice == 4:
            evolve_pokemon_by_name(owner_node)
        elif choice == 5:
            print("Back to Main Menu.")
            break
        else:
            print("Invalid choice.")

def main_menu():
    """
    Main menu for:
    1) New Pokedex
    2) Existing Pokedex
    3) Delete a Pokedex
    4) Sort owners
    5) Print all
    6) Exit
    """
    global ownerRoot
    while True:
        print("\n=== Main Menu ===")
        print("1. New Pokedex")
        print("2. Existing Pokedex")
        print("3. Delete a Pokedex")
        print("4. Display owners by number of Pokemon")
        print("5. Print All")
        print("6. Exit")
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            owner_name = input("Owner name: ").strip()
            if find_owner_bst(ownerRoot, owner_name):
                print(f"Owner {owner_name} already exists. No new Pokedex created.")
                continue
            while True:
                print("Choose your starter Pokemon:")
                print("1) Treecko")
                print("2) Torchic")
                print("3) Mudkip")
                first_pokemon_id = read_int_safe("Your choice: ")
                if first_pokemon_id == 1:
                    first_pokemon_id = 1
                    break
                elif first_pokemon_id == 2:
                    first_pokemon_id = 4
                    break
                elif first_pokemon_id == 3:
                    first_pokemon_id = 7
                    break
                else:
                    print("Invalid input")
            first_pokemon = get_poke_dict_by_id(first_pokemon_id) if first_pokemon_id != -1 else None
            new_node = create_owner_node(owner_name, first_pokemon)
            ownerRoot = insert_owner_bst(ownerRoot, new_node)
            print(f"New Pokedex created for {owner_name} with starter {first_pokemon['Name']}.")
        elif choice == 2:
            existing_pokedex()
        elif choice == 3:
            owner_name = input("Enter owner to delete: ").strip()
            if find_owner_bst(ownerRoot, owner_name):
                print(f"Deleting {owner_name}'s entire Pokedex...")
                ownerRoot = delete_owner_bst(ownerRoot, owner_name)
                print("Pokedex deleted.")
            else:
                print(f"Owner '{owner_name}' not found.")
        elif choice == 4:
            sort_owners_by_num_pokemon()
        elif choice == 5:
            print_all_owners()
        elif choice == 6:
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

def main():
    """
    Entry point: calls main_menu().
    """
    main_menu()

if __name__ == "__main__":
    main()
