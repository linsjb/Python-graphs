import statistics
import matplotlib.pyplot as plt
import numpy as np
import random
import csv
import matplotlib
import yaml
from prodict import Prodict
import click

@click.command()
@click.option('--config', default='plot.yaml')
def run(config):
    with open ('./config/' + config) as config_file:
        plot_config = Prodict.from_dict(yaml.load(config_file, Loader=yaml.FullLoader))
    plot_data = {
        'x': None,
        'y': []
    }
    with open ('./data/' + plot_config.data_file, newline='') as data_file:
        csv_reader = csv.reader(data_file, delimiter=',')
        counter = 0
        for row in csv_reader:
            if counter == 0:
                plot_data['x'] = row
            else:
                plot_data['y'].append(row)
            counter += 1

    if(plot_config.plot_type == 'bar'):
        barPlot(plot_config, plot_data)
    elif(plot_config.plot_type == 'line'):
        linePlot(plot_config, plot_data, 2)
    
def linePlot(config, data, width):
    plt.close()
    plt.title(config.title)
    plt.xlabel(config.x_label)
    plt.ylabel(config.y_label)
    plt.grid(True)

    for data_row in data['y']:
        y_data = [float(y) for y in data_row]
        plot_counter = 0
        plt.plot(data['x'], y_data, linewidth = width, label=config.labels[plot_counter])
        plot_counter += 1

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=2)
    plt.tight_layout()

    fileTypes(config)

def barPlot(config, data):
    width = 0.4
    
    plt.close()
    fig = plt.figure()
    sub_fig = fig.add_subplot(111)
    plt.title(config.title)
    sub_fig.set_ylabel(config.y_label)
    sub_fig.set_xlabel(config.x_label)
    sub_fig.set_xticks(np.arange(len(data['x'])))
    sub_fig.set_xticklabels(data['x'])
    plot_counter = 0

    for data_row in data['y']:
        y_data = [float(y) for y in data_row]
        sub_fig.bar(np.arange(len(data_row)) + width *plot_counter , y_data, width, align='center', label=config.labels[plot_counter])
        plot_counter += 1

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=2)
    plt.tight_layout()

    fileTypes(config)

def fileTypes(config):
    for filetype in config.plot_filetypes:
        if filetype == "pgf":
            matplotlib.use("pgf")
            matplotlib.rcParams.update({
                "pgf.texsystem": "pdflatex",
                'font.family': 'serif',
                'text.usetex': True,
                'pgf.rcfonts': False,
            })
        plt.savefig('./out/' + config.filename + filetype)

if __name__ == '__main__':
    run()