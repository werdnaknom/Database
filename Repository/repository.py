from Entities.Entities import ProjectEntity
# from config import REPOSITORYFILTER, REPOSITORYOPERATORS, VALIDFILTERS
# from config import DATADIRECTORY, PICKLEDIRECTORY
from pathlib import Path

from Entities.Entities import Entity
from config import Config


class Repository(object):
    def __init__(self, entries=None):
        self._filters = Config.REPOSITORYFILTER
        # self._filters = VALIDFILTERS
        self._operators = Config.REPOSITORYOPERATORS
        self._entries = []
        if entries:
            self._build_entries(entries=entries)

    @property
    def filters(self):
        return self._filters

    @property
    def operators(self):
        return self._operators

    def _build_entries(self, entries):
        assert isinstance(entries, list), "'{}' must be of type list".format(entries)
        for entry in entries:
            if isinstance(entry, ProjectEntity):
                self._entries.append(entry)
            elif isinstance(entry, dict):
                p = ProjectEntity._from_dict(entry)
                self._entries.append(p)
            else:
                raise TypeError('{} must be of type Product or product dict'.format(entry))

    def _get_entries(self):
        return self._entries

    def entry_descriptors(self):
        descriptors = [e.descriptor for e in self._get_entries()]
        return descriptors

    def list(self, filters=None):
        if not filters:
            results = self.entry_descriptors()
        else:
            repo_filters = self._get_repository_filters(filters_dict=filters)
            if repo_filters:
                results = []
                results.extend(self._get_entries())
                for repo_key in repo_filters:
                    value = filters.pop(repo_key)
                    if repo_key.split("__")[0] == "dut":
                        results = [e for e in results if
                                   self._check(e.descriptor.upper(), key=repo_key, value=value.upper())]
                    else:
                        results = [e for e in results if self._check(e.descriptor, key=repo_key, value=value)]
            else:
                raise KeyError('{} not in filters: {}!'.format(self.filters, filters))

            # if there are any remaining filters, go to the entities to sort it out
            if filters:
                entity_results = []
                for result in results:
                    assert isinstance(result, Entity)
                    entity_results.extend(result.list(filters=filters))
                results = entity_results
        return results

    def _check(self, entity_descriptor, key, value):
        key, operator = self.separate_key_from_operators(filter_key=key)

        if operator not in self.operators:
            raise ValueError('Operator {} is not supported'.format(operator))

        operator = '__{}__'.format(operator)

        if key.lower() in self.filters:
            '''
            Only applicable filter is dut, which is the entity descriptor
            '''
            return getattr(entity_descriptor, operator)(value)
        else:
            raise KeyError('"{}" is not a valid key'.format(key))

    @staticmethod
    def separate_key_from_operators(filter_key):
        if '__' not in filter_key:
            filter_key = filter_key + '__eq'
        key, operator = filter_key.split('__')
        return key, operator

    def _get_repository_filters(self, filters_dict):
        filters = []
        for key in filters_dict.keys():
            new_key, operator = self.separate_key_from_operators(filter_key=key)
            if new_key == self.filters:
                filters.append(key)
        return filters


class DirectoryRepository(Repository):
    def __init__(self, repository_directory=Config.DATADIRECTORY):
        assert not isinstance(repository_directory, list), \
            "repository directory cannot be type list. must be path or Path. '{}'".format(repository_directory)
        self.structure = ProductDirectoryEntityBuilder
        super(DirectoryRepository, self).__init__(entries=[repository_directory])
        self._directory = repository_directory

    @property
    def directory(self):
        return self._directory

    def _build_entries(self, entries):
        assert isinstance(entries, list), "'{}' must be of type list".format(entries)
        for entry in entries:
            try:
                '''Each entry will be a ProductDirectory under the repository directory'''
                entry = Path(entry)
                self._entries.extend([self.structure(directory=p_dir)
                                      for p_dir in entry.iterdir()
                                      if p_dir.is_dir()])
            except TypeError as e:
                raise TypeError('{} must be path string or Path, Exception: {}'.format(entry, e))

    def entry_descriptors(self):
        product_names = [d.name for d in self._get_entries()]
        return product_names

    def list(self, filters=None):
        if not filters:
            result = self.entry_descriptors()
        else:
            result = []
            entities = []
            dut_keys = [key for key in filters.keys() if self.separate_key_from_operators(filter_key=key)[0] == "dut"]

            for key in dut_keys:
                dut_value = filters.pop(key)
                for entity_builder in self._get_entries():
                    if self._check(entity_descriptor=entity_builder.descriptor.upper(), key=key,
                                   value=dut_value.upper()):
                        entities.extend(entity_builder.build_entities())
            for entity in entities:
                result.extend(entity.list(filters))
        return result

    def format(self, entity_descriptor):
        formatted = entity_descriptor.lower()
        return formatted

    def check_age(self, entity_descriptor):
        max_age = -1
        formatted_descriptor = self.format(entity_descriptor)
        product_paths_list = [path for path in self._get_entries()
                              if path.name.lower() == formatted_descriptor]
        if product_paths_list:
            for product in product_paths_list:
                max_age = max(product.get_age(), max_age)
        return max_age


class PickleRepository(Repository):
    def __init__(self, pickle_directory=PICKLEDIRECTORY):
        assert not isinstance(pickle_directory, list), \
            "repository directory cannot be type list. must be path or Path. '{}'".format(pickle_directory)
        self.structure = PickleEntityBuilder
        super(PickleRepository, self).__init__(entries=[pickle_directory])
        self._directory = pickle_directory

    @property
    def directory(self):
        return self._directory

    def _build_entries(self, entries):
        assert isinstance(entries, list), "'{}' must be of type list".format(entries)
        for entry in entries:
            try:
                entry = Path(entry)
                self._entries.extend([self.structure(p_dir) for p_dir in entry.iterdir()
                                      if p_dir.is_file() and p_dir.suffix == ".pickle"])
            except TypeError as e:
                raise TypeError('{} must be path string or Path, Exception: {}'.format(entry, e))

    def entry_descriptors(self):
        product_names = [d.product_name for d in self._get_entries()]
        return product_names

    def write_entity_to_pickle(self, entity):
        pickle_directory = self.directory
        pickle_path = self.structure.write_entity_to_pickle(pickle_directory=pickle_directory, entity=entity)
        return pickle_path

    def format(self, entity_descriptor):
        formatted = self.structure.format_pickle_name(product_name=entity_descriptor)
        return formatted

    def check_age(self, entity_descriptor):
        max_age = -1
        for entry in self._get_entries():
            if entry.product_name.upper() == entity_descriptor.upper():
                age = entry.get_age()
                max_age = max(max_age, age)
        return max_age

    def list(self, filters=None):
        if not filters:
            result = self.entry_descriptors()
        else:

            entity_builder_list = self._get_entries()
            for key_op, value in filters.items():
                key, _ = self.separate_key_from_operators(filter_key=key_op)
                if key == "dut":
                    filters.pop(key_op)
                    pickle_result_list = [entity_builder for entity_builder in entity_builder_list if
                                          self._check(entity_builder.descriptor.upper(), key=key_op,
                                                      value=value.upper())]
                    break
            result = []
            for pickled_entity in pickle_result_list:
                entity_list = pickled_entity.build_entities()
                for entity in entity_list:
                    result.extend(entity.list(filters=filters))

            # for key, value in filters.items():
            #    entities = self._get_entries()
            #    for entity_builder in self._get_entries():
            #        if self._check(entity_descriptor=entity_builder.descriptor, key=key, value=value):
            #            result.extend(entity_builder.build_entities())
        return result
