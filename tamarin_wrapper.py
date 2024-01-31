import argparse
import copy
import itertools
import json
import os
import signal
import subprocess
import pprint
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import csv
import time

ignore = False


def create_commands(model, executable, ram, cores, lemmas, preprocess_flags, tam):
    finished_commands = []
    prefix = ''
    # if timeout:
    #    prefix += 'timeout %i ' % timeout
    prefix += executable + ' ' + model + ' '
    infix = ''
    if ram:  # does not work
        print("RAM is currently not supported")
        exit()
        infix += "+RTS -N%i -M%i -RTS " % (cores, ram * 1024)
    else:
        infix += "+RTS -N%i -RTS " % cores
    preprocess_flags_string = ''
    if preprocess_flags:
        for ffl in preprocess_flags:
            preprocess_flags_string += '-D=%s ' % ffl
    lemma_strings = []
    for lemma in lemmas:
        lemma_strings.append('--prove=%s ' % lemma)
    for lemma_s in lemma_strings:
        command = prefix + lemma_s + infix + preprocess_flags_string + tam
        finished_commands.append((model, command, lemma_s.split("=")[1]))
    return finished_commands


def run_tamarin(cmd, timeout, silent, log):
    process = subprocess.Popen(cmd, cwd=os.path.dirname(os.path.realpath(__file__)), stderr=subprocess.STDOUT,
                               stdout=subprocess.PIPE, start_new_session=True, shell=True)
    try:
        output, errors = process.communicate(timeout=timeout)
        '''if not silent:
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(output.decode("utf-8"))'''
        if "Maude returned warning" in str(output):
            return "AssociativeFailure", ''
        elif "CallStack" in str(output) or "internal error" in str(output):
            print(output)
            return "TamarinError", ''

        proof_results = [line for line in str(
            output).split('\\n') if ("steps" in line)]
        if len(proof_results) >= 1:
            for line in proof_results:
                if "verified" in line:
                    return line, True
                if "falsified" in line:
                    return line, False
            print("Scripting error")
            print(cmd)
            print(output)
            print(proof_results)
            raise ValueError
        else:
            print("Scripting error")
            print(cmd)
            print(output)
            print(proof_results)
            raise ValueError

    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        return "timeout", ''


def tables(data, m):
    title_text = 'Evaluation of %s' % m
    footer_text = date.today().strftime("%B %d, %Y")
    # fig_background_color = 'skyblue'
    fig_border = 'steelblue'

    column_headers = data.pop(0)
    row_headers = [x[0] for x in data]
    cell_text = []
    for row in data:
        # Get some lists of color specs for row and column headers
        cell_text.append([x for x in row])
    # rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
    # Create the figure. Setting a small pad on tight_layout
    ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
    # seems to better regulate white space. Sometimes experimenting
    # with an explicit figsize here can produce better outcome.
    plt.figure(  # linewidth=2,
        edgecolor=fig_border,
        # facecolor=fig_background_color,
        tight_layout={'pad': 1},
        figsize=(8, len(row_headers))
    )  # Add a table at the bottom of the axes
    the_table = plt.table(cellText=cell_text,
                          # rowLabels=row_headers,
                          # rowColours=rcolors,
                          rowLoc='right',
                          colColours=ccolors,
                          colLabels=column_headers,
                          loc='center')  # Scaling is the only influence we have over top and bottom cell padding.
    # Make the rows taller (i.e., make cell y scale larger).
    # the_table.scale(1, 1.5)  # Hide axes
    ax = plt.gca()
    # ax.set_global()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)  # Hide axes border
    plt.box(on=None)  # Add title
    plt.suptitle(title_text)  # Add footer
    # plt.autoscale(tight=True)
    plt.figtext(0.95, 0.05, footer_text, horizontalalignment='right', size=6,
                weight='light')  # Force the figure to update, so backends center objects correctly within the figure.
    # Without plt.draw() here, the title will center on the axes and not the figure.
    # Create image. plt.savefig ignores figure edge and face colors, so map them.
    plt.draw()
    fig = plt.gcf()
    # fig.canvas.draw()
    # fig.tight_layout()
    plt.savefig('results/results_%s.png' % m,
                edgecolor=fig.get_edgecolor(),
                facecolor=fig.get_facecolor(),
                dpi=250
                )


