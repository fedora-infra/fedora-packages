# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box_url = "https://download.fedoraproject.org/pub/fedora/linux/releases/25/CloudImages/x86_64/images/Fedora-Cloud-Base-Vagrant-25-1.3.x86_64.vagrant-libvirt.box"
  config.vm.box = "f25-cloud-libvirt"
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.synced_folder ".", "/vagrant", type: "sshfs"
  # Ansible needs the guest to have these
  config.vm.provision "shell", inline: "sudo dnf install -y libselinux-python python2-dnf"

  config.vm.provision "ansible" do |ansible|
      ansible.playbook = "devel/ansible/playbook.yml"
  end
end
