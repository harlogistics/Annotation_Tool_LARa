'''
Created on May 17, 2019

@author: fmoya
'''

from __future__ import print_function
import os
import logging

import platform
from modus_selecter import Modus_Selecter

import datetime


def configuration(dataset_idx, network_idx, output_idx, usage_modus_idx=0, dataset_fine_tuning_idx=0,
                  reshape_input=False, learning_rates_idx=0, name_counter=0, freeze=0, percentage_idx=0,
                  fully_convolutional=False, sacred=False):
    # Flags
    plotting = False

    # Options
    dataset = {0: 'mocap', 1: 'mbientlab', 2: 'virtual', 3: 'mocap_half', 4: 'virtual_quarter', 5: 'mocap_quarter',
               6: 'mbientlab_50_p', 7: 'mbientlab_10_p', 8: 'mbientlab_50_r', 9: 'mbientlab_10_r',
               10: 'mbientlab_quarter', 11: 'motionminers_real'}
    network = {0: 'cnn', 1: 'lstm', 2: 'cnn_imu'}
    output = {0: 'softmax', 1: 'attribute'}
    usage_modus = {0: 'train', 1: 'test', 2: 'evolution', 3: 'train_final', 4: 'train_random', 5: 'fine_tuning'}

    # Dataset Hyperparameters
    NB_sensor_channels = {'mocap': 126, 'mbientlab': 30, 'virtual': 126, 'mocap_half': 126, 'virtual_quarter': 126,
                          'mocap_quarter': 126, 'mbientlab_50_p': 30, 'mbientlab_10_p': 30, 'mbientlab_50_r': 30,
                          'mbientlab_10_r': 30, 'mbientlab_quarter': 30, 'motionminers_real': 27}
    sliding_window_length = {'mocap': 200, 'mbientlab': 100, 'virtual': 100, 'mocap_half': 100, 'virtual_quarter': 25,
                             'mocap_quarter': 25, 'mbientlab_50_p': 100, 'mbientlab_10_p': 100, 'mbientlab_50_r': 100,
                             'mbientlab_10_r': 100, 'mbientlab_quarter': 25, 'motionminers_real': 100}
    sliding_window_step = {'mocap': 25, 'mbientlab': 12, 'virtual': 12, 'mocap_half': 12, 'virtual_quarter': 12,
                           'mocap_quarter': 12, 'mbientlab_50_p': 12, 'mbientlab_10_p': 12, 'mbientlab_50_r': 12,
                           'mbientlab_10_r': 12, 'mbientlab_quarter': 12, 'motionminers_real': 12}
    num_attributes = {'mocap': 19, 'mbientlab': 19, 'virtual': 19, 'mocap_half': 19, 'virtual_quarter': 19,
                      'mocap_quarter': 19, 'mbientlab_50_p': 19, 'mbientlab_10_p': 19, 'mbientlab_50_r': 19,
                      'mbientlab_10_r': 19, 'mbientlab_quarter': 19, 'motionminers_real': 19}
    num_tr_inputs = {'mocap': 205016, 'mbientlab': 91384, 'virtual': 239013, 'mocap_half': 213472,
                     'virtual_quarter': 116428, 'mocap_quarter': 168505, 'mbientlab_50_p': 49850,
                     'mbientlab_10_p': 27591, 'mbientlab_50_r': 21791, 'mbientlab_10_r': 8918,
                     'mbientlab_quarter': 91384, 'motionminers_real': 22057}

    num_classes = {'mocap': 7, 'mbientlab': 7, 'virtual': 7, 'mocap_half': 7, 'virtual_quarter': 7,
                   'mocap_quarter': 7, 'mbientlab_50_p': 7, 'mbientlab_10_p': 7, 'mbientlab_50_r': 7,
                   'mbientlab_10_r': 7, 'mbientlab_quarter': 7, 'motionminers_real': 6}

    # Learning rate
    learning_rates = [0.0001, 0.00001, 0.000001]
    lr = {'mocap': {'cnn': learning_rates[learning_rates_idx],
                    'lstm': learning_rates[learning_rates_idx],
                    'cnn_imu': learning_rates[learning_rates_idx]},
          'mbientlab': {'cnn': learning_rates[learning_rates_idx],
                        'lstm': learning_rates[learning_rates_idx],
                        'cnn_imu': learning_rates[learning_rates_idx]},
          'virtual': {'cnn': learning_rates[learning_rates_idx],
                      'lstm': learning_rates[learning_rates_idx],
                      'cnn_imu': learning_rates[learning_rates_idx]},
          'mocap_half': {'cnn': learning_rates[learning_rates_idx],
                         'lstm': learning_rates[learning_rates_idx],
                         'cnn_imu': learning_rates[learning_rates_idx]},
          'virtual_quarter': {'cnn': learning_rates[learning_rates_idx],
                              'lstm': learning_rates[learning_rates_idx],
                              'cnn_imu': learning_rates[learning_rates_idx]},
          'mocap_quarter': {'cnn': learning_rates[learning_rates_idx],
                            'lstm': learning_rates[learning_rates_idx],
                            'cnn_imu': learning_rates[learning_rates_idx]},
          'mbientlab_50_p': {'cnn': learning_rates[learning_rates_idx],
                             'lstm': learning_rates[learning_rates_idx],
                             'cnn_imu': learning_rates[learning_rates_idx]},
          'mbientlab_10_p': {'cnn': learning_rates[learning_rates_idx],
                             'lstm': learning_rates[learning_rates_idx],
                             'cnn_imu': learning_rates[learning_rates_idx]},
          'mbientlab_50_r': {'cnn': learning_rates[learning_rates_idx],
                             'lstm': learning_rates[learning_rates_idx],
                             'cnn_imu': learning_rates[learning_rates_idx]},
          'mbientlab_10_r': {'cnn': learning_rates[learning_rates_idx],
                             'lstm': learning_rates[learning_rates_idx],
                             'cnn_imu': learning_rates[learning_rates_idx]},
          'mbientlab_quarter': {'cnn': learning_rates[learning_rates_idx],
                          'lstm': learning_rates[learning_rates_idx],
                          'cnn_imu': learning_rates[learning_rates_idx]},
          'motionminers_real': {'cnn': learning_rates[learning_rates_idx],
                                'lstm': learning_rates[learning_rates_idx],
                                'cnn_imu': learning_rates[learning_rates_idx]}
          }
    lr_mult = 1.0

    # Maxout
    use_maxout = {'cnn': False, 'lstm': False, 'cnn_imu': False}

    # Balacing
    balancing = {'mocap': False, 'mbientlab': False, 'virtual': False, 'mocap_half': False, 'virtual_quarter': False,
                 'mocap_quarter': False, 'mbientlab_50_p': False, 'mbientlab_10_p': False, 'mbientlab_50_r': False,
                 'mbientlab_10_r': False, 'mbientlab_quarter': False, 'motionminers_real': False}

    # Epochs
    if usage_modus[usage_modus_idx] == 'train_final' or usage_modus[usage_modus_idx] == 'fine_tuning':
        epoch_mult = 2
    else:
        epoch_mult = 1

    epochs = {'mocap': {'cnn': {'softmax': 32, 'attribute': 50},
                        'lstm': {'softmax': 10, 'attribute': 5},
                        'cnn_imu': {'softmax': 32, 'attribute': 50}},
              'mbientlab': {'cnn': {'softmax': 32, 'attribute': 50},
                            'lstm': {'softmax': 10, 'attribute': 5},
                            'cnn_imu': {'softmax': 32, 'attribute': 50}},
              'virtual': {'cnn': {'softmax': 32, 'attribute': 50},
                          'lstm': {'softmax': 10, 'attribute': 5},
                          'cnn_imu': {'softmax': 32, 'attribute': 50}},
              'mocap_half': {'cnn': {'softmax': 32, 'attribute': 50},
                             'lstm': {'softmax': 10, 'attribute': 5},
                             'cnn_imu': {'softmax': 32, 'attribute': 50}},
              'virtual_quarter': {'cnn': {'softmax': 32, 'attribute': 50},
                                  'lstm': {'softmax': 10, 'attribute': 5},
                                  'cnn_imu': {'softmax': 32, 'attribute': 50}},
              'mocap_quarter': {'cnn': {'softmax': 32, 'attribute': 50},
                                'lstm': {'softmax': 10, 'attribute': 5},
                                'cnn_imu': {'softmax': 32, 'attribute': 50}},
              'mbientlab_50_p': {'cnn': {'softmax': 32, 'attribute': 50},
                                 'lstm': {'softmax': 10, 'attribute': 5},
                                 'cnn_imu': {'softmax': 32, 'attribute': 50}},
              'mbientlab_10_p': {'cnn': {'softmax': 32, 'attribute': 50},
                                 'lstm': {'softmax': 10, 'attribute': 5},
                                 'cnn_imu': {'softmax': 32, 'attribute': 50}},
              'mbientlab_50_r': {'cnn': {'softmax': 32, 'attribute': 50},
                                 'lstm': {'softmax': 10, 'attribute': 5},
                                 'cnn_imu': {'softmax': 32, 'attribute': 50}},
              'mbientlab_10_r': {'cnn': {'softmax': 32, 'attribute': 50},
                                 'lstm': {'softmax': 10, 'attribute': 5},
                                 'cnn_imu': {'softmax': 32, 'attribute': 50}},
              'mbientlab_quarter': {'cnn': {'softmax': 32, 'attribute': 50},
                                    'lstm': {'softmax': 10, 'attribute': 5},
                                    'cnn_imu': {'softmax': 32, 'attribute': 50}},
              'motionminers_real': {'cnn': {'softmax': 15, 'attribute': 15},
                                    'lstm': {'softmax': 5, 'attribute': 5},
                                    'cnn_imu': {'softmax': 5, 'attribute': 5}}
              }

    division_epochs = {'mocap': 2, 'mbientlab': 1, 'virtual': 1, 'mocap_half': 1, 'virtual_quarter': 1,
                       'mocap_quarter': 1, 'mbientlab_50_p': 1, 'mbientlab_10_p': 1, 'mbientlab_50_r': 1,
                       'mbientlab_10_r': 1, 'mbientlab_quarter': 1, 'motionminers_real': 1}

    # Batch size
    batch_size_train = {
        'cnn': {'mocap': 100, 'mbientlab': 100, 'virtual': 100, 'mocap_half': 100, 'virtual_quarter': 100,
                'mocap_quarter': 100, 'mbientlab_50_p': 100, 'mbientlab_10_p': 100, 'mbientlab_50_r': 100,
                'mbientlab_10_r': 25, 'mbientlab_quarter': 100, 'motionminers_real': 100},
        'lstm': {'mocap': 100, 'mbientlab': 100, 'virtual': 100, 'mocap_half': 100, 'virtual_quarter': 100,
                 'mocap_quarter': 100, 'mbientlab_50_p': 100, 'mbientlab_10_p': 100, 'mbientlab_50_r': 100,
                 'mbientlab_10_r': 100, 'mbientlab_quarter': 100, 'motionminers_real': 100},
        'cnn_imu': {'mocap': 100, 'mbientlab': 100, 'virtual': 100, 'mocap_half': 100, 'virtual_quarter': 100,
                    'mocap_quarter': 100, 'mbientlab_50_p': 100, 'mbientlab_10_p': 100, 'mbientlab_50_r': 100,
                    'mbientlab_10_r': 25, 'mbientlab_quarter': 100, 'motionminers_real': 100}}

    batch_size_val = {'cnn': {'mocap': 100, 'mbientlab': 100, 'virtual': 100, 'mocap_half': 100,
                              'virtual_quarter': 100, 'mocap_quarter': 100, 'mbientlab_50_p': 100,
                              'mbientlab_10_p': 100, 'mbientlab_50_r': 100, 'mbientlab_10_r': 25,
                              'mbientlab_quarter': 100, 'motionminers_real': 100},
                      'lstm': {'mocap': 100, 'mbientlab': 100, 'virtual': 100, 'mocap_half': 100,
                               'virtual_quarter': 100, 'mocap_quarter': 100, 'mbientlab_50_p': 100,
                               'mbientlab_10_p': 100, 'mbientlab_50_r': 100, 'mbientlab_10_r': 100,
                               'mbientlab_quarter': 100, 'motionminers_real': 100},
                      'cnn_imu': {'mocap': 100, 'mbientlab': 100, 'virtual': 100, 'mocap_half': 100,
                                  'virtual_quarter': 100, 'mocap_quarter': 100,
                                  'mbientlab_50_p': 100, 'mbientlab_10_p': 100, 'mbientlab_50_r': 100,
                                  'mbientlab_10_r': 25, 'mbientlab_quarter': 100, 'motionminers_real': 100}}

    accumulation_steps = {'mocap': 4, 'mbientlab': 4, 'virtual': 4, 'mocap_half': 4, 'virtual_quarter': 4,
                          'mocap_quarter': 4, 'mbientlab_50_p': 4, 'mbientlab_10_p': 4, 'mbientlab_50_r': 4,
                          'mbientlab_10_r': 4, 'mbientlab_quarter': 4, 'motionminers_real': 4}

    # Filters
    filter_size = {'mocap': 5, 'mbientlab': 5, 'virtual': 5, 'mocap_half': 5, 'virtual_quarter': 5, 'mocap_quarter': 5,
                   'mbientlab_50_p': 5, 'mbientlab_10_p': 5, 'mbientlab_50_r': 5, 'mbientlab_10_r': 5,
                   'mbientlab_quarter': 5, 'motionminers_real': 5}
    num_filters = {'mocap': {'cnn': 64, 'lstm': 64, 'cnn_imu': 64},
                   'mbientlab': {'cnn': 64, 'lstm': 64, 'cnn_imu': 64},
                   'virtual': {'cnn': 64, 'lstm': 64, 'cnn_imu': 64},
                   'mocap_half': {'cnn': 64, 'lstm': 64, 'cnn_imu': 64},
                   'virtual_quarter': {'cnn': 64, 'lstm': 64, 'cnn_imu': 64},
                   'mocap_quarter': {'cnn': 64, 'lstm': 64, 'cnn_imu': 64},
                   'mbientlab_50_p': {'cnn': 64, 'lstm': 64, 'cnn_imu': 64},
                   'mbientlab_10_p': {'cnn': 64, 'lstm': 64, 'cnn_imu': 64},
                   'mbientlab_50_r': {'cnn': 64, 'lstm': 64, 'cnn_imu': 64},
                   'mbientlab_10_r': {'cnn': 64, 'lstm': 64, 'cnn_imu': 64},
                   'mbientlab_quarter': {'cnn': 64, 'lstm': 64, 'cnn_imu': 64},
                   'motionminers_real': {'cnn': 64, 'lstm': 64, 'cnn_imu': 64}}

    freeze_options = [False, True]

    # Evolution
    evolution_iter = 10000

    reshape_input = reshape_input
    if reshape_input:
        reshape_folder = "reshape"
    else:
        reshape_folder = "noreshape"

    if fully_convolutional:
        fully_convolutional = "FCN"
    else:
        fully_convolutional = "FC"

    if output[output_idx] == 'softmax':
        labeltype = "class"
        folder_base = "/data2/"
    elif output[output_idx] == 'attribute':
        labeltype = "attributes"
        folder_base = "/data2/"

    # Folder
    if usage_modus[usage_modus_idx] == 'train':
        folder_exp = folder_base + 'fmoya/HAR/pytorch/' + dataset[dataset_idx] + '/' + \
                     network[network_idx] + '/' + output[output_idx] + '/' + fully_convolutional + '/' \
                     + reshape_folder + '/' + 'experiment/'
        folder_exp_base_fine_tuning = folder_base + 'fmoya/HAR/pytorch/' + dataset[dataset_fine_tuning_idx] + '/' + \
                                      network[network_idx] + '/' + output[output_idx] + '/' + fully_convolutional + \
                                      '/' + reshape_folder + '/' + 'final/'
    elif usage_modus[usage_modus_idx] == 'test':
        folder_exp = folder_base + 'fmoya/HAR/pytorch/' + dataset[dataset_idx] + '/' + \
                     network[network_idx] + '/' + output[output_idx] + '/' + fully_convolutional + \
                     '/' + reshape_folder + '/' + 'final/'
        folder_exp_base_fine_tuning = folder_base + 'fmoya/HAR/pytorch/' + dataset[dataset_fine_tuning_idx] + '/' + \
                                      network[network_idx] + '/' + output[output_idx] + '/' + fully_convolutional + \
                                      '/' + reshape_folder + '/' + 'final/'
    elif usage_modus[usage_modus_idx] == 'train_final':
        folder_exp = folder_base + 'fmoya/HAR/pytorch/' + dataset[dataset_idx] + '/' + \
                     network[network_idx] + '/' + output[output_idx] + '/' + fully_convolutional +\
                     '/' + reshape_folder + '/' + 'final/'
        folder_exp_base_fine_tuning = folder_base + 'fmoya/HAR/pytorch/' + dataset[dataset_fine_tuning_idx] + '/' + \
                                      network[network_idx] + '/' + output[output_idx] + '/' + fully_convolutional + \
                                      '/' + reshape_folder + '/' + 'final/'
    elif usage_modus[usage_modus_idx] == 'fine_tuning':
        folder_exp = folder_base + 'fmoya/HAR/pytorch/' + dataset[dataset_idx] + '/' + \
                     network[network_idx] + '/' + output[output_idx] + '/' + fully_convolutional + \
                     '/' + reshape_folder + '/' + 'fine_tuning/'
        folder_exp_base_fine_tuning = folder_base + 'fmoya/HAR/pytorch/' + dataset[dataset_fine_tuning_idx] + '/' + \
                                      network[network_idx] + '/' + output[output_idx] + '/' + fully_convolutional + \
                                      '/' + reshape_folder + '/' + 'final/'
    else:
        raise ("Error: Not selected fine tuning option")

    dataset_root = {'mocap': folder_base + 'fmoya/HAR/datasets/MoCap_dataset/',
                    'mbientlab': folder_base + 'fmoya/HAR/datasets/mbientlab/',
                    'virtual': folder_base + 'fmoya/HAR/datasets/Virtual_IMUs/',
                    'mocap_half': folder_base + 'fmoya/HAR/datasets/MoCap_dataset_half_freq/',
                    'virtual_quarter': folder_base + 'fmoya/HAR/datasets/Virtual_IMUs/',
                    'mocap_quarter': folder_base + 'fmoya/HAR/datasets/MoCap_dataset_half_freq/',
                    'mbientlab_50_p': folder_base + 'fmoya/HAR/datasets/mbientlab_50_persons/',
                    'mbientlab_10_p': folder_base + 'fmoya/HAR/datasets/mbientlab_10_persons/',
                    'mbientlab_50_r': folder_base + 'fmoya/HAR/datasets/mbientlab_50_recordings/',
                    'mbientlab_10_r': folder_base + 'fmoya/HAR/datasets/mbientlab_10_recordings/',
                    'mbientlab_quarter': folder_base + 'fmoya/HAR/datasets/mbientlab/',
                    'motionminers_real': folder_base + 'fmoya/HAR/datasets/motionminers_real/'}

    # GPU
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"
    GPU = 0

    # Labels position on the segmented window
    label_pos = {0: 'middle', 1: 'mode', 2: 'end'}

    percentages_names = ["001", "002", "005", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
    percentages_dataset = [0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    train_show_value = num_tr_inputs[dataset[dataset_idx]] * percentages_dataset[percentage_idx]
    if dataset[dataset_idx] == "mbientlab":
        train_show = {'cnn': int(train_show_value / 300), 'lstm': 100, 'cnn_imu': int(train_show_value / 300)}
        valid_show = {'cnn': int(train_show_value / 100), 'lstm': 500, 'cnn_imu': int(train_show_value / 100)}
    else:
        train_show = {'cnn': 50, 'lstm': 100, 'cnn_imu': 50}
        valid_show = {'cnn': 100, 'lstm': 500, 'cnn_imu': 100}

    now = datetime.datetime.now()


    configuration = {'dataset': dataset[dataset_idx],
                     'dataset_finetuning': dataset[dataset_fine_tuning_idx],
                     'network': network[network_idx],
                     'output': output[output_idx],
                     'num_filters': num_filters[dataset[dataset_idx]][network[network_idx]],
                     'filter_size': filter_size[dataset[dataset_idx]],
                     'lr': lr[dataset[dataset_idx]][network[network_idx]] * lr_mult,
                     'epochs': epochs[dataset[dataset_idx]][network[network_idx]][output[output_idx]] * epoch_mult,
                     'evolution_iter': evolution_iter,
                     'train_show': train_show[network[network_idx]],
                     'valid_show': valid_show[network[network_idx]],
                     'plotting': plotting,
                     'usage_modus': usage_modus[usage_modus_idx],
                     'folder_exp': folder_exp,
                     'folder_exp_base_fine_tuning': folder_exp_base_fine_tuning,
                     'use_maxout': use_maxout[network[network_idx]],
                     'balancing': balancing[dataset[dataset_idx]],
                     'GPU': GPU,
                     'division_epochs': division_epochs[dataset[dataset_idx]],
                     'NB_sensor_channels': NB_sensor_channels[dataset[dataset_idx]],
                     'sliding_window_length': sliding_window_length[dataset[dataset_idx]],
                     'sliding_window_step': sliding_window_step[dataset[dataset_idx]],
                     'num_attributes': num_attributes[dataset[dataset_idx]],
                     'batch_size_train': batch_size_train[network[network_idx]][dataset[dataset_idx]],
                     'batch_size_val': batch_size_val[network[network_idx]][dataset[dataset_idx]],
                     'num_classes': num_classes[dataset[dataset_idx]],
                     'label_pos': label_pos[2],
                     'file_suffix': 'results_yy{}mm{}dd{:02d}hh{:02d}mm{:02d}.xml'.format(now.year,
                                                                                          now.month,
                                                                                          now.day,
                                                                                          now.hour,
                                                                                          now.minute),
                     'dataset_root': dataset_root[dataset[dataset_idx]],
                     'accumulation_steps': accumulation_steps[dataset[dataset_idx]],
                     'reshape_input': reshape_input,
                     'name_counter': name_counter,
                     'freeze_options': freeze_options[freeze],
                     'percentages_names': percentages_names[percentage_idx],
                     'fully_convolutional': fully_convolutional,
                     'sacred': sacred,
                     'labeltype': labeltype}

    return configuration


def setup_experiment_logger(logging_level=logging.DEBUG, filename=None):
    # set up the logging
    logging_format = '[%(asctime)-19s, %(name)s, %(levelname)s] %(message)s'

    if filename != None:
        logging.basicConfig(filename=filename, level=logging.DEBUG,
                            format=logging_format,
                            filemode='w')
    else:
        logging.basicConfig(level=logging_level,
                            format=logging_format,
                            filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger

    if logging.getLogger('').hasHandlers():
        logging.getLogger('').handlers.clear()

    logging.getLogger('').addHandler(console)

    return


def main():
    dataset_idx = [11]
    network_idx = [0]
    reshape_input = [False]
    output_idxs = [0, 1]
    lrs = [0, 1, 2]
    dataset_ft_idx = [0,1,2,3]
    counter_exp = 0
    freeze = [0]
    percentages = [12]
    for dts in range(len(dataset_idx)):
        for nt in range(len(network_idx)):
            for opt in output_idxs:
                for dft in dataset_ft_idx:
                    for pr in percentages:
                        for rsi in range(len(reshape_input)):
                            for fr in freeze:
                                for lr in lrs:
                                    config = configuration(dataset_idx=dataset_idx[dts],
                                                           network_idx=network_idx[nt],
                                                           output_idx=opt,
                                                           usage_modus_idx=5,
                                                           dataset_fine_tuning_idx=dft,
                                                           reshape_input=reshape_input[rsi],
                                                           learning_rates_idx=lr,
                                                           name_counter=counter_exp,
                                                           freeze=fr,
                                                           percentage_idx=pr,
                                                           fully_convolutional=False)

                                    setup_experiment_logger(logging_level=logging.DEBUG,
                                                            filename=config['folder_exp'] + "logger.txt")

                                    logging.info('Finished')

                                    modus = Modus_Selecter(config)

                                    # Starting process
                                    modus.net_modus()
                                    counter_exp += 1


    return


if __name__ == '__main__':

    print("Python Platform {}".format(platform.python_version()))
    
    main()

    print("Done")

