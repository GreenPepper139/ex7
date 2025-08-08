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
        x = input(prompt).strip()
        if x.isdigit() or (x.startswith('-') and x[1:].isdigit()):
            return int(x)
        print("Invalid input.")

def get_poke_dict_by_id(poke_id):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by ID, or None if not found.
    """
    for poke in HOENN_DATA:
        if poke['ID'] == poke_id:
            return poke
    return None

def get_poke_dict_by_name(name):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by name, or None if not found.
    """
    for poke in HOENN_DATA:
        if poke['Name'].lower() == name.lower():
            return poke
    return None

def display_pokemon_list(poke_list):
    """
    Display a list of Pokemon dicts, or a message if empty.
    """
    if not poke_list:
        print("There are no Pokemons in this Pokedex that match the criteria.")
        return
    for poke in poke_list:
        print("ID: ", poke["ID"], ", Name: ", poke["Name"], ", Type: ", poke["Type"],
              ", HP: ", poke["HP"], ", Attack: ", poke["Attack"], ", Can Evolve: ", poke["Can Evolve"], sep="")
    pass


########################
# 2) BST (By Owner Name)
########################

def create_owner_node(owner_name, first_pokemon=None):
    """
    Create and return a BST node dict with keys: 'owner', 'pokedex', 'left', 'right'.
    """
    owner = {
        'owner': owner_name,
        'pokedex': [first_pokemon],
        'left': None,
        'right': None
    }
    return owner

def insert_owner_bst(root, new_node):
    """
    Insert a new BST node by owner_name (alphabetically). Return updated root.
    """
    if root is None:
        return new_node
    if new_node['owner'].lower() < root['owner'].lower():
        root['left'] = insert_owner_bst(root['left'], new_node)
    if new_node['owner'].lower() > root['owner'].lower():
        root['right'] = insert_owner_bst(root['right'], new_node)
    """
    the line below shouldn't happen, but it's here just in case
    """
    return root

def find_owner_bst(root, owner_name):
    """
    Locate a BST node by owner_name. Return that node or None if missing.
    """
    if root is None:
        return None
    if owner_name.lower() < root['owner'].lower():
        return find_owner_bst(root['left'], owner_name)
    elif owner_name.lower() > root['owner'].lower():
        return find_owner_bst(root['right'], owner_name)
    else:
        return root

def min_node(node):
    """
    Return the leftmost node in a BST subtree.
    """
    result = node
    while result['left'] is not None:
        result = result['left']
    return result

def delete_owner_bst(root, owner_name):
    """
    Remove a node from the BST by owner_name. Return updated root.
    """
    if root is None:
        return None
    if owner_name.lower() < root['owner'].lower():
        root['left'] = delete_owner_bst(root['left'], owner_name)
    elif owner_name.lower() > root['owner'].lower():
        root['right'] = delete_owner_bst(root['right'], owner_name)
    else:
        if root['left'] is None:
            return root['right']
        elif root['right'] is None:
            return root['left']
        min_val = min_node(root['right'])
        root['owner'] = min_val['owner']
        root['pokedex'] = min_val['pokedex']
        root['right'] = delete_owner_bst(root['right'], min_val['owner'])
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
    queue = [root]
    while queue:
        current = queue.pop(0)
        print("\nOwner:", current['owner'])
        display_pokemon_list(current['pokedex'])
        if current['left'] is not None:
            queue.append(current['left'])
        if current['right'] is not None:
            queue.append(current['right'])

def pre_order(root):
    """
    Pre-order traversal (root -> left -> right). Print data for each node.
    """
    if root is None:
        return
    print("\nOwner:", root['owner'])
    display_pokemon_list(root['pokedex'])
    pre_order(root['left'])
    pre_order(root['right'])
    pass

def in_order(root):
    """
    In-order traversal (left -> root -> right). Print data for each node.
    """
    if root is None:
        return
    in_order(root['left'])
    print("\nOwner:", root['owner'])
    display_pokemon_list(root['pokedex'])
    in_order(root['right'])
    pass

def post_order(root):
    """
    Post-order traversal (left -> right -> root). Print data for each node.
    """
    if root is None:
        return
    post_order(root['left'])
    post_order(root['right'])
    print("\nOwner:", root['owner'])
    display_pokemon_list(root['pokedex'])
    pass


