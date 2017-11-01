Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
  config.vm.provider "virtualbox" do |v|
    v.name = "interview_manager"
  end
  config.vm.network "forwarded_port", host_ip: "127.0.0.1", guest: 8080, host: 8080
  config.vm.network "forwarded_port", host_ip: "127.0.0.1", guest: 5555, host: 5555
  config.vm.network "forwarded_port", host_ip: "127.0.0.1", guest: 15672, host: 15672
  config.vm.network "forwarded_port", host_ip: "127.0.0.1", guest: 9200, host: 9200
  config.vm.synced_folder "./", "/home/vagrant/im"
  config.vm.provision "shell", privileged: false, path: "./setup.sh"
end