def get_lemma(model, executable, preprocess_flags):
    command = "%s %s" % (executable, model)
    preprocess_flags_string = ''
    if preprocess_flags:
        for ffl in preprocess_flags:
            preprocess_flags_string += ' -D=%s' % ffl
    command += preprocess_flags_string
    process = subprocess.Popen(command.split(' '), cwd=os.path.dirname(os.path.realpath(__file__)),
                               stderr=subprocess.STDOUT,
                               stdout=subprocess.PIPE, start_new_session=True, shell=False)
    try:
        output, errors = process.communicate()
        if "Maude returned warning" in str(output):
            return "AssociativeFailure", ''
        elif "CallStack" in str(output) or "internal error" in str(output):
            return "TamarinError", ''

        proof_results = [line.split(' ')[2] for line in str(
            output).split('\\n') if ("steps" in line)]
        if len(proof_results) > 0:
            return "Success", proof_results
        else:
            return "NoLemmas", []
    except Exception:
        return "Error", []


def load_json(file):
    try:
        with open(file) as json_file:
            data = json.load(json_file)
            return data
    except Exception:
        print("Not a valid JSON format")
        exit()


def decode_file(file):
    data = load_json(file)
    if "ignore" in data.keys():
        ignore = data["ignore"]
    initvalues = [("executable", "tamarin-prover"),
                  ("timeout", 60000),
                  ("ram", None),
                  ("cores", min(os.cpu_count(), 4)),
                  ("silent", False),
                  ("log", False),
                  ("tamcommand", ""),
                  ("graphic", False),
                  ("preprocess_flags", []),
                  ("lemmas", None),
                  ("flags", None),
                  ("resultfolder", "results")]
    model_dict = dict()
    for modelname in data["models"]:
        model_dict[modelname] = dict(initvalues)
        tmplist = data["models"] + ["models"]
        key_subset = [item for item in data.keys() if item not in tmplist]
        for key in key_subset:
            model_dict[modelname][key] = data[key]
        for key_model in ["preprocess_flags", "tamcommand", "flags"]:
            if key_model in data[modelname].keys():
                model_dict[modelname][key_model] = data[modelname][key_model]
        if "lemmas" in data[modelname].keys():
            model_dict[modelname]["lemmas"] = data[modelname]["lemmas"]
        else:
            is_lemmas = get_lemma(modelname,
                                  model_dict[modelname]["executable"],
                                  model_dict[modelname]["preprocess_flags"])
            if is_lemmas[0] == "Success":
                model_dict[modelname]["lemmas"] = is_lemmas[1]
            else:
                print(modelname + " has no lemmas")
                exit()
    return model_dict


def parse_arguments(parsed_args):
    model_dict = dict()
    model_dict[parsed_args.filename] = dict()
    ignore = parsed_args.ignore
    model_dict[parsed_args.filename]["executable"] = parsed_args.name
    model_dict[parsed_args.filename]["timeout"] = parsed_args.timeout
    model_dict[parsed_args.filename]["ram"] = parsed_args.ram
    model_dict[parsed_args.filename]["cores"] = parsed_args.cores
    model_dict[parsed_args.filename]["silent"] = parsed_args.silent
    model_dict[parsed_args.filename]["log"] = parsed_args.log
    model_dict[parsed_args.filename]["tamcommand"] = parsed_args.tam
    model_dict[parsed_args.filename]["graphic"] = parsed_args.graphic
    model_dict[parsed_args.filename]["resultfolder"] = parsed_args.resultfolder
    if parsed_args.preprocess:
        model_dict[parsed_args.filename]["preprocess_flags"] = [
            item for item in parsed_args.preprocess.split(',')]
    else:
        model_dict[parsed_args.filename]["preprocess_flags"] = []
    if parsed_args.lemmas:
        model_dict[parsed_args.filename]["lemmas"] = [
            item for item in parsed_args.lemmas.split(',')]
    else:
        executable = model_dict[parsed_args.filename]["executable"]
        preprocess_flags = model_dict[parsed_args.filename]["preprocess_flags"]
        is_lemmas = get_lemma(parsed_args.filename,
                              executable, preprocess_flags)
        if is_lemmas[0] == "Success":
            model_dict[parsed_args.filename]["lemmas"] = is_lemmas[1]
        else:
            print(parsed_args.filename + " has no lemmas")
            exit()
    # parsed later
    model_dict[parsed_args.filename]["flags"] = parsed_args.flags
    return model_dict


