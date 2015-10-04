import csv
#Contact(['Hannah','Smith','98 e nowhere','eugene','oregon','97212','5555555555','hus@uoregon.edu'])
class Contact(object):
    def __init__(self, list):
        self.first_name = list[0]
        self.last_name = list[1]
        self.address = list[2]
        self.city = list[3]
        self.state = list[4]
        self.zip_code = list[5]
        self.phone = list[6]
        self.email = list[7]


    def to_csv(self):
        return [self.first_name,self.last_name,self.address,self.city,self.state,self.zip_code,self.phone,self.email]

    def __str__(self):
        return self.first_name,self.last_name,self.address,self.city,self.state,self.zip_code,self.phone,self.email


    def address_info(self):
        return [self.address, self.city, self.state, self.zip_code]
