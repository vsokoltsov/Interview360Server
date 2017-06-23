Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
  config.vm.provision "shell", privileged: false, path: "./postgres.sh"
end
