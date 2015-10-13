import time
import subprocess
import glob
#garrett , hannah , josh , majeed , max
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
        if "#" in line:
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

#Contact module
succeed = False
start_time = time.clock()
try:
    out = subprocess.check_output(['python',"addressbook.py"])
    if len(out) == 0:
        succeed = True
    import addressbook
except subprocess.CalledProcessError as e:
    errors.append("Import FAIL: addressbook.py "+str(e))

end_time = time.clock()
elapsed_time = end_time - start_time
if (succeed and elapsed_time < time_threshold):
    successes.append("Import SUCCESS: addressbook.py")
elif (elapsed_time >= time_threshold):
    errors.append("Import FAIL: addressbook.py time limit exceeded: " + str(elapsed_time))


print("Beginning contact instantiation")
#Contact class
succeed = False
start_time = time.clock()
try:
    person = contact.Contact(['Hannah','Smith','98 e nowhere','eugene','oregon','97212','5555555555','hus@uoregon.edu'])
    succeed = True
except:
    errors.append("Instance Creation FAIL: Contact")
end_time = time.clock()
elapsed_time = end_time - start_time
if (succeed and elapsed_time < time_threshold):
    successes.append("Instance SUCCESS: Contact")
elif (elapsed_time >= time_threshold):
    errors.append("Instance FAIL: Contact time limit exceeded: " + str(elapsed_time))

print("Beginning contact method testing")
#Contact class
succeed = False
output = False
expected_output = 39278464
start_time = time.clock()
try:
    id = id(person)
    succeed = True
    output = type(id) == long
except:
    errors.append("Method Test FAIL: id(contact)")
end_time = time.clock()
elapsed_time = end_time - start_time
if (output == True and succeed and elapsed_time < time_threshold):
    successes.append("Method Test SUCCESS: id(contact)")
elif (output == False):
    errors.append("Method Test FAIL: id(contact) produces bad output. Expected: "+ str(expected_output)+ " and got: " + str(id))
elif (elapsed_time >= time_threshold):
    errors.append("Instance FAIL: id(ontact) time limit exceeded: " + str(elapsed_time))


#Contact class
succeed = False
output = False
expected_output = 'Hannah,Smith,98 e nowhere,eugene,oregon,97212,5555555555,hus@uoregon.edu'
start_time = time.clock()
try:
    id = str(person)
    succeed = True
    output = (type(id) == type(expected_output)) and id == expected_output
except:
    errors.append("Method Test FAIL: str(contact)")
end_time = time.clock()
elapsed_time = end_time - start_time
if (output == True and succeed and elapsed_time < time_threshold):
    successes.append("Method Test SUCCESS: str(contact)")
elif (output == False):
    errors.append("Method Test FAIL: str(contact) produces bad output. Expected: "+ str(expected_output)+ " and got: " + str(id))
elif (elapsed_time >= time_threshold):
    errors.append("Instance FAIL: str(contact) time limit exceeded: " + str(elapsed_time))

print("Beginning address book instantiation")
#Address Book class
succeed = False
start_time = time.clock()
try:
    book = addressbook.AddressBook("Cats")
    succeed = True
except:
    errors.append("Instance Creation FAIL: AddressBook")
end_time = time.clock()
elapsed_time = end_time - start_time
if (succeed and elapsed_time < time_threshold):
    successes.append("Instance SUCCESS: AddressBook")
elif (elapsed_time >= time_threshold):
    errors.append("Instance FAIL: AddressBook time limit exceeded: " + str(elapsed_time))


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