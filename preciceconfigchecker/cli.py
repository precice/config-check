#import sys
#from precice_config_graph import graph, xml_processing
#from pyprecice import Participant
from rule import rules

from collection_of_rules.level1.rule_1_1 import *
from collection_of_rules.level1.rule_1_2 import *
from collection_of_rules.level1.rule_1_3 import *
from collection_of_rules.level1.rule_1_4 import *
from collection_of_rules.level2.rule_2_1 import *
from collection_of_rules.level2.rule_2_2 import *
from collection_of_rules.level3.rule_3_1 import *

def check_all_rules() -> None:
    #path:str = "./preciceconfigchecker/collection_of_rules"
    #levels = os.listdir(path)
    #for level in levels:
    #    level_path:str = path + "/" + level
    #    rule_files = os.listdir(level_path)
    #    for rule_file in rule_files:
    #        if rule_file != "__pycache__":
    #            rule_path = level_path + "/" + rule_file
    #            exec(open(rule_path).read())
    #    copy_rules = rules
    #    for rule in copy_rules:
    #        rule.check()
    #        print(rule)
    #        rules_checked.append(rule)
    #    rules.clear()
    for rule in rules:
        rule.check()
        rule.collect_output()
        print(rule.get_complete_output())

if __name__ == "__main__":
    #path = sys.argv[1]

    #print(f"Checking file at {path}")

    # Step 1: Use PreCICE itself to check for basic errors
    #TODO: Participant.check(...)

    # Step 2: Detect more issues through the use of a graph
    #root = xml_processing.parse_file(path)
    #graph.get_graph(root)

    check_all_rules()