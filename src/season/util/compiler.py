import inspect
import season

from flask import request, abort
import datetime
import traceback
import sys

class compiler:
    def __init__(self, fn=None):
        self.fn = fn
    
    def build(self, code, name=None, logger=print, **kwargs):
        fn = {'__file__': name, '__name__': name, 'print': logger, 'season': season}
        for key in kwargs: fn[key] = kwargs[key]
        try:
            if type(code) == str:
                exec(compile(code, name, 'exec'), fn)
            else:
                exec(code, fn)
        except season.lib.exception.ResponseException as e:
            raise season.lib.exception.ResponseException(e.code, e.response)
        except Exception as e:
            error_type = type(e).__name__
            if error_type != "InternalServerError":
                tb = traceback.TracebackException(*sys.exc_info())
                filtered = []
                for entry in tb.stack:
                    if entry.filename.endswith("/site-packages/season/util/compiler.py"):
                        continue
                    filtered.append(f'  File "\033[1m{entry.filename}\033[0m", line \033[1m{entry.lineno}\033[0m, in {entry.name}\n    {entry.line}')
                if filtered:
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print("\033[91m[{now}][ERROR][http][error]\033[0m {uri}".format(now=now, uri=request.path))
                    print("Traceback (most recent call last):")
                    print("\n".join(filtered))
                    print(f"{error_type}: {str(e)}")
                else:
                    # fallback: show last frame of traceback
                    traceback.print_exc()
            abort(500, description="")
        self.fn = fn
        return self
    
    def __call__(self, **kwargs):
        return self.call(**kwargs)

    def call(self, **kwargs):
        if self.fn is None:
            raise Exception("Compiler is not initialized")
        
        fn = self.fn
        args = inspect.getfullargspec(fn).args
        if len(args) > 0:
            if args[0] == 'self':
                args = args[1:]

        for i in range(len(args)):
            key = args[i]
            if key in kwargs: 
                args[i] = kwargs[key]
            else:
                args[i] = None
        
        return fn(*args)