def get_implications(status, orders, nextvalue, restrictions):
    if status:
        new_cross_prod = []
        for i in range(len(nextvalue)):
            if nextvalue[i] == "":
                new_cross_prod.append([""])
            else:
                smaller = [nextvalue[i]]
                for order in orders:
                    if nextvalue[i] == order[0]:
                        smaller.append(order[1])
                smaller.append("")
                new_cross_prod.append(smaller)
        resultlist = list(itertools.product(*new_cross_prod))
    else:
        new_cross_prod = []
        for i in range(len(nextvalue)):
            if nextvalue[i] == "":
                new_cross_prod.append(restrictions[i] + [""])
            else:
                bigger = [nextvalue[i]]
                for order in orders:
                    if nextvalue[i] == order[1]:
                        bigger.append(order[0])
                new_cross_prod.append(bigger)
        resultlist = list(itertools.product(*new_cross_prod))
    resultlist.remove(nextvalue)
    if resultlist:
        return resultlist
    else:
        return []


def compute_flags(model, lemma, command, flag_processor, log, silent, timeout):
    flag_dict = load_json(flag_processor)
    orders = []
    priority = []
    restrictions = []
    if "orders" in flag_dict.keys():
        orders = flag_dict["orders"]
    if "restrictions" in flag_dict.keys():
        restrictions = flag_dict["restrictions"]
    if "priority" in flag_dict.keys():
        priority_raw = flag_dict["priority"]
        for prio in priority_raw:
            tuple_prio = [""] * len(restrictions)
            for element in prio:
                for i in range(len(restrictions)):
                    if element in restrictions[i]:
                        tuple_prio[i] = element
            priority.append(tuple(tuple_prio))
    cross_product_prep = []
    for flaglist in restrictions:
        cross_product_prep.append(flaglist + [""])
    combinations = list(itertools.product(*cross_product_prep))
    resultdict = dict()
    for value in combinations:
        resultdict[tuple(value)] = None
    counter = 0
    while combinations:
        counter += 1
        if priority:
            nextvalue = priority.pop(0)
        else:
            nextvalue = combinations.pop(0)
        flagstring = ""
        for element in nextvalue:
            if element:
                flagstring += " -D=%s" % element
        flags = [item for item in nextvalue if not item == ""]
        start = time.time()
        res, status = run_tamarin(command + flagstring, timeout, silent, log)
        finaltime = time.time() - start
        if res in ["TamarinError", "timeout", "AssociativeFailure"]:
            if res == "TamarinError":
                print((flags, lemma))
            steps = -1
            status = res
            resultdict[nextvalue] = (lemma, status, finaltime, steps, flags)
        else:
            tmplist = res.split()
            steps = tmplist[tmplist.index('steps)') - 1][1:]
            implications = get_implications(
                status, orders, nextvalue, restrictions)
            resultdict[nextvalue] = (lemma, status, finaltime, steps, flags)
            for value in implications:
                if value in resultdict.keys():
                    del resultdict[value]
                if value in combinations:
                    combinations.remove(value)

    print("Number of Tamarin queries for %s, %s: %i" % (model, lemma, counter))
    finallist = []
    for key in resultdict.keys():
        finallist.append(list(resultdict[key]))
    return finallist


def execute_model(model, commands, flag_processor, log, silent, timeout):
    results = []
    for (model, command, lemma) in commands:
        if not flag_processor:
            if not silent:
                print(model, lemma)
            # result_list = [["Protocol", "Lemma", "Verified", "#Steps", "List of Flags"]]
            # result should have the form (model, lemma, status, steps, [flags])
            start = time.time()
            res, status = run_tamarin(command, timeout, silent, log)
            finaltime = time.time() - start
            if res in ["TamarinError", "timeout", "AssociativeFailure"]:
                steps = -1
                status = res
                if not ignore:
                    results.append([lemma, status, finaltime, steps, []])
            else:
                tmplist = res.split()
                steps = tmplist[tmplist.index('steps)') - 1][1:]
                results.append([lemma, status, finaltime, steps, []])
        else:
            results += compute_flags(model, lemma, command,
                                     flag_processor, log, silent, timeout)

    return results


