from selenium import webdriver
import time
import datetime
import os

# before you begin: navigate to a place you want to keep your completed assignments
# type 'mkdir completed_assignments'
# type 'cd completed_assignments'
# type 'mkdir [insert exact name of class here]'
# type 'cd [same name of class here]'
# type 'mv [path to assignment file] .'

site = 'https://canvas.disabroad.org/'
local_pass_file = '/Users/sejaldua/Desktop/cp.txt'
my_username = 'sejal.dua@tufts.edu'
submission_dir = '/Users/sejaldua/Desktop/DIS/completed_assignments'
submitted_dir = '/Users/sejaldua/Desktop/DIS/submitted_assignments'

def submit_assignment(file_tup, site=site, my_username=my_username, file=local_pass_file, submission_dir=submission_dir, submitted_dir=submitted_dir):

        
        driver = webdriver.Chrome()
        time.sleep(3)
        driver.get(site)

        # enter username
        id_box = driver.find_element_by_id('pseudonym_session_unique_id')
        id_box.send_keys(my_username)

        # get password from file
        with open(file, 'r') as f:
	        my_pass = f.read()

        # enter password
        pass_box = driver.find_element_by_id('pseudonym_session_password')
        pass_box.send_keys(my_pass)
        driver.find_element_by_css_selector('button').click()

        time.sleep(1)

        # find and click on list of courses
        courses_button = driver.find_element_by_id('global_nav_courses_link')
        courses_button.click()

        time.sleep(1)

        # click on the course for which you are submitting an assignment
        class_select = driver.find_element_by_link_text(file_tup[0])
        class_select.click()

        # click the 'Assignments' button
        assignment_button = driver.find_element_by_link_text('Assignments')
        assignment_button.click()

        folder = file_tup[0]

        time.sleep(2)

        # locate the specific assignment
        # note: this only works if your submission file is the name of the assignment + .xxx (file extension)
        file_name = file_tup[1]
        file_locator = file_name.split('.')[0]
        specific_assigment = driver.find_element_by_link_text(file_locator)
        specific_assigment.click()

        # click on the button to submit an assignment
        try:
                submit_assignment_button = driver.find_element_by_link_text('Submit Assignment')
        # if assignment has already been submitted
        except:
                print('Assignment already submitted, re-submitting')
                submit_assignment_button = driver.find_element_by_link_text('Re-submit Assignment')

        submit_assignment_button.click()

        # wait for the page to load
        time.sleep(2)

        # choose file button
        choose_file = driver.find_element_by_name('attachments[0][uploaded_data]')

        # Send the name of the file to the button
        file_location = os.path.join(submission_dir, folder, file_name)
        choose_file.send_keys(file_location)

        # click submit file button
        submit_assignment = driver.find_element_by_id('submit_file_button')
        submit_assignment.click()

        # Wait for the page
        time.sleep(2)

        # move the file to the submitted folder
        try:
                submitted_dir = os.path.join(submitted_dir, folder)
        except:
                os.chdir(submitted_dir)
                os.mkdir(folder)
                submitted_dir = os.path.join(submitted_dir, folder)
                
        submitted_file_name = 'Submitted ' + file_name

        submitted_file_location = os.path.join(submitted_dir, submitted_file_name)
       
        # print some updates to demonstrate successful submission
        print('{} Assignment for Class {} successfully submitted at {}.'.format(
        file_name, folder, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        print('Submitted assignment available at {}.'.format(submitted_file_location))

if __name__ == "__main__":

        # some variables that help this program serve my current needs right now
        # if you want to use this function to automate your Canvas submissions, 
        # just tweak the variables below with your information instead of mine

        # build a tuple of course name and submission file name
	dir_list = list(os.listdir(submission_dir))

	for directory in dir_list:
	    file_list = list(os.listdir(os.path.join(submission_dir, directory)))
	    if len(file_list) != 0:
	        file_tup = (directory, file_list[0])

	if len(file_tup) == 0:
		print('No files to submit')

	else:
		print('Assignment "{}" for "{}" found.'.format(file_tup[1], file_tup[0]))
		input('Press enter to proceed: ')
		submit_assignment(file_tup)