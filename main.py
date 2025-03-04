import argparse
from src.database import init_db, store_password, retrieve_password, list_services
from src.auth import set_master_password, verify_master_password
from src.password_generator import generate_password
from src.gui import root

# Initialize database
init_db()

parser = argparse.ArgumentParser(description="🔐 Simple Password Manager CLI")
parser.add_argument("action", choices=["store", "retrieve", "list", "set-master", "generate", "gui"], help="Action to perform")
parser.add_argument("--service", type=str, help="Service name (e.g., GitHub, Gmail)")
parser.add_argument("--username", type=str, help="Username for the service")
parser.add_argument("--password", type=str, help="Password to store")
parser.add_argument("--master", type=str, required=True, help="Master password for authentication")
parser.add_argument("--length", type=int, help="Length of generated password")

args = parser.parse_args()

if args.action == "set-master":
    set_master_password(args.master)

elif args.action == "store":
    if not verify_master_password(args.master):
        exit(1)
    if not args.service or not args.username or not args.password:
        print("❌ Missing required arguments for storing a password.")
    else:
        store_password(args.master, args.service, args.username, args.password)

elif args.action == "retrieve":
    if not verify_master_password(args.master):
        exit(1)
    if not args.service:
        print("❌ Please specify the service name to retrieve the password.")
    else:
        print(retrieve_password(args.master, args.service))

elif args.action == "list":
    if not verify_master_password(args.master):
        exit(1)
    services = list_services()
    if services:
        print("🔹 Stored Services:")
        for service in services:
            print(f"- {service}")
    else:
        print("📭 No saved passwords found.")

elif args.action == "generate":
    length = args.length if args.length else 16
    print(f"🔑 Generated Password: {generate_password(length)}")

elif args.action == "gui":
    root.mainloop()
