import unittest

from starwars.nodes import BinaryOp, Number, Print, Program, Variable, to_dict


class ToDictTest(unittest.TestCase):
    def test_serializes_nested_nodes(self):
        expression = BinaryOp(Number("1", 1, 5), "+", Variable("x", 1, 9), 1, 7)
        self.assertEqual(to_dict(Program([Print([expression], 1, 1)])), {
            "node": "Program",
            "statements": [{
                "node": "Print",
                "items": [{
                    "node": "BinaryOp",
                    "left": {"node": "Number", "text": "1", "line": 1, "column": 5, "type_name": None},
                    "op": "+",
                    "right": {"node": "Variable", "name": "x", "line": 1, "column": 9,
                              "c_name": None, "type_name": None},
                    "line": 1, "column": 7, "type_name": None,
                }],
                "line": 1, "column": 1,
            }],
            "functions": [],
        })


if __name__ == "__main__":
    unittest.main()
