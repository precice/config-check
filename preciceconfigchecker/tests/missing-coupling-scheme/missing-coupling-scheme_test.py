import contextlib
import io

from precice_config_graph import graph, xml_processing

from preciceconfigchecker.rules_processing import check_all_rules
from preciceconfigchecker.rule import rules

from preciceconfigchecker.rules.missing_coupling import MissingCouplingSchemeRule as c


def equals(a, b):
    if type(a) != type(b):
        return False
    return vars(a) == vars(b)


xml = xml_processing.parse_file("precice-config.xml")
graph = graph.get_graph(xml)

# To suppress terminal messages
with contextlib.redirect_stdout(io.StringIO()):
    check_all_rules(graph, False)

violations_expected = []

v_missing_coupling_scheme = c.MissingCouplingSchemeViolation()

violations_expected += [v_missing_coupling_scheme]

violations_actual = []
for rule in rules:
    for violation in rule.violations:
        violations_actual.append(violation)

violations_expected_s = sorted(violations_expected, key=lambda obj: type(obj).__name__)
violations_actual_s = sorted(violations_actual, key=lambda obj: type(obj).__name__)

for violation_e, violation_a in zip(violations_expected_s, violations_actual_s):
    # print(violation_e, violation_a)
    assert equals(violation_e, violation_a), "There is an error in missing-coupling-scheme test."
print("Passed missing-coupling-scheme test.")
