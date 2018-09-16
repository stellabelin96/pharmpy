# -*- encoding: utf-8 -*-
"""
===================
Generic Model class
===================

**Parent to all implementations.**

Inherit to *implement*, i.e. to define support for a specific model type. Duck typing is utilized,
but an implementation is expected to implement **all** methods/attributes.

Definitions
-----------
"""

from pathlib import Path

from pharmpy import output  # TODO: ModelEstimation uses 'import generic; generic.output.XXX'
from pharmpy.input import ModelInput
from pharmpy.output import ModelOutput
from pharmpy.parameters import ParameterModel
from pharmpy.execute import Engine


def detect(lines):
    return False


class ModelException(Exception):
    pass


class ModelParsingError(ModelException):
    def __init__(self, msg='model parse error'):
        super().__init__(msg)


class ModelLookupError(LookupError):
    def __init__(self, lookup):
        self.lookup = lookup
        try:
            reason = 'index %d out of range' % (self.lookup,)
        except TypeError:
            reason = 'name %s not found' % (repr(str(self.lookup)),)
        msg = 'submodel does not exist (%s)' % (reason,)
        super().__init__(msg)


class Model(object):
    """(Generic) Model class.

    Represents a model file object, that may or may not exist on disk too.

    Attributes:
        self.input: Instance of (model API) :class:`~pharmpy.input.ModelInput` (e.g. data).
        self.output: Instance of (model API) :class:`~pharmpy.output.ModelOutput` (results of
            evaluation, estimation or simulations).
        self.parameters: Instance of (model API) :class:`~pharmpy.parameters.ParameterModel` (e.g.
            parameter estimates or initial values).
        self.execute: Instance of (model API) :class:`~pharmpy.execute.Engine` (executing evaluation,
            estimation or simulation).
    """

    _path = None
    _index = 0

    def __init__(self, path):
        self._path = Path(path).resolve() if path else None
        if self.exists:
            self.read()

    @property
    def index(self):
        """Current model (subproblem) index.

        The context for everything else changes if changed. Implementation might accept name lookup.
        """
        return self._index

    @index.setter
    def index(self, new):
        if new != 0:
            raise ModelLookupError(new)
        self._index = new

    @property
    def exists(self):
        """True *if and only if* model exists on disk."""
        if self.path and self.path.is_file():
            return True

    @property
    def content(self):
        """Raw content stream of model."""
        if not self.exists:
            return None
        with open(str(self.path), 'r') as f:
            content = f.read()
        return content

    def validate(self):
        """Test if model is syntactically valid (raises if not)."""
        raise NotImplementedError

    def read(self):
        """Read model from disk.

        Initiates all the API:s of the Model, e.g. :class:`~pharmpy.input.ModelInput`,
        :class:`~pharmpy.input.ModelOutput` and :class:`~pharmpy.parameters.ParameterModel`.
        """
        self.input = ModelInput(self)
        self.output = ModelOutput(self)
        self.parameters = ParameterModel(self)
        self.execute = Engine(self)
        self.validate()

    def write(self, path):
        """Write model to disk.

        .. todo:: Start implementing Model write. Will require thoughts on how to "bootstrap" up a
            rendering of the low-level objects (e.g. every ThetaRecord, etc.).
        """
        raise NotImplementedError

    @property
    def path(self):
        """File path of the model."""
        return self._path

    @path.setter
    def path(self, path):
        if self._path:
            import pdb; pdb.set_trace()  # noqa
            rel = self._path.relative(path)
            print(rel)
        self._path = path

    @property
    def has_results(self):
        """True *if and only if* model has results.

        Must be True for accessing :class:`~pharmpy.output.ModelOutput`.

        .. todo::
            Implement model execution/results status checker.
            **Should** contain a call to :class:`.engine` class. An implementation of *that* should
            then know how to check on current platform/cluster system (also *without* initializing a
            run directory).
            **Shouldn't** need to override this (by implementation).
        """
        return True

    def __repr__(self):
        path = None if self.path is None else str(self.path)
        return "%s(%r)" % (self, path)

    def __str__(self):
        if self.exists:
            return self.content

    def __deepcopy__(self, memo):
        """Copy model completely.

        Utilized by e.g. :class:`pharmpy.execute.run_directory.RunDirectory` to "take" the model in a
        dissociated state from the original.

        .. note::
            Lazy solution with re-parsing path for now. Can't deepcopy down without implementing
            close to Lark tree's, since compiled regexes must be re-compiled.

            .. todo:: Deepcopy Model objects "correctly"."""
        if self.exists:
            return type(self)(self.path)
        elif self.content is not None:
            raise NotImplementedError("Tried to (deeply) copy %r without path but content; "
                                      "Not yet supported" % (self,))