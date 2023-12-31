import unittest

from pjtools.configurator.base import BaseConfigurator


class TestBaseConfigurator(unittest.TestCase):

    def test_init_and_access(self):
        config = BaseConfigurator({'attr1': 1, 'attr2': 'string'})
        self.assertEqual(config.attr1, 1)
        self.assertEqual(config['attr2'], 'string')

    def test_nested_config(self):
        config = BaseConfigurator({'attr1': {'nested_attr': 2}})
        self.assertIsInstance(config.attr1, BaseConfigurator)
        self.assertEqual(config.attr1.nested_attr, 2)

    def test_merge_with_common_and_unique_keys(self):
        config1 = BaseConfigurator({'a': 1, 'b': 2, 'c': {'x': 10, 'y': 20}})
        config2 = BaseConfigurator({'b': 3, 'c': {'y': 21, 'z': 30}, 'd': 4})

        config1.merge(config2)
        self.assertEqual(config1.to_dict(), {
            'a': 1,
            'b': 3,
            'c': {
                'x': 10,
                'y': 21,
                'z': 30
            },
            'd': 4
        })

    def test_merge_with_empty_config(self):
        config1 = BaseConfigurator({'a': 1})
        config2 = BaseConfigurator({})
        config1.merge(config2)
        self.assertEqual(config1.to_dict(), {'a': 1})

    def test_merge_without_common_keys(self):
        config1 = BaseConfigurator({'a': 1})
        config2 = BaseConfigurator({'b': 2})
        config1.merge(config2)
        self.assertEqual(config1.to_dict(), {'a': 1, 'b': 2})

    def test_merge_with_nested_config(self):
        config1 = BaseConfigurator({'a': {'b': 1}})
        config2 = BaseConfigurator({'a': {'c': 2}})
        config1.merge(config2)
        self.assertEqual(config1.to_dict(), {'a': {'b': 1, 'c': 2}})

    def test_merge_with_different_types(self):
        config1 = BaseConfigurator({'a': 1})
        config2 = BaseConfigurator({'a': 'string'})
        config1.merge(config2)
        self.assertEqual(config1.to_dict(), {'a': 'string'})

    def test_set_item(self):
        config = BaseConfigurator()
        config['attr1'] = 1
        self.assertEqual(config.attr1, 1)

    def test_set_attr(self):
        config = BaseConfigurator()
        config.attr1 = 1
        self.assertEqual(config['attr1'], 1)

    def test_singleton_instance(self):
        config1 = BaseConfigurator({'a': 1}, singleton=True)
        config2 = BaseConfigurator({'b': 2}, singleton=True)

        self.assertIs(config1, config2)
        self.assertEqual(config1.b, 2)

    def test_non_singleton_instance(self):
        config1 = BaseConfigurator({'a': 1})
        config2 = BaseConfigurator({'b': 2})
        self.assertIsNot(config1, config2)
        self.assertIsNone(config1.__dict__.get('b'))

    def test_mixed_singleton_and_non_singleton_instances(self):
        config1 = BaseConfigurator({'a': 1}, singleton=True)
        config2 = BaseConfigurator({'b': 2}, singleton=False)
        config3 = BaseConfigurator({'c': 3}, singleton=True)

        self.assertIsNot(config1, config2)
        self.assertIs(config1, config3)
        self.assertEqual(config1.c, 3)
