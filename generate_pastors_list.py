import csv

def save_to_csv(data, filename="members.csv"):
    # Ensure there's data to write
    if not data:
        print("No data provided.")
        return

    # Extract field names from the first dictionary
    fieldnames = data[0].keys()

    # Write to CSV
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Data successfully written to {filename}")


# Example usage:
members = [
    {'name': 'John Kabia', 'church': 'KAG Resurrection', 'section': 'Kangundo Road'},
    {'name': 'Daniel  Watunu', 'church': "KAG God's Favour", 'section': 'Kangundo Road'},
    {'name': 'Daniel Mwathe', 'church': 'KAG Saika', 'section': 'Kangundo Road'},
    {'name': 'Daniel Gitau', 'church': 'KAG Baraka', 'section': 'Kangundo Road'},
    {'name': 'G. Maina', 'church': 'KAG Restoration', 'section': 'Kangundo Road'},
    {'name': 'John Marite', 'church': 'KAG Shilanga', 'section': 'Kangundo Road'},
    {'name': 'Davi Shukuru', 'church': 'KAG La Borne', 'section': 'Kangundo Road'},
    {'name': 'Peter  Nuthu', 'church': 'KAG New Mathare', 'section': 'Dandora'},
    {'name': 'Martin Warui', 'church': 'KAG Kahawa Sukari', 'section': 'Dandora'},
    {'name': 'Dan Muiruri', 'church': 'KAG Marura', 'section': 'Dandora'},
    {'name': 'Ephantus  Nyaga', 'church': 'KAG Komabridge', 'section': 'Dandora'},
    {'name': 'Rose Mitambo', 'church': 'KAG Revival', 'section': 'Dandora'},
    {'name': 'Alfred Okello', 'church': 'KAG Canaan', 'section': 'Dandora'}
]

save_to_csv(members, "pastors_missing_role.csv")
