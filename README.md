## Official utilities for the CAPE dataset

#### Description

This repository contains the scripts to facilitate using the [CAPE dataset](https://cape.is.tue.mpg.de/dataset), introduced in our CVPR 2020 paper [Learning to Dress 3D People in Generative Clothing](https://arxiv.org/abs/1907.13615). 

The CAPE dataset is a collection of 3D meshes of clothed humans in motion. It consists of 15 subjects, 610 sequences,  148K frames in total. The data is captured with a hi-res 4D body scanner, and registered to the topology of the [SMPL body model](https://smpl.is.tue.mpg.de). Thanks to its consistent mesh topology, the data is readily applicable for various machine learning tasks, such as explicit / implicit clothing modeling, 3D dynamic shape modeling, graph neural networks, etc.

We have attached here a synthetic example that emulates the ones CAPE dataset. For more details and to download the entire dataset, please visit our [project website](https://cape.is.tue.mpg.de/).

![CAPE dataset examples](./images/cape_dataset.png)

#### Dependencies

- numpy
- trimesh
- tqdm

They can be installed by  `pip3 install -r requirements.txt`. The code has been tested on Ubuntu 18.04 and python 3.6.

##### Optional Dependencies 

For visualizing data as videos:
- The [PSBody Mesh package](https://github.com/MPI-IS/mesh). Go to "releases" there and install version 0.3 (not the latest 0.4).
- ffmpeg: for saving the visualization into videos

#### Usage

##### Extract the meshes out of the compressed data

```python
python dataset_utils.py --subj <subject> --seq_name <sequence_name> --option posed --extract
```

##### Render the extracted meshes into videos (requires psbody.mesh)

```python
python dataset_utils.py --subj <subject> --seq_name <sequence_name> --option posed --vis
```

##### Visualize the clothing displacements (of a single frame)

```python
python dataset_utils.py --subj <subject> --seq_name <sequence_name> --option posed --demo_disps
```

#### License

Software Copyright License for **non-commercial scientific research purposes**. Please read carefully the [terms and conditions](./LICENSE) and any accompanying documentation before you download and/or use the CAPE data and software, (the "Dataset & Software"), including 3D meshes, pose parameters, scripts, and animations. By downloading and/or using the Model & Software (including downloading, cloning, installing, and any other use of this github repository), you acknowledge that you have read these terms and conditions, understand them, and agree to be bound by them. If you do not agree with these terms and conditions, you must not download and/or use the Model & Software. Any infringement of the terms of this agreement will automatically terminate your rights under this [License](LICENSE).

#### Citation:

If you find the CAPE dataset useful in your research, please consider citing our work:

```bibtex
@inproceedings{CAPE:CVPR:20,
  title = {Learning to Dress 3D People in Generative Clothing},
  author = {Ma, Qianli and Yang, Jinlong and Ranjan, Anurag and Pujades, Sergi and Pons-Moll, Gerard and Tang, Siyu and Black, Michael J.},
  booktitle = {Computer Vision and Pattern Recognition (CVPR)},
  month = jun,
  year = {2020},
  month_numeric = {6}
}
```



#### Contact

The code of this repository is implemented by [Qianli Ma](qma@tue.mpg.de). For questions, please contact cape@tue.mpg.de

For feature requests and feedbacks, please raise issues to this repository.
