import csv

#Contact(['Hannah','Smith','98 e nowhere','eugene','oregon','97212','5555555555','hus@uoregon.edu'])

class Contact(object):

    def __init__(self, list):
        if len(list) != 8:
            try:
                raise MyError(len(list))
            except MyError as e:
                print 'Error occurred, Contact expected 8 values but received'+e.value
        else:
            self.first_name = list[0]
            self.last_name = list[1]
            self.address = list[2]
            self.city = list[3]
            self.state = list[4]
            self.zip_code = list[5]
            self.phone = list[6]
            self.email = list[7]

    def __str__(self):
        return first_name + ',' + last_name + ',' + address + ',' + city + ',' + state + ',' + zip_code + ',' + phone + ',' + email

    def __hash__(self):
        return self.hash(first_name,last_name,zip_code)

    def to_dao(self):
        return "VALUES("+self.__str__()+")"

    def to_tsv(self):
        return first_name + '\t' + last_name + '\t' + address + '\t' + city + '\t' + state + '\t' + zip_code + '\t' + phone + '\t' + email + '\n'

class FieldError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)
