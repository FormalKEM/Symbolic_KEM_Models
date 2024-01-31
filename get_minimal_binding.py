import kem_property_dag
import argparse
import subprocess
import os
import datetime

TIMEOUT = 1800


def run_tamarin(filename, outputf, flags, lemma):
    name = 'tamarin_wrapper.py'
    command = 'python3 {} {} -l {} -p {} -t {} --resultfolder {}'.format(name, filename, lemma, ','.join(flags), TIMEOUT, outputf)
    print(command.split(' '))
    process = subprocess.Popen(command.strip('\n').split(' '), cwd=os.path.dirname(os.path.realpath(__file__)),
                               stderr=subprocess.STDOUT,
                               stdout=subprocess.PIPE, start_new_session=True, shell=False)
    try:
        sdin, sder = process.communicate()
        if "True" in str(sdin):
            print('P')
            return "P"
        elif "False" in str(sdin):
            print('CEX')
            return "CEX"
        else:
            print('Timeout')
            return "Timeout"
    except Exception:
        return "Error"
    

def main(args):
    current_time = datetime.datetime.now()
    timestamp = str(current_time.timestamp())
      
    for lemma in args.lemmas.split(','):
        if args.mal:
            dag = kem_property_dag.get_mal_kem_property_dag(args.filename+'_'+lemma+'_'+'MAL'+'_'+timestamp)
        else:
            dag = kem_property_dag.get_kem_property_dag(args.filename+'_'+lemma+'_'+timestamp)
        while not(dag.is_fully_explored()):
            next_property = dag.get_next_property()
            flag_list = [s.strip() for s in next_property.split(',')]
            if args.mal:
                flag_list.append('MAL')
            else:
                flag_list.append('GoodKeysOnly')
            result = run_tamarin(args.filename, 'Results_'+timestamp, flag_list, lemma)
            if result == "P":
                dag.report_proof(next_property)
            elif result == "CEX":
                dag.report_counterexample(next_property)
            else:
                dag.report_timeout(next_property)
        dag.render_dot()
        print("SOLUTION:")
        print(dag.get_solution_set())

            



    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A cool script to run testcases')
    parser.add_argument('filename', nargs='?', type=str, help="string of filename")
    parser.add_argument('lemmas', nargs='?', type=str, help="string of lemmas separated by commas")
    parser.add_argument('--mal',  action="store_true", help="Enable MAL")
    args = parser.parse_args()
    main(args)
