import unittest

from starwars.symbols import SymbolTable


class SymbolTableTest(unittest.TestCase):
    def test_inner_scope_shadows_until_popped(self):
        table = SymbolTable()
        outer = table.declare("x", "int")
        table.push()
        inner = table.declare("x", "float")
        self.assertEqual(table.lookup("x"), inner)
        table.pop()
        self.assertEqual(table.lookup("x"), outer)
        self.assertEqual((outer.c_name, inner.c_name), ("sw_v0", "sw_v1"))

    def test_read_only_symbols_and_fresh_names(self):
        table = SymbolTable()
        self.assertFalse(table.declare("x", "int").read_only)
        self.assertTrue(table.declare("i", "int", read_only=True).read_only)
        self.assertEqual(table.new_c_name(), "sw_v2")
        self.assertIsNone(table.lookup("sw_v2"))

    def test_declared_here_and_missing_names(self):
        table = SymbolTable()
        table.declare("x", "int")
        table.push()
        self.assertFalse(table.declared_here("x"))
        self.assertIsNone(table.lookup("y"))


if __name__ == "__main__":
    unittest.main()
