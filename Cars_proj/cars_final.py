import os 
import csv

class CarBase:
    def __init__(self, car_type, brand, photo_file_name, carrying):
        allowed_attr = ('car', 'truck', 'spec_machine')
        if car_type not in allowed_attr:
            raise ValueError("Car type should be 'car', 'truck', or 'spec_machine' only")
        else:
            self.car_type = car_type
        self.brand = brand
        self.photo_file_name = photo_file_name
        if carrying == '':
            self.carrying = carrying
        else:
            self.carrying = float(carrying)

    def get_photo_file_ext(self):
        path_ext = path.splitext(self.photo_file_name)
        return path_ext[1]
        
class Car(CarBase):
    def __init__(self, car_type, brand, passenger_seats_count, photo_file_name, carrying):
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    def __init__(self, car_type, brand, photo_file_name, body_whl, carrying):
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.body_whl = body_whl
        if body_whl is "":
            self.body_length, self.body_width, self.body_height = float(0)
        else:
            self.body_length, self.body_width, self.body_height = [float(param) for param in body_whl.split('x')]

    def get_body_volume(self):
        volume = self.body_length * self.body_width * self.body_height
        return volume 


class SpecMachine(CarBase):
    def __init__(self, car_type, brand, photo_file_name, carrying, extra):
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.extra = extra


def get_car_list(csv_filename):

    variable_dict = {}
    cars_list = []

    def make_vars(name, container, index=0):
        for _ in range(len(container)):
            key = '{}{}'.format(name, index)
            value = container[index]
            if value == []:
                continue
            else:
                variable_dict[key] = value
            index += 1

    def make_list(index=0):
        dict_list = [value for value in variable_dict.items()]
        while index < len(dict_list):
            element = dict_list[index]
            try:
                if element[1][0] == 'car':
                    cars_list.append(Car(*element[1][0:5]))
                elif element[1][0] == 'truck':
                    cars_list.append(Truck(*element[1][0:5]))
                elif element[1][0] == 'spec_machine':
                    cars_list.append(SpecMachine(*element[1][0:5]))
            except(ValueError, TypeError):
                pass
            index += 1

    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=";")
        next(reader)
        rows_list = []
        for row in reader:
            rows_list.append(row)

        make_vars('car', rows_list)
        make_list()

    return cars_list

