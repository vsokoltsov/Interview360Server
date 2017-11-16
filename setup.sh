PYTHON_VERSION=3.5.2
JAVA_VERSION=jdk-8u131-linux-x64.rpm
sudo yum -y update

# PYTHON 3.5.2
sudo yum install -y  gcc gcc-c++ make git patch openssl-devel zlib-devel readline-devel sqlite-devel bzip2-devel nginx wget
git clone git://github.com/yyuu/pyenv.git ~/.pyenv
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'alias pm="python manage.py"' >> ~/.bashrc
echo 'alias activate_env="source venv/bin/activate"' >> ~/.bashrc

pyenv install $PYTHON_VERSION
pyenv global $PYTHON_VERSION
pip install --upgrade pip
pip install virtualenvwrapper
git clone https://github.com/yyuu/pyenv-virtualenvwrapper.git ~/.pyenv/plugins/pyenv-virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
eval "$(pyenv init -)"
pyenv virtualenvwrapper
mkvirtualenv interview360
echo 'pyenv virtualenvwrapper' >> ~/.bashrc
echo 'workon interview360' >> ~/.bashrc

cd ~

sudo yum -y install postgresql-server postgresql-contrib postgresql-devel curl
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo su postgres -c 'psql -c "CREATE USER vagrant WITH PASSWORD '"'"'vagrant'"'"' SUPERUSER;"'
sudo su postgres -c 'psql -c "CREATE DATABASE interview_manager;"'
sudo su postgres -c 'psql -c "GRANT ALL PRIVILEGES ON DATABASE interview_manager TO vagrant;"'

# ERLANG
cd ~
wget http://packages.erlang-solutions.com/erlang-solutions-1.0-1.noarch.rpm
sudo rpm -Uvh erlang-solutions-1.0-1.noarch.rpm
sudo yum -y install erlang

# RABBIT MQ

cd ~
wget https://www.rabbitmq.com/releases/rabbitmq-server/v3.6.1/rabbitmq-server-3.6.1-1.noarch.rpm
sudo rpm --import https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
sudo yum -y install rabbitmq-server-3.6.1-1.noarch.rpm
sudo systemctl start rabbitmq-server.service
sudo systemctl enable rabbitmq-server.service

sudo rabbitmqctl add_user admin admin
sudo rabbitmqctl set_user_tags admin administrator
sudo rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"

# JAVA
wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" \
"http://download.oracle.com/otn-pub/java/jdk/8u131-b11/d54c1d3a095b4ff2b6607d096fa80163/$JAVA_VERSION"
sudo yum -y localinstall $JAVA_VERSION
rm $JAVA_VERSION

#ELASTICSEARCH
cd ~
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.3.rpm
sha1sum elasticsearch-5.6.3.rpm
sudo rpm --install elasticsearch-5.6.3.rpm
sudo service elasticsearch start
sudo service elasticsearch enabled

#KIBANA
wget https://artifacts.elastic.co/downloads/kibana/kibana-5.6.3-x86_64.rpm
sha1sum kibana-5.6.3-x86_64.rpm
sudo rpm --install kibana-5.6.3-x86_64.rpm
sudo service kibana start

#MAKE ELASTICSEARCH AND KIBANA VISIBLE FROM THE VM
sudo bash -c "echo 'network.host: 0.0.0.0' >> /etc/elasticsearch/elasticsearch.yml"
sudo bash -c "echo 'server.host: 0.0.0.0' >> /etc/kibana/kibana.yml"
sudo bash -c "echo 'elasticsearch.url: http://localhost:9200' >> /etc/kibana/kibana.yml"
