global_variable = 0

def change_global():
    global global_variable  # Declare global_variable as global
    global_variable = 10    # Modify the global variable

print("Before:", global_variable)
change_global()
print("After:", global_variable)