########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner_node):
    """
    Prompt user for a Pokemon ID, find the data, and add to this owner's pokedex if not duplicate.
    """
    pokemon_ID = read_int_safe("Enter Pokemon ID to add: ")
    for poke in owner_node['pokedex']:
        if poke['ID'] == pokemon_ID:
            print("Pokemon already in the list. No changes made.")
            return
    new_pokemon = get_poke_dict_by_id(pokemon_ID)
    if new_pokemon is None:
        print("ID", pokemon_ID, "not found in Honen data.")
        return
    owner_node['pokedex'].append(new_pokemon)
    print("Pokemon ", new_pokemon["Name"], " (ID ", pokemon_ID, ") added to ", owner_node["owner"],
         "'s Pokedex.", sep="")
    pass

def release_pokemon_by_name(owner_node):
    """
    Prompt user for a Pokemon name, remove it from this owner's pokedex if found.
    """
    name = input("Enter Pokemon Name to release: ")
    for poke in owner_node['pokedex']:
        if poke['Name'].lower() == name.lower():
            print("Releasing ", poke["Name"], " from ", owner_node["owner"], ".", sep="")
            owner_node['pokedex'].remove(poke)
            return
    print("No Pokemon named '", name,"' in ", owner_node["owner"],"'s Pokedex.", sep="")
    pass

def evolve_pokemon_by_name(owner_node):
    """
    Evolve a Pokemon by name:
    1) Check if it can evolve
    2) Remove old
    3) Insert new
    4) If new is a duplicate, remove it immediately
    """
    name = input("Enter Pokemon Name to evolve: ")
    to_evolve = None
    for poke in owner_node['pokedex']:
        if poke['Name'].lower() == name.lower():
            to_evolve = poke
            break
    if to_evolve is None:
        print("No Pokemon named '", name,"' in ", owner_node["owner"],"'s Pokedex.", sep="")
        return
    if to_evolve['Can Evolve'] == "FALSE":
        print(to_evolve["Name"], " cannot evolve.")
        return
    new_pokemon = get_poke_dict_by_id(to_evolve['ID'] + 1)
    print("Pokemon evolved from ", to_evolve["Name"], " (ID ", to_evolve["ID"], ") to ",
            new_pokemon["Name"], " (ID ", new_pokemon["ID"],").", sep="")
    owner_node['pokedex'].remove(to_evolve)
    if new_pokemon in owner_node['pokedex']:
        print(new_pokemon["Name"], "was already present; releasing it immediately.")
        return
    owner_node['pokedex'].append(new_pokemon)
    pass


