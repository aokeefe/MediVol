MediVol
=======
Things to download (Windows):
* VirtualBox https://www.virtualbox.org/
* Vagrant http://www.vagrantup.com/
* git client http://git-scm.com/downloads

Steps
* Once you have completed all of the downloads, start by opening up th egit bash client
* navigate to the directory that you wish to store the project
* copy 'git clone https://github.com/MikeLentini/MediVol.git' into the git bash terminal, this will copy all of the projects code into the directory
* type 'vagrant up' into the terminal, this will download the virtual box image, start up the vm, initalize the vm to have all the nessessary programs, and start the server
* in your browser go to localhost:8888
* you can now view the current version of the website

Important Urls
=======
* localhost:8888/admin - Opens the admin panel
* localhost:8888/inventory/create - The create box page
* localhost:8888/inventory/view_box_info/<boxid> - View a box info
* localhost:8888/inventory/view_box_info/barcode/<barcode> - View a box info by its barcode
