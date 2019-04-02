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
        try:
            self.carrying = float(carrying)
        except ValueError:
            self.carrying = ''

    def get_photo_file_ext(self):
        path_ext = os.path.splitext(self.photo_file_name)
        return path_ext[1]
        
class Car(CarBase):
    def __init__(self, car_type, brand, passenger_seats_count, photo_file_name, carrying):
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    def __init__(self, car_type, brand, photo_file_name, carrying, body_whl):
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.body_whl = body_whl
        if self.body_whl == '':
            try:
                self.body_length, self.body_width, self.body_height = float(0)
            except ValueError:
                pass
            except TypeError:
                pass
        else:
            try:
                self.body_length, self.body_width, self.body_height = [float(param) for param in self.body_whl.split('x')]
            except ValueError:
                print("Float Error_2")
                
    def get_body_volume(self):
        volume = self.body_length * self.body_width * self.body_height
        return volume 


class SpecMachine(CarBase):
    def __init__(self, car_type, brand, photo_file_name, carrying, extra):
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.extra = extra

class CsvParser:
    
    done = False
    
    def __init__(self, lst):
        self.lst = lst
              
    @property
    def attr_to_init(self):
        attrs_lst = self._clear(self.csv_dict())
        return attrs_lst
    
    def _clear(self, container):
        cleared_dict = {}
        for key, value in container.items():
            try:
                assert len(value) > 5
                if value[0] == 'car':
                    assert Car(*value[0:5])
                elif value[0] == 'truck':
                    assert Truck(*value[0:5])
                elif value[0] == 'spec_machine':
                    assert SpecMachine(*value[0:5])
            except AssertionError:
                continue
            else:
                cleared_dict[key] = value
        CsvParser.done = True
        return list(cleared_dict.values())
    
    def csv_dict(self, sub_id='car_id_', index=0):
        vars_dict = {}
        for _ in range(len(self.lst)):
            key = '{}{}'.format(sub_id, index)
            value = self.lst[index]
            vars_dict[key] = value
            index += 1
        return vars_dict
    
def get_car_list(csv_filename):
    
    rows_list = []
    car_list = []
    parser = CsvParser(rows_list)
    
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=";")
        next(reader)
        for row in reader:
            rows_list.append(row)

    for value in parser.attr_to_init:
        if value[0] == 'car':
            car_list.append(Car(*value[0:5]))
        elif value[0] == 'truck':
            car_list.append(Truck(*value[0:5]))
        elif value[0] == 'spec_machine':
            car_list.append(SpecMachine(*value[0:5]))
    return car_list