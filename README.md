https://fedorahosted.org/fedoracommunity/wiki/Development

Note: Some more dependencies to be installed:-

    $ sudo dnf install python-webhelpers fedmsg pygobject3

    $ pip install gearbox

### Hacking with Vagrant

We have a simple vagrant setup for hacking on the fedora-packages app.

First, install Ansible, Vagrant, the vagrant-sshfs plugin, and the
vagrant-libvirt plugin from the official Fedora repos:

    $ sudo dnf install ansible vagrant vagrant-libvirt vagrant-sshfs

Now, from within main directory (the one with the Vagrantfile in it)
of your git checkout of fedora-pacakges, run the vagrant up command to provision
your dev environment:

    $ vagrant up

When this command is completed (it may take a while) you will be able to
ssh into your dev VM with vagrant ssh and then run the c
ommand to start the fedora-packages server:

    $ vagrant ssh
    [vagrant@localhost ~]$ pushd /vagrant/; gearbox serve;

Once that is running, simply go to http://localhost:8080/ in your browser on
your host to see your running fedora-packages test instance.
