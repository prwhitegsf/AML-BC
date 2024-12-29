from setup.modules.setup_modules import remove_users_by_time, remove_all_users

dbname = input("Please enter the database name: ") 

prompt = "To remove all users, enter 'a': \nTo remove by time, enter 't': "

sel = input(prompt)

if sel == 'a':
    rows = remove_all_users(dbname)
    print(f'Removed {rows} rows from User')
elif sel == 't':
    minutes = input("Enter expiration in minutes: ")
    remove_users_by_time(dbname, minutes)
else:
    print("invalid selection, please try again")


