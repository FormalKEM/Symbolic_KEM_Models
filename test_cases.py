import argparse
import subprocess
import os
import itertools

# TODO clean up the script
OUTPUTF = "testfiles"
RESULTS = "bindingresults"
TIMEOUT = "20"

BINDING_PROPERTIES = [
        'bindktoct',
        'bindktopk',
        'bindcttok',
        'bindcttopk',
        'bindkcttopk',
        'bindpkktoct'
        ]

ORACLETEST = [
        'BindingGames/Ct_Bind_K.spthy',
        'BindingGames/Ct_Bind_Pk.spthy',
        'BindingGames/K_Bind_Ct.spthy',
        'BindingGames/K_Bind_Pk.spthy',
        'BindingGames/K_Ct_Bind_Pk.spthy',
        'BindingGames/Pk_K_Bind_Ct.spthy',
        'BindingGames/Mal_Ct_Bind_K.spthy',
        'BindingGames/Mal_Ct_Bind_Pk.spthy',
        'BindingGames/Mal_K_Bind_Ct.spthy',
        'BindingGames/Mal_K_Bind_Pk.spthy',
        'BindingGames/Mal_K_Ct_Bind_Pk.spthy',
        'BindingGames/Mal_Pk_K_Bind_Ct.spthy'
        ]

def get_combinations(lst,leng):
   combination = [] 
   for r in range(1, leng + 1):
      # to generate combination
      combination += itertools.combinations(lst, r)
   return combination

def run_tamarin(filename, outputf, flags):
    name = 'tamarin_wrapper.py'
    command = 'python3 {} {} -p {} -t {} --resultfolder {}'.format(name, filename, ','.join(flags), TIMEOUT, outputf)
    print(command.split(' '))
    process = subprocess.Popen(command.strip('\n').split(' '), cwd=os.path.dirname(os.path.realpath(__file__)),
                               stderr=subprocess.STDOUT,
                               stdout=subprocess.PIPE, start_new_session=True, shell=False)
    try:
        process.communicate()
        return "Worked"
    except Exception:
        return "Error"

def combiner(ora,ppf,mal):
    ToTest = []
    for file in ora:
        ToTest.append((file,[]))
        for flags in get_combinations(ppf,6):
            ToTest.append((file,list(flags)))
    results = []
    if mal:
        for (file,lof) in ToTest:
            results.append((file,lof))
            results.append((file,lof+['MAL']))
    else:
        results = ToTest
    return results


# TODO prettify the output
def collect_results(filename, flags, outputf):
    name = filename.split('/')[-1]
    with open(RESULTS+"/"+name,"a+") as h:
        if not os.path.exists(outputf):
            raise Exception
        for f in os.listdir(outputf):
            with open(outputf+"/"+f) as g:
                for line in g.readlines():
                    h.writelines(name+","+line.split(',')[0]+","+str(flags)+","+line.split(',')[1]+'\n')
            os.remove(outputf+"/"+f)
        os.rmdir(outputf)
    

def test(mal):
    oracle_names = ORACLETEST
    possible_preprocessor_flags = BINDING_PROPERTIES
    combinations = combiner(oracle_names, possible_preprocessor_flags,mal)
    for (filename, flags) in combinations:
        code = run_tamarin(filename,OUTPUTF,flags)
        assert code == "Worked"
        collect_results(filename, flags, OUTPUTF)


def main(args):
    mal = False
    if not os.path.exists(RESULTS):
        os.mkdir(RESULTS)
    if args.test:
        test(True)
    if args.mal:
        mal = True
    if args.filename:
        filenames = args.filename.split(',')
        possible_preprocessor_flags = BINDING_PROPERTIES
        combinations = combiner(filenames, possible_preprocessor_flags,mal)
        for (filename, flags) in combinations:
            code = run_tamarin(filename,OUTPUTF,flags)
            assert code == "Worked"
            collect_results(filename, flags, OUTPUTF)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A cool script to run testcases')
    parser.add_argument('filename', nargs='?', type=str, help="string of filenames separated by commas")
    parser.add_argument('--test',  action="store_true", help="Execute test cases")
    parser.add_argument('--mal',  action="store_true", help="Enable MAL")
    args = parser.parse_args()
    main(args)