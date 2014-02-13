import base
import datum

class ScriptNode(base.Node3D):
    default = """import math

from fab.shapes import *
from fab.expression import Expression

c = circle(0, 0, 1)
output('c', c)
"""

    def __init__(self, name, x, y, z):
        super(ScriptNode, self).__init__(name, x, y, z)
        self.add_datum('script', datum.ScriptDatum(self, self.default))

        self.default_datums = [d[0] for d in self.datums]


    def get_control(self):
        import control.script
        return control.script.ScriptNodeControl


    def update_datums(self):
        """ Updates datums based on script inputs and outputs.
        """
        # Names of dynamic datums
        names = [d[1] for d in self._script._inputs + self._script._outputs]

        # Check to make sure that each existing datum is either one of the
        # defaults or defined by this set of dynamic datums.
        for name, d in self.datums:
            if not name in self.default_datums and not name in names:
                self.del_datum(name)

        # Add new input datums as needed.
        for name, t in self._script._inputs:
            if name in [d[1] for d in self.datums]:
                continue
            elif t is float:
                d = datum.FloatDatum(self, 0)
            elif t is Expression:
                d = datum.ExpressionDatum(self, "None")
            self.add_datum(name, d)
            self.control.editor_datums.append(name)



from fab.expression import Expression
