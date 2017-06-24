PYTHON_VERSION=3.5.2

sudo yum -y update

# PYTHON 3.5.2
sudo yum install -y  gcc gcc-c++ make git patch openssl-devel zlib-devel readline-devel sqlite-devel bzip2-devel
git clone git://github.com/yyuu/pyenv.git ~/.pyenv
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
pyenv install $PYTHON_VERSION
pyenv global $PYTHON_VERSION
pip install --upgrade pip
pip install virtualenvwrapper

sudo yum -y install postgresql-server postgresql-contrib postgresql-devel curl
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
