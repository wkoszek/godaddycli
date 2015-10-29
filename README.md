# Command Line Interface to GoDaddy.com based on PyGoDaddy Library

This is a simple CLI for GoDaddy. It supports listing of all record types
from all domains, and deleting and updating of A records.

# How to install

Version 0.1.2 you can get from `pip`:

	pip install godaddycli

# How to use

Once you install the CLI, using is very simple:

	godaddycli

When started 1st time will prompt for the user and the password.
User has a way to save the credentials. Warning: it's stored in
a clear-text form (unencrypted). When stored, file `~/.godaddyclirc`
is used.

To list domains (`--list` is optional):

	godaddycli --list

To update a domain:

	godaddycli --update test.sample.com --val 127.0.0.1

Will add record A of name `test.sample.com` and the value `127.0.0.1`

To delete:

	godaddycli --delete test.sample.com

# Author

- Wojciech Adam Koszek, [wojciech@koszek.com](mailto:wojciech@koszek.com)
- [http://www.koszek.com](http://www.koszek.com)
