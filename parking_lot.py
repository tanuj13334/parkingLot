import vehicle
import argparse
import sys

if sys.version_info[0] == 2:
    input = raw_input


class ParkingLot:
    def __init__(self):
        self.capacity = 0
        self.slot_id = 0
        self.num_of_occupied_slots = 0
        self.slots = []

    # create parking lot to park cars
    def create_parking_lot(self, capacity):
        self.slots = [-1] * capacity
        self.capacity = capacity
        return self.capacity

    # process input from file
    def process(self, line):
        if line.startswith('Create_parking_lot'):
            n = int(line.split(' ')[1])
            res = self.create_parking_lot(n)
            print('Created a parking of '+str(res)+' slots')

        elif line.startswith('Park'):
            parking_car_details = line.split(' ')
            registration_num = parking_car_details[1].strip()
            driver_age = int(parking_car_details[3].strip())

            res = self.park(registration_num, driver_age)
            if res == -1:
                print("Sorry, parking lot is full")
            else:
                print('Car with vehicle registration number "' + str(registration_num) +
                      '" has been parked at slot number ' + str(res))

        elif line.startswith('Leave'):
            leave_slot_id = int(line.split(' ')[1].strip())

            leaving_vehicle_details = self.leave(leave_slot_id)
            if leaving_vehicle_details:
                print('Slot number '+ str(leave_slot_id) +
                      ' vacated, the car with vehicle registration number "' +
                      str(leaving_vehicle_details['registration_num']) +
                      '" left the space, the driver of the car was of age '+
                      str(leaving_vehicle_details['driver_age']))
            else:
                print('Slot ' + leave_slot_id + ' is already vacated')

        elif line.startswith('Slot_number_for_car_with_number'):
            registration_num = str(line.split(' ')[1].strip())
            slot_num = self.get_slot_num_from_registration_num(registration_num)
            if slot_num == -1:
                print("null")
            else:
                print(slot_num)

        elif line.startswith('Slot_numbers_for_driver_of_age'):
            driver_age = int(line.split(' ')[1].strip())
            slot_nums = self.get_slot_nums_from_drivers_age(driver_age)
            if not slot_nums:
                print("null")
            else:
                print(','.join(str(x) for x in slot_nums))

        elif line.startswith('Vehicle_registration_number_for_driver_of_age'):
            driver_age = int(line.split(' ')[1].strip())
            slot_nums = self.get_registration_nums_from_drivers_age(driver_age)
            if not slot_nums:
                print("null")
            else:
                print(','.join(str(x) for x in slot_nums))

        elif line.startswith('exit'):
            exit(0)

    # get empty slot to park
    def get_empty_slot(self):
        for i in range(len(self.slots)):
            if self.slots[i] == -1:
                return i

    # park car from at slot
    def park(self, registration_num, driver_age):
        if self.num_of_occupied_slots < self.capacity:
            slot_id = self.get_empty_slot()

            self.slots[slot_id] = vehicle.Car(registration_num, driver_age)
            self.slot_id = self.slot_id+1

            self.num_of_occupied_slots = self.num_of_occupied_slots + 1
            return slot_id+1
        else:
            return -1

    # remove car from slot
    def leave(self, slot_id):
        leaving_vehicle_details = {}

        if self.num_of_occupied_slots > 0 and self.slots[slot_id-1] != -1:
            leaving_vehicle_details['registration_num'] = self.slots[slot_id-1].registration_num
            leaving_vehicle_details['driver_age'] = self.slots[slot_id-1].driver_age

            self.slots[slot_id-1] = -1
            self.num_of_occupied_slots = self.num_of_occupied_slots - 1

            return leaving_vehicle_details
        else:
            return False

    def get_slot_num_from_registration_num(self, registration_num):
        for i in xrange(self.num_of_occupied_slots):
            if self.slots[i].registration_num == registration_num:
                return i+1
            else:
                continue
        return -1

    def get_slot_nums_from_drivers_age(self, driver_age):
        slots_num_with_driver_age = []

        for i in xrange(self.num_of_occupied_slots):
            if self.slots[i].driver_age == driver_age:
                slots_num_with_driver_age.append(i+1)

        return slots_num_with_driver_age

    def get_registration_nums_from_drivers_age(self, driver_age):

        reg_nums_with_driver_age = []
        for i in xrange(self.num_of_occupied_slots):
            if self.slots[i].driver_age == driver_age:
                reg_nums_with_driver_age.append(self.slots[i].registration_num)

        return reg_nums_with_driver_age


def main():

    parkinglot = ParkingLot()
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action="store", required=False, dest='src_file', help="Input File")
    args = parser.parse_args()

    if args.src_file:
        with open(args.src_file) as f:
            for line in f:
                line = line.rstrip('\n')
                parkinglot.process(line)
    else:
        while True:
            line = input("$ ")
            parkinglot.process(line)


if __name__ == '__main__':
    main()
