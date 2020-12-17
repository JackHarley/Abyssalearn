# Abyssalearn

Database
--------------------------------
A copy of `database.db` is maintained in `data/database.db`, please avoid committing any of your changes to this file. 

You can discard your local changes with `git reset --hard HEAD` before pulling. N.B. Make sure you have committed your own changes before running this command as it will wipe out any uncommitted changes from the filesystem!

Installation
--------------------------------
1. Install `pipenv` from your distribution package manager or with `pip install pipenv`
2. Run `pipenv install --ignore-pipfile` to install dependencies

Usage
--------------------------------
Run `pipenv shell` and then use any of the following features:

* `python main.py scrape` - Scrapes any new contract data from the EVE servers
* `python main.py summary` - Print a summary of the data in the database
* `python main.py random 47702` - Pull a random module with type ID 47702 (abyssal stasis webifier) and print its pricing/attributes
* `python main.py ridgereg|lassoreg-crossval 47702 0.001` - Run Ridge|Lasso Regression with type ID 47702 and alpha=0.001 and print out the mean squared error of 5-Fold cross-validation
* `python main.py linreg 47702` - Run Linear Regression with type ID 47702 and print out the mean squared error of 5-Fold cross-validation
* `python main.py ridgereg-crossval|lassoreg-crossval 47702` - Run Ridge|Lasso Regression with type ID 47702 and test alpha in [0.0001, 0.001, 0.01, 0.1, 1] using 5-Fold cross-validation
* `python main.py poly_reg 47702` - Run Linear Regression with type ID 47702 and polynomial features with degrees in ranges `[1,2,3,4,5,6]` and print out the mean squared error of 5-Fold cross-validation
