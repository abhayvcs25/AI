class Room:
    def __init__(self, room_number, status):
        self.room_number = room_number
        self.status = status

    def clean(self):
        if self.status == "dirty":
            self.status = "clean"
            return True
        return False


class VacuumCleaner:
    def __init__(self, rooms):
        self.rooms = rooms
        self.current_position = 1
        self.rooms_cleaned = 0
        self.movement_count = 0

    def move(self, room_number):
        distance = abs(self.current_position - room_number)

        self.movement_count += distance
        self.current_position = room_number

        print(f"Robot moved to Room {room_number}")

    def clean_room(self, room):
        if room.clean():
            self.rooms_cleaned += 1
            print(f"Room {room.room_number} was dirty → Cleaned")
        else:
            print(f"Room {room.room_number} is already clean")

    def start_cleaning(self):

        print("\n--- Cleaning Started ---")

        for room in self.rooms:

            self.move(room.room_number)

            self.clean_room(room)

        self.final_report()

    def final_report(self):

        dirty_rooms = 0

        for room in self.rooms:
            if room.status == "dirty":
                dirty_rooms += 1

        print("\n========== FINAL REPORT ==========")
        print(f"Total rooms       : {len(self.rooms)}")
        print(f"Rooms cleaned     : {self.rooms_cleaned}")
        print(f"Rooms still dirty : {dirty_rooms}")
        print(f"Robot movements   : {self.movement_count}")
        print(f"Final position    : Room {self.current_position}")
        print("==================================")


# -------- MAIN PROGRAM --------

n = int(input("Enter number of rooms: "))

rooms = []

for i in range(1, n + 1):

    status = input(
        f"Enter status of Room {i} (clean/dirty): "
    ).lower()

    while status not in ["clean", "dirty"]:
        print("Invalid status. Enter clean or dirty.")
        status = input(
            f"Enter status of Room {i} (clean/dirty): "
        ).lower()

    room = Room(i, status)
    rooms.append(room)


robot = VacuumCleaner(rooms)

robot.start_cleaning()