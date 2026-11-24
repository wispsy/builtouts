"""Installed contracts for the three public utility modules."""
import sys
import types
import unittest
from unittest.mock import patch
from builtouts.auto_repr import auto_repr
from builtouts.callable_module import callable_module
from builtouts.exit_to_repl import exit_to_repl


class UtilityTests(unittest.TestCase):
    def test_repr_public_slots_explicit_properties_and_recursion(self):
        @auto_repr(include=("label",), exclude=("secret",))
        class Record:
            __slots__ = ("value", "secret", "_hidden")
            def __init__(self):
                self.value, self.secret, self._hidden = 4, "private", "hidden"
            @property
            def label(self):
                return "sample"
        record = Record()
        self.assertEqual(repr(record), "Record(value=4, label='sample')")
        record.value = record
        self.assertEqual(repr(record), "Record(value=..., label='sample')")

    def test_callable_module_preserves_function_and_module_exports(self):
        name = "_callable_module_fixture"
        module = types.ModuleType(name)
        def add(value):
            return value + 3
        add.__module__ = name
        module.marker = "preserved"
        with patch.dict(sys.modules, {name: module}):
            self.assertIs(callable_module(add), add)
            self.assertEqual(module(4), 7)
            self.assertEqual(module.marker, "preserved")
            self.assertEqual(module.__name__, name)

    def test_repl_uses_caller_locals_without_opening_interactive_input(self):
        local_value = "caller fixture"
        with patch("builtouts.exit_to_repl.code.interact", return_value="completed") as interact:
            self.assertEqual(exit_to_repl(), "completed")
        self.assertEqual(interact.call_args.kwargs["local"]["local_value"], local_value)
        self.assertIn("local_value='caller fixture'", interact.call_args.kwargs["banner"])
