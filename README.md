# Multi-Task Batch RL with Metric Learning

This repository contains the code accompanying the paper ```Multi-Task Batch Reinforcement Learning with Metric Learning```.

Codes for the full model algorithm and each of the baseline and ablation can be found under their corresponding folder.

# Reproducing Results

To reproduce the results, we provide the collected transition buffers for each of the training tasks, the trained BCQ models and ensemble predictors in the [Google Drive](https://drive.google.com/file/d/1YqskGjcPURHs-Al3wGs4ddVKBcw6np5q/view?usp=sharing), i.e., the first phase of training pipeline. Please download all the data and put them in the ```data_and_trained_models``` folder. Otherwise you should be careful when running the following experiments and you should correctly specify the locations. After downloading the files from Google Drive, use the command below to unzip the file:

```
tar -xvf data_and_trained_model.tar.gz
```

Experiments are configured via `.py` configuration files located in `./configs`. To reproduce an experiment, you can first go to the corresponding folder, and then run the following commands:

```
python main.py --config=DOMAIN_NAME
```

Make sure to check the `configs` folder before running any experiment. For example, if you would like to reproduce the results of ``AntDir`` with the full model, then you should do 

```
cd full_model
python main.py --config=ant-dir
```

An exception is applied when reproducing results of `PEARL` under the batch settings. Here you should do

```
cd batch_pearl
python launch_experiment.py './configs/DOMAIN_NAME.json'
```

For example, if you would like to reproduce the results of ``AntDir`` with PEARL, then you should do 

```
cd batch_pearl
python launch_experiment.py './configs/ant-dir.json'
```

# Running Experiments

If you would like to generate the results for the training phase, first you can go to the ``oac-explore`` folder and run the following command to obtain the training buffers. Note that the list of ``goal_id`` varies from domain to domain:

```
python main.py --config=DOMAIN_NAME --goal=GOAL_ID
```

Then you can go the the ``BCQ`` folder and run the following command to extract task-specific results:

```
python main.py --config=DOMAIN_NAME --goal=GOAL_ID
```

Simultaneously, you can get the reward prediction ensembles by going to the ``reward_prediction_ensemble`` and running

```
python main.py --config=DOMAIN_NAME
```

and can get the next state prediction ensembles by going to the ``transition_prediction_ensemble`` and running

```
python main.py --config=DOMAIN_NAME
```

Note that you should pay extra attention to ``--data_models_root``.

For software dependencies, please have a look inside the ```environment``` folder, you can create a conda environment with ```environment.yml```.

To create the conda environment, ```cd``` into the ```environment``` folder and run:

```
python install_mujoco.py
conda env create -f environment.yml
```

# Acknowledgement

This repository was based on [rlkit](https://github.com/vitchyr/rlkit), [oac-explore](https://github.com/microsoft/oac-explore), [BCQ](https://github.com/sfujim/BCQ/tree/master/continuous_BCQ) and [PEARL](https://github.com/katerakelly/oyster).

The codes to generate the transition batch for each task and codes to accelerate conventional SAC are obtained modifying the codes as provided in the [oac-explore](https://github.com/microsoft/oac-explore).

The Batch RL part of this paper is based on the codes as provided in the [BCQ](https://github.com/sfujim/BCQ/tree/master/continuous_BCQ).

The codes for `batch_pearl` are obtained by modifying [PEARL](https://github.com/katerakelly/oyster).

The codes for each environment files in the folder ``env`` are adapted from [PEARL](https://github.com/katerakelly/oyster). Note that the ``rand_param_envs`` in each folder is copied from [rand_param_envs](https://github.com/dennisl88/rand_param_envs/tree/4d1529d61ca0d65ed4bd9207b108d4a4662a4da0).
