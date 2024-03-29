class ExtrasCandidate(Candidate):
    """A candidate that has 'extras', indicating additional dependencies.

    Requirements can be for a project with dependencies, something like
    foo[extra].  The extras don't affect the project/version being installed
    directly, but indicate that we need additional dependencies. We model that
    by having an artificial ExtrasCandidate that wraps the "base" candidate.

    The ExtrasCandidate differs from the base in the following ways:

    1. It has a unique name, of the form foo[extra]. This causes the resolver
       to treat it as a separate node in the dependency graph.
    2. When we're getting the candidate's dependencies,
       a) We specify that we want the extra dependencies as well.
       b) We add a dependency on the base candidate.
          See below for why this is needed.
    3. We return None for the underlying InstallRequirement, as the base
       candidate will provide it, and we don't want to end up with duplicates.

    The dependency on the base candidate is needed so that the resolver can't
    decide that it should recommend foo[extra1] version 1.0 and foo[extra2]
    version 2.0. Having those candidates depend on foo=1.0 and foo=2.0
    respectively forces the resolver to recognise that this is a conflict.
    """

    def __init__(self, base, extras):
        self.base = base
        self.extras = extras

    def __str__(self):
        name, rest = str(self.base).split(' ', 1)
        return '{}[{}] {}'.format(name, ','.join(self.extras), rest)

    def __repr__(self):
        return '{class_name}(base={base!r}, extras={extras!r})'.format(class_name=self.__class__.__name__, base=self.base, extras=self.extras)

    def __hash__(self):
        return hash((self.base, self.extras))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.base == other.base and self.extras == other.extras
        return False

    @property
    def project_name(self):
        return self.base.project_name

    @property
    def name(self):
        """The normalised name of the project the candidate refers to"""
        return format_name(self.base.project_name, self.extras)

    @property
    def version(self):
        return self.base.version

    def format_for_error(self):
        return '{} [{}]'.format(self.base.format_for_error(), ', '.join(sorted(self.extras)))

    @property
    def is_installed(self):
        return self.base.is_installed

    @property
    def is_editable(self):
        return self.base.is_editable

    @property
    def source_link(self):
        return self.base.source_link

    def iter_dependencies(self, with_requires):
        factory = self.base._factory
        yield factory.make_requirement_from_candidate(self.base)
        if not with_requires:
            return
        valid_extras = self.extras.intersection(self.base.dist.extras)
        invalid_extras = self.extras.difference(self.base.dist.extras)
        for extra in sorted(invalid_extras):
            logger.warning("%s %s does not provide the extra '%s'", self.base.name, self.version, extra)
        for r in self.base.dist.requires(valid_extras):
            requirement = factory.make_requirement_from_spec(str(r), self.base._ireq, valid_extras)
            if requirement:
                yield requirement

    def get_install_requirement(self):
        return None