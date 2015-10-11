import time
import subprocess
import glob
#garrett , hannah , josh , majeed , max
successes = []
warnings = []
errors = []
time_threshold = 0.5

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


print("\nErrors: " + str(len(errors)))
for error in errors:
    print(error)
print("\nWarnings: " + str(len(warnings)))
for warning in warnings:
    print(warning)
print("\nSuccesses: " + str(len(successes)))
for success in successes:
    print(success)