import sys
import os

# Function to read the argument file passed
def read_argument_file(argument_file):
    users = {}
    groups = {}
    with open(argument_file, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) != 3:
                continue  # Skip lines with more or less than 3 entries
            user_or_group, name, id_ = parts
            if user_or_group == 'user':
                users[name] = id_
            elif user_or_group == 'group':
                groups.setdefault(name, []).append(id_)  # Group names map to a list of IDs
    return users, groups

# Function to print all users in the argument file
def print_users(users):
    all_users = sorted(users.keys())
    if all_users:
        print("Available users:")
        for user in all_users:
            print(user)
    else:
        print("No users available")

# Function to print all groups in the argument file
def print_groups(groups):
    all_groups = sorted(groups.keys())
    if all_groups:
        print("Available groups:")
        for group in all_groups:
            print(group)
    else:
        print("No groups available")

# Function to print information about a specific user
def print_user_info(user, users, groups):
    if user in users:
        user_id = users[user]
        user_groups = [group for group, ids in groups.items() if user_id in ids]
        print(f"User {user}:")
        print(f"ID: {user_id}")
        if user_groups:
            print(f"Groups: {', '.join(user_groups)}")
        else:
            print("Groups: None")
    else:
        print(f"User {user} not found")

# Function to handle unknown option entry
def print_usage():
    print("Available Options:")
    print("  -u                 List all available users")
    print("  -g                 List all available groups")
    print("  -i <user>          List information for the specified user")
    print("  -h                 Print this help message")

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    option = sys.argv[1]

    # Validate the -h option immediately
    if option == '-h':
        print_usage()
        sys.exit(0)

    # Check if there are enough arguments
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    argument_file = sys.argv[-1]  # The last argument should be the file
    user = sys.argv[2] if option == '-i' else None  # The second argument is the username for -i

    # Check if the argument file is provided and is readable
    if option in ['-u', '-g', '-i'] and (not os.path.isfile(argument_file) or not os.access(argument_file, os.R_OK)):
        print(f"Error: Argument file '{argument_file}' does not exist or is not readable")
        sys.exit(1)

    users, groups = read_argument_file(argument_file)

    if option == '-u':
        print_users(users)
    elif option == '-g':
        print_groups(groups)
    elif option == '-i':
        if user:  # Ensure there is a username specified
            print_user_info(user, users, groups)
        else:
            print("******Error: User not specified******")
            print_usage()
            sys.exit(1)
    else:
        print("******Error: Invalid option******")
        print_usage()
        sys.exit(1)

if __name__ == "__main__":
    main()
