# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.provision :shell, :path => "vagrant-setup/vagrant-setup.sh"
  config.vm.synced_folder ".", "/var/www"

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "ubuntu"

  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  # accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network :forwarded_port, guest: 3306, host: 8889
  config.vm.network :forwarded_port, guest: 80, host: 8888
end