def main(parsed_args):
    start_exec_time = time.time()
    if parsed_args.filename:
        query_dict = parse_arguments(parsed_args)
    else:
        query_dict = decode_file(parsed_args.file)

    fulltable = []
    for model in query_dict.keys():
        res_folder = query_dict[model]["resultfolder"]
        if not os.path.exists(res_folder):
            os.makedirs(res_folder)
    for model in query_dict.keys():
        flags = query_dict[model]["flags"]
        commands = create_commands(model,
                                   query_dict[model]["executable"],
                                   query_dict[model]["ram"],
                                   query_dict[model]["cores"],
                                   query_dict[model]["lemmas"],
                                   query_dict[model]["preprocess_flags"],
                                   query_dict[model]["tamcommand"])
        if not query_dict[model]["silent"]:
            print("Number of created commands: %i" % len(commands))
            for command in commands:
                print(command)
        start_full_exec = time.time()
        cleaned_results = execute_model(model,
                                        commands,
                                        flags,
                                        query_dict[model]["log"],
                                        query_dict[model]["silent"],
                                        query_dict[model]["timeout"])

        finalprocesstime = time.time() - start_full_exec
        tablelist = [["Lemma", "Verified", "Time", "#Steps", "List of Flags"]]
        tablelist += cleaned_results
        if query_dict[model]["graphic"]:
            tables(tablelist, model)
        res_folder = query_dict[model]["resultfolder"]
        with open(res_folder+'/recent_results_%s.csv' % model.split('/')[0], 'w') as r:
            writer = csv.writer(r)
            writer.writerows(cleaned_results)
        intermediate_table = []
        for entry in cleaned_results:
            if entry[1] == True or entry[1] == False:
                intermediate_table += [[model] + entry]
        table_t = tabulate(intermediate_table,
                           headers='firstrow', tablefmt='fancy_grid')
        if not query_dict[model]["silent"]:
            print(table_t)
            print(" ")
            print(finalprocesstime)
        for entry in cleaned_results:
            fulltable += [[model] + entry]
    silent = False
    for key in query_dict.keys():
        silent = query_dict[key]["silent"]
        break
    if not silent:
        print(" ")
        print(" ")
        print(" ")
        table_term = tabulate(fulltable, headers='firstrow', tablefmt='fancy_grid')
        print(table_term)
        exec_time = time.time() - start_exec_time
        print(exec_time)
    else:
        for model in query_dict.keys():
            res_folder = query_dict[model]["resultfolder"]
            with open(res_folder+'/recent_results_%s.csv' % model.split('/')[0], 'r') as r:
                for l in r.readlines():
                    l = l.replace(" ", "").strip()
                    tmplist = l.split(',')
                    print(' '.join(tmplist[:3]))


def pre_process():
    '''
    Parse input
    '''
    parser = argparse.ArgumentParser(description='A cool wrapper for tamarin')
    parser.add_argument('-n', '--name', type=str, default='tamarin-prover',
                        help='name of the tamarin executable')  # WORKING
    parser.add_argument('-t', '--timeout', type=int, default=600,
                        help='timeout in seconds per execution')  # WORKING
    parser.add_argument('-r', '--ram', type=int,
                        help='max RAM in Gb')  # TODO currently not working/supported
    parser.add_argument('-c', '--cores', type=int,
                        help='max cores', default=min(os.cpu_count(), 4))  # WORKING
    parser.add_argument('-s', '--silent', action="store_true",
                        help='surpress tamarin output in the terminal')  # TODO working but stupid
    parser.add_argument('-o', '--log', action="store_true",
                        help='create a log file')  # TODO not implemented
    parser.add_argument('-i', '--ignore', action="store_true", default=False,
                        help='ignore timeouts and erros in the results')  # WORKING
    parser.add_argument('-l', '--lemmas', type=str,
                        help='string of lemmas to prove comma separated')  # WORKING
    parser.add_argument('-p', '--preprocess', type=str,
                        help='string of preprocessor flags which are needed (comma separated)')  # WORKING
    parser.add_argument('-fl', '--flags', type=str,
                        help='file containing preprocessor flags. Check documentation for format')  # WORKING
    parser.add_argument('-g', '--graphic', action="store_true",
                        help='create a output table file')  # WORKING but TODO make prettier Pictures
    parser.add_argument('--tam', type=str, default='',
                        help='string of additional tamarin flags. E.g.: --tam="--auto-sources"')  # WORKING
    parser.add_argument('--resultfolder', type=str, default='results',
                         help='Output folder')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('filename', nargs='?', type=str)  # WORKING
    group.add_argument('-f', '--file', default=None,
                       help='input commands as .tamjson file')  # WORKING
    args = parser.parse_args()
    if args.file:
        if not ".tamjson" in args.file:
            print("We need a tamjson file: %s" % args.file)
            exit()
    if args.flags:
        if not ".json" in args.flags:
            print("We need a json file: %s" % args.flags)
            exit()
    main(args)


if __name__ == '__main__':
    pre_process()
