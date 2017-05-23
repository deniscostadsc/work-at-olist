Olist API
=========

Project running at [heroku](https://warm-citadel-37739.herokuapp.com/)

Used tools in the project

- Vim
- Vagrant
- VirtualBox
- Ubuntu (VM)
- OSx

To run the project, if you don't use vagrant, you need to have installed:

- PostgreSQL
- Virtualenv

If you want to use Vagrant you need to have installed:

- VirtualBox
- Vagrant

To setup variables, need to create a .env file. You can do it based on
local.env.

To create the VM, run:

```
make create-vm
```

To run lint check, test and coverage report  just run:

```
make build
```

And to run the project just run:

```
make runserver
```
