# License Reader with YoloV5 weight pre-trained by myself

## [Install guide](#install_guide)
#### 1. [Project install](#project_install)
#### 2. [PyTorch install Mac M1](#torch_mac_install)

## [Usage guide](#usage_guide)
#### 1. [How to run server](#django_run)
#### 2. [API documentation](#api_docs)

---

<a name="install_guide"></a>

<a name="project_install"><h2>How to install project</h2></a>

```shell
git clone https://github.com/Land-Maze/License_Reader_YoloV5
cd ./License_Reader_YoloV5
# If user doesn't have write permission use sudo
sh install.sh
```

---

<a name="torch_mac_install"><h2>How to install **torch** on *Mac M1*</h2></a>

### Install brew and dependency

```shell
# Follow prompts if there will be
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install wget

# If xcode tools not installed
xcode-select --install
```

### Install miniconda

```shell
# Create and download script for miniconda install
mkdir tmp || echo "Can't create directory tmp. If directory exists, simply ignore"
cd tmp
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-MacOSX-arm64.sh -O miniconda.install.sh

# Checking of hash sum
test "$( shasum -a 256 miniconda.install.sh )" != "4bd112168cc33f8a4a60d3ef7e72b52a85972d588cd065be803eb21d73b625ef  miniconda.install.sh"
if (( $? == 1 ))
then
  echo "Checksum is OK"
else
  echo "Checksum is BAD. Exiting"
  return
fi

# Install proccess
# It may ask for agreement
sh miniconda.install.sh -p $HOME/miniconda
```

### Conda configuration

```shell
# Creating conda enviroment
conda create -n torch python=3.9

# Activating conda source
conda activate torch

# Installing deps
conda install pytorch torchvision torchaudio -c pytorch-nightly
```

---

<a name="usage_guide"></a>

<a name="django_run"><h2>How to run server</h2></a>

```shell
# In root folder
sudo python manage.py runserver 3000 --noreload
```

<a name="api_docs"><h2>API docs</h2></a>

### **UNDER CONSTRUCT**