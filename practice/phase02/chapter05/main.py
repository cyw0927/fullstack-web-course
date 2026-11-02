"""Run database connection and SELECT checks without starting FastAPI."""

from db import check_connection, fetch_members


def main():
    database, schema = check_connection()
    print("=== Connected database / schema ===")
    print(database, schema)
    print("=== Member records (tuples) ===")
    rows = fetch_members()
    for member in rows:
        print(member)
    print(f"Total rows: {len(rows)}")


if __name__ == "__main__":
    main()
