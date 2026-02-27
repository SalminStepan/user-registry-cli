from datetime import datetime
import json
import os

class Users:
    def __init__(self):
        self.users = []
        self.next_id = 1


    def create_user(self, name: str, phone: str, city: str):
        user = {
        "id": self.next_id,
        "name": name.strip(),
        "phone": phone.strip(),
        "city": city.strip(),
        "created_at": datetime.now().isoformat()
        }
        self.users.append(user)
        self.next_id +=1
        return user.copy()


    def list_users(self) -> list[dict]:
        return [user.copy() for user in self.users]

    def find_user(self, user_id:int):
        if not self.users:
            raise ValueError("Users catalog is empty")

        try:
            user_id = int(user_id)
        except ValueError:
            raise ValueError("user_id must be an integer")

        for user in self.users:
            if user["id"] == user_id:
                return user.copy()
        raise ValueError(f"User with id={user_id} not found")

    def delete_user(self, user_id):
        if not self.users:
           raise ValueError(f"Users catalog is empty")

        try:
            user_id = int(user_id)
        except ValueError:
            raise ValueError(f"user_id must be an integer")

        for i,user in enumerate(self.users):
            if user["id"] == user_id:
                deleted_user = user.copy()
                del self.users[i]
                return deleted_user
        raise ValueError(f"User with id={user_id} not found")

    def update_user(self, user_id, name, phone, city):
        if not self.users:
            raise ValueError(f"Users catalog is empty")

        try:
            user_id = int(user_id)
        except ValueError:
            raise ValueError(f"user_id must be an integer")

        if user_id < 1:
            raise ValueError("User id must be positive")

        for user in self.users:
            if user["id"] == user_id:
                user["name"] = name.strip()
                user["phone"] = phone.strip()
                user["city"] = city.strip()
                return user.copy()
        raise ValueError(f"User with id={user_id} not found")

    def search_user(self, query: str) -> list[dict]:
        q = query.strip().lower()
        if q == "":
            raise ValueError("Search cannot be empty")
        result = []
        for user in self.users:
            if (
                q in user["name"].lower() 
                or q in user["city"].lower() 
                or q in user["phone"].lower()
            ):
                result.append(user.copy())
        if not result:
            raise ValueError(f"{q} not found")
        return result

    def save(self, path: str = "users.json") -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)

    def load(self, path:str = "users.json") -> None:
        if not os.path.exists(path):
            self.users = []
            self.next_id = 1
            return

        with open(path, "r", encoding="utf-8") as f:
            self.users = json.load(f)

        if self.users:
            max_id = max(user["id"] for user in self.users)
            self.next_id = max_id + 1
        else:
            self.next_id = 1

def parse_id(parts, command_name):
    if len(parts) < 2:
        print(f"Usage: {command_name} <id>")
        return None

    user_id_str = parts[1]

    try:
        user_id = int(user_id_str)
    except ValueError:
        print("Error: id must be an integer")
        return None

    if user_id < 1:
        print("Error: id must be positive")
        return None

    return user_id

def cli_loop():
    store = Users()
    store.load()

    while True:

        cmd_line = input("> ").strip()
        parts = cmd_line.split()

        if len(parts) == 0:
            continue

        else:
            cmd = parts[0]
#save/exit
        if cmd == "exit":
            store.save()
            print("Bye!")
            break
# help
        elif cmd == "help":
            print("Commands:")
            print("add - add new user")
            print("get <id> - get user card by id")
            print("list - show all users")
            print("delete <id> - delete user by id")
            print("updade <id> - updade user information by id")
            print("search <text> - search user information")
            print("exit - save and exit")

# add (или create — выбери одно)
        elif cmd == "add":
            try:
                name = input("Name: ").strip()
                if not name:
                    raise ValueError("Name cannot be empty")
                phone = input("Phone: ").strip()
                if not phone:
                    raise ValueError("Phone cannot be empty")
                city = input("City: ").strip()
                if not city:
                        raise ValueError("City cannot be empty")
                user = store.create_user(name, phone, city)
                print(f"Added: {user}")
            except ValueError as e:
                print(f"Error: {e}")
# list
        elif cmd == "list":
            users = store.list_users()
            if not store.users:
                print(f"Catalog is empty")
            else:
                for u in users:
                    print(f'{u["id"]}. {u["name"]} tel.:{u["phone"]} from: {u["city"]}')
# parse_id

# get <id>
        elif cmd == "get":

            user_id = parse_id(parts, "get")

            if user_id is None:
                continue

            try:
                user = store.find_user(user_id)
                print(f"Found: {user}")
            except ValueError as e:
                print(f"Error: {e}")
# delete <id>
        elif cmd == "delete":

            user_id = parse_id(parts, "delete")

            if user_id is None:
                continue

            try:
                user = store.delete_user(user_id)
                print(f"Deleted: {user}")
            except ValueError as e:
                print(f"Error: {e}")
# update <id>
        elif cmd == "update":
            user_id = parse_id(parts, "update")
            if user_id is None:
                continue

            try:
                name = input("Name: ").strip()
                if not name:
                    raise ValueError("Name cannot be empty")

                phone = input("Phone: ").strip()
                if not phone:
                    raise ValueError("Phone cannot be empty")

                city = input("City: ").strip()
                if not city:
                    raise ValueError("City cannot be empty")

                user = store.update_user(user_id, name, phone, city)
                print(f"Updated: {user}")
            except ValueError as e:
                print(f"Error: {e}")
# search <text>
        elif cmd == "search":
            if len(parts) < 2:
                print("Usage search <text>")
                continue

            query = " ".join(parts[1:])

            try:
                results = store.search_user(query)

                for user in results:
                    print(f'{user["id"]}. {user["name"]} tel.:{user["phone"]} from: {user["city"]}')
            except ValueError as e:
                print(f"Error: {e}")

        else:
            print("Unknown command. Type 'help'.")

if __name__ == "__main__":
    cli_loop()





