# -*- encoding: utf-8 -*-

from pathlib import Path

from . import generic


class ModelInput(generic.ModelInput):
    """A NONMEM 7.x model $INPUT class"""

    def column_names(self):
        """Gets a list of the column names of the input dataset

        Limitation: Tries to create unique symbol for anonymous columns, but
        only uses the INPUT names.
        """
        records = self.model.get_records('INPUT')
        all_symbols = []
        for record in records:
            pairs = record.ordered_pairs()
            for key in pairs:
                all_symbols.append(key)
                if pairs[key]:
                    all_symbols.append(key)
        names = []
        for record in records:
            pairs = record.ordered_pairs()
            for key, value in pairs.items():
                if key == 'DROP' or key == 'SKIP':
                    names.append(all_symbols, 'DROP')
                else:
                    names.append(key)
        return names

    @property
    def path(self):
        data_records = self.model.get_records('DATA')
        pairs = data_records[0].ordered_pairs()
        first_pair = next(iter(pairs.items()))
        path = Path(first_pair[0]).resolve()
        return path