########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    """
    Collect all BST nodes into a list (arr).
    """
    if root is None:
        return
    gather_all_owners(root['left'], arr)
    arr.append(root)
    gather_all_owners(root['right'], arr)
    pass

def sort_owners_by_num_pokemon():
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    if ownerRoot is None:
        print("No owners at all.")
        return
    print("=== The Owners we have, sorted by number of Pokemons ===")
    arr = []
    gather_all_owners(ownerRoot, arr)
    arr.sort(key=lambda x: (len(x['pokedex']), x['owner'].lower()))
    for owner in arr:
        print("Owner: ", owner['owner'], " (has ", len(owner['pokedex']), " Pokemon)", sep="")
    pass


########################
# 6) Print All
########################

def print_all_owners():
    """
    Let user pick BFS, Pre, In, or Post. Print each owner's data/pokedex accordingly.
    """
    print("1) BFS", "2) Pre-Order", "3) In-Order", "4) Post-Order", sep="\n")
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
    pass


########################
# 7) The Display Filter Sub-Menu + filters
########################

def filter_by_type(owner_node):
    """
    Prompt user for a type, return a list of Pokemon dicts of that type.
    """
    type = input("Which Type? (e.g. GRASS, WATER): ")
    list = []
    for poke in owner_node['pokedex']:
        if poke['Type'].lower() == type.lower():
            list.append(poke)
    return list

def filter_by_evolve(owner_node):
    """
    Return a list of Pokemon dicts that can evolve.
    """
    list = []
    for poke in owner_node['pokedex']:
        if poke['Can Evolve'] == "TRUE":
            list.append(poke)
    return list

def filter_by_attack(owner_node):
    """
    Prompt user for a minimum attack value, return a list of Pokemon dicts with attack >= that value.
    """
    attack = read_int_safe("Enter Attack threshold: ")
    list = []
    for poke in owner_node['pokedex']:
        if poke['Attack'] > attack:
            list.append(poke)
    return list

def filter_by_hp(owner_node):
    """
    Prompt user for a minimum HP value, return a list of Pokemon dicts with HP >= that value.
    """
    hp = read_int_safe("Enter HP threshold: ")
    list = []
    for poke in owner_node['pokedex']:
        if poke['HP'] > hp:
            list.append(poke)
    return list

def filter_by_name(owner_node):
    """
    Prompt user for a name prefix, return a list of Pokemon dicts with that prefix.
    """
    prefix = input("Starting letter(s): ")
    list = []
    for poke in owner_node['pokedex']:
        if poke['Name'].lower().startswith(prefix.lower()):
            list.append(poke)
    return list

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
    choice = 0
    while choice != 7:
        print("\n-- Display Filter Menu --", "1. Only a certain Type", "2. Only Evolvable", "3. Only Attack above __",
            "4. Only HP above __", "5. Only names starting with letter(s)", "6. All of them!", "7. Back", sep="\n")
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            display_pokemon_list(filter_by_type(owner_node))
        elif choice == 2:
            display_pokemon_list(filter_by_evolve(owner_node))
        elif choice == 3:
            display_pokemon_list(filter_by_attack(owner_node))
        elif choice == 4:
            display_pokemon_list(filter_by_hp(owner_node))
        elif choice == 5:
            display_pokemon_list(filter_by_name(owner_node))
        elif choice == 6:
            display_pokemon_list(owner_node['pokedex'])
        elif choice == 7:
            print("Back to Pokedex Menu.")
        else:
            print("Invalid choice.")
    pass


########################
# exercises
########################
def create_a_pokedex():
    global ownerRoot
    name = input("Owner name: ")
    new_node = find_owner_bst(ownerRoot, name)
    if new_node is not None:
        print("Owner '", name,"' already exists. No new Pokedex created.", sep="")
        return
    print("Choose your starter Pokemon:", "1) Treecko", "2) Torchic", "3) Mudkip", sep="\n")
    choice = read_int_safe("Your choice: ")
    if choice == 1:
        starter = get_poke_dict_by_name("Treecko")
    elif choice == 2:
        starter = get_poke_dict_by_name("Torchic")
    elif choice == 3:
        starter = get_poke_dict_by_name("Mudkip")
    else:
        print("Invalid choice. No new Pokedex created.")
        return
    new_node = create_owner_node(name, starter)
    ownerRoot = insert_owner_bst(ownerRoot, new_node)
    print("New Pokedex created for ", name, " with starter ", starter["Name"], ".", sep="")

def delete_a_pokedex():
    global ownerRoot
    name = input("Enter owner to delete: ")
    owner = find_owner_bst(ownerRoot, name)
    if owner is None:
        print("Owner '", name,"' not found.", sep="")
        return
    ownerRoot = delete_owner_bst(ownerRoot, name)
    print("Deleting ", name,"'s entire Pokedex...\nPokedex deleted.", sep="")
    pass

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
    name = input("Owner name: ")
    owner = find_owner_bst(ownerRoot, name)
    if owner is None:
        print("Owner '", name,"' not found.", sep="")
        return
    choice = 0
    while choice != 5:
        print("\n-- ", owner["owner"], "'s Pokedex Menu --\n1. Add Pokemon\n2. Display Pokedex",
            "\n3. Release Pokemon\n4. Evolve Pokemon\n5. Back to Main", sep="")
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            add_pokemon_to_owner(owner)
        elif choice == 2:
            display_filter_sub_menu(owner)
        elif choice == 3:
            release_pokemon_by_name(owner)
        elif choice == 4:
            evolve_pokemon_by_name(owner)
        elif choice == 5:
            print("Back to Main Menu.")
        else:
            print("Invalid choice.")
    pass

def main_menu():
    """
    Main menu for:
    1. New Pokedex
    2. Existing Pokedex
    3. Delete a Pokedex
    4. Sort owners
    5. Print all
    6. Exit
    """
    choice = 0
    while choice != 6:
        print("\n=== Main Menu ===", "1. New Pokedex", "2. Existing Pokedex", "3. Delete a Pokedex",
            "4. Display owners by number of Pokemon", "5. Print All", "6. Exit", sep="\n")
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            create_a_pokedex()
        elif choice == 2:
            existing_pokedex()
        elif choice == 3:
            delete_a_pokedex()
        elif choice == 4:
            sort_owners_by_num_pokemon()
        elif choice == 5:
            print_all_owners()
        elif choice == 6:
            print("Goodbye!")
        else:
            print("Invalid choice.")
    pass

def main():
    """
    Entry point: calls main_menu().
    """
    main_menu()
    pass

if __name__ == "__main__":
    main()
