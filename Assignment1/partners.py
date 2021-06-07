"""Support file for PyMatch (Assignment 1) in CSSE1001.

Reads the partner data from the database text file.
Stores the data in a list of partners.
Provides a mechanism to iterate over the partners and
extract the details of each partner.

Richard Thomas, 03/03/2017
"""


class Partner:
    """Represents a single potential partner from the database."""

    def __init__(self, first_name, last_name, gender, sexual_pref,
                 height, height_pref, personality_score):
        """Initialise the partner with their personal details."""
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.sexual_pref = sexual_pref
        self.height = height
        self.height_pref = height_pref
        self.personality_score = personality_score

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_gender(self):
        return self.gender

    def get_sexual_pref(self):
        return self.sexual_pref

    def get_height(self):
        return self.height

    def get_height_pref(self):
        return self.height_pref

    def get_personality_score(self):
        return self.personality_score


class Partners:
    """Provides access to partner details from the database."""

    def __init__(self):
        """Read the partner data from the database."""
        self.partners = []  # List of partners
        self.partners_read = -1  # Number of partners read from the list

        with open("database.txt", "r") as file:
            file_contents = file.readlines()

        for line in file_contents:
            person = line.split()
            self.partners.append(Partner(person[0], person[1], person[2], person[3],
                                         person[4], person[5], int(person[6])))

    def available(self):
        """Indicates if there is another partner available to process.

            This function must be called as an initial test when
            iterating over the list of partners.
            See the example of usage in: partners_example.py.
        """
        self.partners_read += 1
        return self.partners_read < len(self.partners)

    def reset_iterator(self):
        """Resets the iteration counter.

            Allows processing of list of partners to be restarted
            from the begining of the list.
            This function does not need to be used in assignment 1,
            but some people may find it useful.
        """
        self.partners_read = -1  # Reset count of number of partners read

    # Utility methods to read each part of a partner's details.
    def get_first_name(self):
        return self.partners[self.partners_read].get_first_name()

    def get_last_name(self):
        return self.partners[self.partners_read].get_last_name()

    def get_name(self):
        return (self.partners[self.partners_read].get_first_name()
                + " "
                + self.partners[self.partners_read].get_last_name())

    def get_gender(self):
        return self.partners[self.partners_read].get_gender()

    def get_sexual_pref(self):
        return self.partners[self.partners_read].get_sexual_pref()

    def get_height(self):
        return self.partners[self.partners_read].get_height()

    def get_height_pref(self):
        return self.partners[self.partners_read].get_height_pref()

    def get_personality_score(self):
        return self.partners[self.partners_read].get_personality_score()


# Check if an attempt is made to execute this module and output error message
if __name__ == "__main__":
    print("This module provides utility functions for Partners",
          "and is not meant to be executed on its own.")
