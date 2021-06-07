"""
__author__ = Yufeng Liu
student number = 44443115
__email__ = yufeng.liu1@uqconnect.edu.au
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

def physical_characteristics_question(question, answer1, answer2, answer3):
    print(question)
    print(" 1)" + answer1)
    print(" 2)" + answer2)
    print(" 3)" + answer3)
    response = input("Please enter your answer: ")
    if response == "1":
        print()
        return answer1
    elif response == "2":
        print()
        return answer2
    elif response == "3":
        print()
        return answer3
    else:
        print("That is not a valid selection. Please try again.\n")
        return physical_characteristics_question(question, answer1, answer2, answer3)


def personality_question(question):
    print(question)
    selections = '  1) Yes\n' \
                 '  2) Most of the time\n' \
                 '  3) Neutral\n' \
                 '  4) Some times\n' \
                 '  5) No'
    print(selections)
    answer = input("Please enter your answer: ")
    if answer == "1" or answer == "2" or answer == "3" or answer == "4" or answer == "5":
        print()
        return answer
    else:
        print("That is not a valid selection. Please try again.\n")
        return personality_question(question)


def match(gender, sexual_pref, height, height_pref, personality_score):
    best = None
    list1_best_difference = 100
    list2_best_difference = 100
    list3_best_difference = 100
    list4_best_difference = 100
    name_list1 = []
    name_list2 = []
    name_list3 = []
    name_list4 = []
    while potential_partners.available():
        # guarantees that the genders and gender preferences of the user
        if gender == potential_partners.get_sexual_pref() and sexual_pref == potential_partners.get_gender():
            # calculate the gap between score of
            difference = abs(personality_score - potential_partners.get_personality_score())

            name = potential_partners.get_name()
            # requirement both satisfied first
            if height_pref == potential_partners.get_height() and height == potential_partners.get_height_pref():
                if difference < list1_best_difference:
                    list1_best_difference = difference
                    name_list1.insert(0, name)
                else:
                    name_list1.append(name)
            elif height_pref == potential_partners.get_height() and height != potential_partners.get_height_pref():
                if difference < list2_best_difference:
                    list2_best_difference = difference
                    name_list2.insert(0, name)
                else:
                    name_list2.append(name)
            elif height_pref != potential_partners.get_height() and height == potential_partners.get_height_pref():
                if difference < list3_best_difference:
                    list3_best_difference = difference
                    name_list3.insert(0, name)
                else:
                    name_list3.append(name)
            else:
                # both not equal
                if difference < list4_best_difference:
                    list4_best_difference = difference
                    name_list4.insert(0, name)
                else:
                    name_list4.append(name)
    if len(name_list1) > 0:
        # return the name of the first one found
        best = name_list1[0]
    elif len(name_list2) > 0:
        # return the name of the first one
        best = name_list2[0]
    elif len(name_list3) > 0:
        # return the name of the first one
        best = name_list3[0]
    elif len(name_list4) > 0:
        best = name_list4[0]
    return best


def main():
    print('Welcome to PyMatch\n')

    name = input('Please enter your name:')  # get_user_name
    print("\nHi", name + ".")

    gender = physical_characteristics_question("What is your gender?", "male", "female",
                                               "other")
    sexual_pref = physical_characteristics_question("What is your sexual preference?", "male", "female",
                                                    "other")
    height = physical_characteristics_question("What is your height?", "tall", "medium",
                                               "short")
    height_pref = physical_characteristics_question("What height do you prefer your partner to be?", "tall", "medium",
                                                    "short")
    print("\nWe will now ask you some questions to try to determine your personality type.")

    personality_answer1 = personality_question("Do you find it easy to introduce yourself to other people?")
    personality_answer2 = personality_question("Do you usually initiate conversations?")
    personality_answer3 = personality_question("Do you often do something out of sheer curiosity?")
    personality_answer4 = personality_question(
        "Do you prefer being out with a large group of friends rather than spending time on your own?")
    personality_score = (int(personality_answer1) + int(personality_answer2) + int(personality_answer3) + int(
        personality_answer4)) * 2  # calculate the personality test score

    print("Your personality score is", personality_score)

    print(
        "\nThank you for answering all the questions. We have found your best match from our database and hope that "
        "you enjoy getting to know each other. Your best match is:")
    print(match(gender, sexual_pref, height, height_pref, personality_score))


if __name__ == '__main__':
    main()

# therefore, the program can run with the command prompt when you open your file (instead of editing with IDLE and
# running through the python shell)
