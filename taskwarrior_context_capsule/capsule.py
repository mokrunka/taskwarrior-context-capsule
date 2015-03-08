from taskwarrior_capsules.capsule import CommandCapsule
from taskwarrior_capsules.exceptions import CapsuleError
from taskwarrior_capsules.data import BUILT_IN_COMMANDS


class Context(CommandCapsule):
    """ Backports 'context' command Taskwarrior 2.4.2."""

    MIN_VERSION = '0.2.5'
    MAX_VERSION = '1.0'
    MIN_TASKWARRIOR_VERSION = '2.3'
    MAX_TASKWARRIOR_VERSION = '2.4.1.99999'

    def handle(self, filter_args, extra_args, **kwargs):
        try:
            first_arg = extra_args[0].lower()
        except IndexError:
            raise CapsuleError("No context command specified")

        if first_arg == 'none':
            self.clear_context(extra_args[1:])
        elif first_arg == 'delete':
            self.delete_context(extra_args[1:])
        elif first_arg == 'list':
            self.list_contexts(extra_args[1:])
        elif first_arg == 'show':
            self.show_context(extra_args[1:])
        elif first_arg == 'define':
            self.define_context(extra_args[1:])
        else:
            self.set_context(extra_args)

        self.configuration.write()

    def preprocess(self, filter_args, extra_args, command_name=None, **kwargs):
        try:
            context = self.configuration['current_context']
            is_report = command_name not in BUILT_IN_COMMANDS
            if is_report and context:
                context_filters = self._get_contexts()[context]
                filter_args.append('(%s)' % context_filters)
        except KeyError:
            pass
        return filter_args, extra_args, command_name

    # Utility methods

    def clear_context(self, args):
        self.configuration['current_context'] = ''

    def delete_context(self, args):
        ctx = self._get_contexts()
        context_name = self._collapse(args)
        if context_name in ctx:
            del ctx[context_name]
        else:
            raise CapsuleError(
                "Context '%s' does not exist" % context_name
            )

    def list_contexts(self, args):
        ctx = self._get_contexts()
        for context_name, context in ctx.items():
            print '%s\t%s' % (context_name, context)

    def show_context(self, args):
        print self.configuration.get('current_context', '')

    def define_context(self, args):
        context_name = args[0]
        spec = self._collapse(args[1:])

        contexts = self._get_contexts()
        contexts[context_name] = spec
        self._set_contexts(contexts)

    def set_context(self, args):
        context_name = self._collapse(args)
        if context_name in self._get_contexts():
            self.configuration['current_context'] = context_name
        else:
            raise CapsuleError(
                "Context '%s' does not exist" % context_name
            )

    def _get_contexts(self):
        if 'contexts' not in self.configuration:
            self.configuration['contexts'] = {}
        return self.configuration['contexts']

    def _set_contexts(self, ctx):
        self.configuration['contexts'] = ctx

    def _collapse(self, args):
        return ' '.join(args)
