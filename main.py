import argparse
from src.database import init_db, store_password, retrieve_password, list_services

# Initialize database if it doesn't exist
init_db()

# Set up argument parsing
parser = argparse.ArgumentParser(description="🔐 Simple Password Manager CLI")
parser.add_argument("action", choices=["store", "retrieve", "list"], help="Action to perform")
parser.add_argument("--service", type=str, help="Service name (e.g., GitHub, Gmail)")
parser.add_argument("--username", type=str, help="Username for the service")
parser.add_argument("--password", type=str, help="Password to store")
parser.add_argument("--master", type=str, required=True, help="Master password for encryption")

args = parser.parse_args()

if args.action == "store":
    if not args.service or not args.username or not args.password:
        print("❌ Missing required arguments for storing a password.")
    else:
        store_password(args.master, args.service, args.username, args.password)

elif args.action == "retrieve":
    if not args.service:
        print("❌ Please specify the service name to retrieve the password.")
    else:
        print(retrieve_password(args.master, args.service))

elif args.action == "list":
    services = list_services()
    if services:
        print("🔹 Stored Services:")
        for service in services:
            print(f"- {service}")
    else:
        print("📭 No saved passwords found.")
