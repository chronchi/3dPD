# make directory to download, build and make cgal and optiperslp. This requires
# root privileges and a debian/ubuntu machine. 

export HOME=/home

apt update1
apt install cmake 
apt install make

mkdir installation

cd installation

# install conda to download bokeh 
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
mkdir ../miniconda3
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
# activate base 
conda activate base

# install bokeh 
conda install bokeh

# install cgal 
wget https://github.com/CGAL/cgal/releases/download/releases%2FCGAL-4.12/CGAL-4.12.tar.xz
tar -xf CGAL-4.12.tar.xz 
cd CGAL-4.12
mkdir cgal_build 
cd cgal_build
cmake ..
make 
sudo make install

# install boost 
sudo apt-get install libboost-all-dev

# install GLPK
sudo apt-get install glpk-utils libglpk-dev libglpk40

# install optiperslp 
cd ../..
wget https://bitbucket.org/remere/optiperslp/downloads/optiperslp-1.2.1.tar.gz
tar -xf optiperslp-1.2.1.tar.gz
cd optiperslp-1.2.1
./configure
make
sudo make install 

# update links and shared libraries 
ldconfig 
