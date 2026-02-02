FILE_NAME = "names.txt"

def add_name():
    name = input("Enter a name to store: ").strip()

    if not name:
        print("❌ Name cannot be empty\n")
        return

    with open(FILE_NAME, "a") as file:
        file.write(name + "\n")

    print("✅ Name saved successfully\n")

def read_names():
    try:
        with open(FILE_NAME, "r") as file:
            names = file.readlines()

        if not names:
            print("📭 No names found\n")
            return

        print("\n📋 Stored names:")
        for i, name in enumerate(names, start=1):
            print(f"{i}. {name.strip()}")
        print()

    except FileNotFoundError:
        print("📭 No names found (file does not exist yet)\n")

def main():
    while True:
        print("Choose an option:")
        print("1. Add name")
        print("2. Read all names")
        print("3. Exit")

        choice = input("Enter choice (1/2/3): ").strip()

        if choice == "1":
            add_name()
        elif choice == "2":
            read_names()
        elif choice == "3":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice\n")

if __name__ == "__main__":
    main()
