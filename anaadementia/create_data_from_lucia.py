import argparse
import json
import re
import os


proposicoes = ['LUCIA', 'MORA_INTERIOR', 'PARANA', 'NUMA_MANHA_SEGUNDA', 'ELA_SAI',
                'DE_CASA', 'ENTREVISTA', 'NA_CAPITAL', 'ELA_FOI', 'PARA_RODOVIARIA',
                'DE_CARONA', 'COM_PEDRO', 'ESTAVA_CHOVENDO', 'NAQUELA_MANHA',
                'CARRO', 'PASSOU_CAIU', 'BURACO', 'PNEU_FUROU', 'PENSOU_ACHOU_PERDER',
                'ONIBUS', 'PEGOU_TAXI', 'CONSEGUIU_CHEGAR_TEMPO']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'narratives_dir',
        help='directory with narratives and ann files')
    parser.add_argument('json_file', help='a path to save a json file')
    
    args = parser.parse_args()

    json_object = {}
    for name in os.listdir(args.narratives_dir):
        annotantions = {}
        if name.endswith('ann'):
            with open(os.path.join(args.narratives_dir, name)) as f_ann:
                for annotantion in f_ann:
                    if not annotantion.startswith("#"):
                        splited = annotantion.split('\t')
                        label = splited[1].split()[0]
                        if label not in proposicoes:
                            print(name)
                            print(annotantion)
                            raise Exception
                        key = splited[-1].replace('\n', '')
                        if key in annotantions:
                            annotantions[key].append(label)
                        else:
                            annotantions[key] = [label]
            # Estamos pegando a narrativa original para manter a ordem das sentenças
            sentences = []
            narrative_file  = name.replace('ann', 'txt')
            with open(os.path.join(args.narratives_dir, narrative_file)) as f_txt:
                for line in f_txt:
                    line =  line.replace(' .', '')
                    line =  line.replace('\n', '')
                    if line in annotantions:
                        labels = annotantions[line]
                    else:
                        labels = None
                    sentences.append((line, labels))
            name = name.replace('.ann', '')
            json_object[name] = sentences
        json.dump(json_object, open(args.json_file, 'w'))