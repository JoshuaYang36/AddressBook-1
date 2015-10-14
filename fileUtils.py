import csv

def import_csv(file,ab):
    #TODO: should pass in the id of addressbook so that dict can add id
    contact_list = []
    with open(file,'rb') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            row.update({'ab':ab})
            contact_list.append(row)
    return contact_list

def export_csv():
    pass
