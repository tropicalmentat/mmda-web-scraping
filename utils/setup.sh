# preliminaries from
# https://computingforgeeks.com/how-to-install-python-on-3-on-centos/
# install python dependencies
sudo yum -y update
sudo yum -y groupinstall "Development Tools"
sudo yum -y install openssl-devel bzip2-devel libffi-devel

# install centos sclo rh repository
sudo yum install centos-release-scl-rh

# install python 3.8 using software collections
# https://www.server-world.info/en/note?os=CentOS_7&p=python38

sudo yum --enablerepo=centos-sclo-rh -y install rh-python38