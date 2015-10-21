


"""
Address Book Unit Test Program

Author: Max Kohl
Contributors in alphabetic order by last name:
        Abdulmajeed Kadi, Garrett Morrison, Hannah Smith, Joshua Yang
"""


import time
import subprocess
import glob
successes = []
warnings = []
errors = []
time_threshold = 0.5
print("Beginning unit tests")
print("Beginning Academic Integrity Test")
files = glob.glob("*.py")
for fi in files:
    na = ["garrett","hannah","josh","majeed","max"]
    names_array = ["garrett","hannah","josh","majeed","max"]
    counter = 0
    f = open(fi, 'r')
    lines = f.readlines()
    for line in lines:
        line = line.lower()
        for name in na:
            if name in line and name in names_array:
                names_array.remove(name)
    if len(names_array) == 0:
        successes.append("Academic Integrity SUCCESS: " + str(fi))
    else:
        errors.append("Academic Integrity FAIL: "+str(fi)+" does not contain the following names names: " + (" ").join(names_array))


print("Beginning import tests")
#Contact module
succeed = False
start_time = time.clock()
try:
    out = subprocess.check_output(['python',"contact.py"])
    if len(out) == 0:
        succeed = True
    import contact
except subprocess.CalledProcessError as e:
    errors.append("Import FAIL: contact.py "+str(e))

end_time = time.clock()
elapsed_time = end_time - start_time
if (succeed and elapsed_time < time_threshold):
    successes.append("Import SUCCESS: contact.py")
elif (elapsed_time >= time_threshold):
    errors.append("Import FAIL: contact.py time limit exceeded: " + str(elapsed_time))


print("Beginning contact instantiation")
#Contact class
succeed = False
start_time = time.clock()
try:
    person = contact.ContactDAO(['Hannah','Smith','98 e nowhere','eugene','oregon','97212','5555555555','hus@uoregon.edu'])
    succeed = True
except:
    errors.append("Instance Creation FAIL: Contact")
end_time = time.clock()
elapsed_time = end_time - start_time
if (succeed and elapsed_time < time_threshold):
    successes.append("Instance SUCCESS: Contact")
elif (elapsed_time >= time_threshold):
    errors.append("Instance FAIL: Contact time limit exceeded: " + str(elapsed_time))

print("Beginning ContactDAO method testing")
#Contact class
succeed = False
output = False
expected_output = long(39278464)
start_time = time.clock()
try:
    contact_id = id(person)
    succeed = True
    output = type(contact_id) == type(expected_output)
except:
    errors.append("Method Test FAIL: id(contact)")
end_time = time.clock()
elapsed_time = end_time - start_time
if (output == True and succeed and elapsed_time < time_threshold):
    successes.append("Method Test SUCCESS: id(contact)")
elif (output == False):
    errors.append("Method Test FAIL: id(contact) produces bad output.\nExpected:\n"+ str(type(expected_output))+ "\nand got:\n" + str(type(contact_id)))
elif (elapsed_time >= time_threshold):
    errors.append("Instance FAIL: id(contact) time limit exceeded: " + str(elapsed_time))


#Contact class
succeed = False
output = False
expected_output = 'Smith,Hannah,98 e nowhere,eugene,oregon,97212,5555555555,hus@uoregon.edu'
start_time = time.clock()
try:
    contact_id = str(person)
    succeed = True
    output = (type(contact_id) == type(expected_output)) and contact_id == expected_output
except:
    errors.append("Method Test FAIL: str(contact)")
end_time = time.clock()
elapsed_time = end_time - start_time
if (output == True and succeed and elapsed_time < time_threshold):
    successes.append("Method Test SUCCESS: str(contact)")
elif (output == False):
    errors.append("Method Test FAIL: str(contact) produces bad output.\nExpected:\n"+ str(expected_output)+ "\nand got:\n" + str(contact_id))
elif (elapsed_time >= time_threshold):
    errors.append("Instance FAIL: str(contact) time limit exceeded: " + str(elapsed_time))

#Contact class
succeed = False
output = False
expected_output = "VALUES(Smith,Hannah,98 e nowhere,eugene,oregon,97212,5555555555,hus@uoregon.edu)"
start_time = time.clock()
try:
    contact_id = person.to_dao()
    succeed = True
    output = (type(contact_id) == type(expected_output)) and contact_id == expected_output
except:
    errors.append("Method Test FAIL: contact.to_dao()")
end_time = time.clock()
elapsed_time = end_time - start_time
if (output == True and succeed and elapsed_time < time_threshold):
    successes.append("Method Test SUCCESS: contact.to_dao()")
elif (output == False):
    errors.append("Method Test FAIL: contact.to_dao() produces bad output.\nExpected:\n"+ str(expected_output)+ "\nand got:\n" + str(contact_id))
elif (elapsed_time >= time_threshold):
    errors.append("Instance FAIL: contact.to_dao() time limit exceeded: " + str(elapsed_time))

#Contact class
succeed = False
output = False
expected_output = "Smith\tHannah\t98 e nowhere\teugene\toregon\t97212\t5555555555\thus@uoregon.edu\n"
start_time = time.clock()
try:
    contact_id = person.to_tsv()
    succeed = True
    output = (type(contact_id) == type(expected_output)) and contact_id == expected_output
except:
    errors.append("Method Test FAIL: contact.to_tsv()")
end_time = time.clock()
elapsed_time = end_time - start_time
if (output == True and succeed and elapsed_time < time_threshold):
    successes.append("Method Test SUCCESS: contact.to_tsv()")
elif (output == False):
    errors.append("Method Test FAIL: contact.to_tsv() produces bad output.\nExpected:\n"+ str(expected_output)+ "\nand got:\n" + str(contact_id))
elif (elapsed_time >= time_threshold):
    errors.append("Instance FAIL: contact.to_tsv() time limit exceeded: " + str(elapsed_time))


print("\nUnit Test Complete. Results:")
print("\nErrors: " + str(len(errors)))
for error in errors:
    print(error)
print("\nWarnings: " + str(len(warnings)))
for warning in warnings:
    print(warning)
print("\nSuccesses: " + str(len(successes)))
for success in successes:
    print(success)