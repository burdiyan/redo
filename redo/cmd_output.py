"""redo-output: track side-effects as generated files."""
import sys
import os
from . import env, logs, state
from .logs import err


def main():
    try:
        env.inherit()
        logs.setup(
            tty=sys.stderr, parent_logs=env.v.LOG,
            pretty=env.v.PRETTY, color=env.v.COLOR)

        me = os.path.join(env.v.STARTDIR,
                          os.path.join(env.v.PWD, env.v.TARGET))
        f = state.File(name=me)
        for t in sys.argv[1:]:
            if not t:
                err('cannot declare empty target as output ("").\n')
                sys.exit(204)
            if os.path.exists(t):
                tf = state.File(name=t)
                tf.mark_output(must_exist=True)
                tf.save()
                f.add_dep('m', t)
            else:
                tf = state.File(name=t)
                tf.mark_output(must_exist=False)
                tf.save()
                f.add_dep('m', t)
        state.commit()
    except KeyboardInterrupt:
        sys.exit(200)


if __name__ == '__main__':
    main()
