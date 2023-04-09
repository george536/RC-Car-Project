## Setting Up a Virtual Environment (Important)

1. Install the `virtualenv` package by running `pip install virtualenv` in your terminal.

2. Create a new virtual environment with the `--system-site-packages` flag by running `virtualenv venv --system-site-packages` in your terminal. This will create a new virtual environment named `venv` in your current directory, and it will include all of the packages that are installed system-wide.

3. Activate the virtual environment by running `source venv/bin/activate` in your terminal. This will activate the virtual environment and change your prompt to indicate that you are now working in the virtual environment.

That's it! You can now install additional packages using `pip` just like you would in a regular virtual environment. When you are finished working in the virtual environment, you can deactivate it by running the `deactivate` command in your terminal.
