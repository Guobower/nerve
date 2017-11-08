# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrant.configure version 2.
Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.ssh.username = "vagrant"
  config.ssh.password = "vagrant"
  config.ssh.insert_key = false

  config.vm.provider "virtualbox" do |vb|
      vb.gui = false
      vb.memory = "1000"
      vb.cpus = 1
  end


  config.vm.define "client01" do |c01|
      c01.vm.network :"private_network", ip: "192.168.100.101"
      c01.vm.provision "shell", path: "bootstrap.sh"
  end

  config.vm.define "client02" do |c02|
      c02.vm.network :"private_network", ip: "192.168.100.102"
      c02.vm.provision "shell", path: "bootstrap.sh"
  end

  config.vm.define "mailcatcher" do |mailcatcher|
      mailcatcher.vm.network :"private_network", ip: "192.168.100.200"
      config.vm.network :forwarded_port, host: 1080, guest: 1080
      config.vm.network :forwarded_port, host: 1025, guest: 1025

      mailcatcher.vm.provision "shell", path: "mailcatcher.sh"
  end

end
