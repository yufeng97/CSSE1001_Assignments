"""This is a simple example of using the partners.py file.

The partners.py file allows you to retrieve each potential partner 
from the database. The one restriction is that you must finish getting
details of the potential partner before checking to see if there are
any more potential partners available.
"""

# The following statement gives you access to the code in the partners.py file.
import partners

# The following statement creates a variable that can access the potential partners.
potential_partners = partners.Partners()

# The following loop iterates over all of the potential partners in the database.
# Inside the loop the potential_partners variable is used to call functions
# that get the details of one potential partner.
# In your assignment you will need to implement a loop similar to this one
# and use the functions to access the attributes of each potential partner.
while potential_partners.available() :
    print(potential_partners.get_name())
    print(potential_partners.get_gender())
    print(potential_partners.get_sexual_pref())
    print(potential_partners.get_height())
    print(potential_partners.get_height_pref())
    print(potential_partners.get_personality_score())

print("\nFinished")    
