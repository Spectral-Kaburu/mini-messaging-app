from .database import create_user, fetch_all_users, fetch_user_by_name

print("FETCHED ALL USERS:", fetch_all_users())
print("FETCHED USER:", fetch_user_by_name("lee"))
print("CREATED USER:", create_user("205893", "dad", "ps_hashh"))