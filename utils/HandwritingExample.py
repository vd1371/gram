'''
This is an example of the handwriting that MUST be followed for commiting to the master branch
Otherwise, it will simply not be accepted

Useful resources:
[1] Transforming Code into Beautiful, Idiomatic Python: https://www.youtube.com/watch?v=OSGv2VnC0go

'''

import time
# Definition of global variables, Please kindly refer to RULE NO.9
ANALYSIS_DONE, FIRST_GLOBAL_VARIABLE = False, 'I am the first global variable'


# RULE NO.0: Each line and section of the code needs a comment to increase legiblity. It must clearly describe everything so one could possibly understand section's ultimate aim without reading the code

# RULE NO.1:  Attributes and methods must have a clear name which could represent their nature. Avoid using
# ...variable names such as a = 10, c = False.

# RULE NO.2: Name classes and files in PascalCase form (like HandwritingExample), example:
class ExampleClass:
	def __init__(self):
		# This is an inner method, please kindly refer to RULE No.4
		self._inner_method()

		# This is a parameter to show the usage of RULE No. 12
		self.foo_param = 10
		pass

	# RULE NO.3: name the methods of the class in lower_case form with "_" as seperator
	def foo_method(self):
		pass

	# RULE NO.4 : begin the name the mehtods and parameters that are used in the inner scope of the class with "_"
	def _inner_method(self):
		# Methods and parameters inside the parameter are only and only used inside the class and will not have any effect, will not be called from outside, will not print anything
		self._inner_param = 'I am inner parameter, I am used for calculations inside the class and will not be accessed from outside of the class'
	
	# RULE NO.5 : Always use f_string, DO NOT USE other forms of strings and variables:
	def example_of_f_string(self):
		print (f"This is a correct example to show f_string {time.time().4f}")
		# This is wrong print ("Wrong version 1, %s" %(self._inner_param))

	# RULE NO. 6: use enumerate and zip if necessary
	def test_of_enumerate_and_zip(self):
		# creating two example lists
		list1 = ['a', 'b', 'c']
		list2 = [10, 20, 30]

		# zip example:
		for char, val in zip (list1, list2):
			print (char, val)

		# The output is sth like this:
		'''
		a 10
		b 20
		c 30
		'''

		# enumerate example:
		for i, char in enumerate(list1):
			print (i, char)

		# The output is sth like this:
		'''
		0 a
		1 b
		2 c
		'''
	
	# This is to show the usage of RULE No. 12
	def set_foo(self, val):
		# Sets the value of class attribute foo_param
		self.foo_param = val



# RULE NO.7: name a function not belonging to a class in camelCase for
def greetPerson(name):
	# RULE NO.8: Each function and method must have a thorough description of the input arguments and their types, the outputs and their types, what is does, and probably an example
	
	# Following is the example of the description of this function
	'''
	This function greets a person
	:params: name : string
	:output params: None
	example:
	--> greetPerson("Alex")

	Hello Alex
	'''
	print (f"Hello {name}")

# RULE NO.8: if you need to test what you have written, ALWAYS write it after if __name__ == '__main__':
if __name__ == '__main__':

	# RULE NO.9: Avoid hardcoding and using integers, strings, and booleans in the code. Always use global variable written in UPPER_CASE_FROM
	while not ANALYSIS_DONE:
		print (FIRST_GLOBAL_VARIABLE)
		# it will print it forever

	# RULE NO.10: Use Pandas and numpy in an eficient way. Sub-optimal usage of these libraries are not acceptable
	# RULE NO.11: The code must be written in a way that the output is created in the fastest possible way. Sub-optimal algorithms which 
	# ... consumes a lot of memory, cpu and time are not acceptable
	
	# RULE NO. 12: Do not access or set the attributes of a class out of the class
	