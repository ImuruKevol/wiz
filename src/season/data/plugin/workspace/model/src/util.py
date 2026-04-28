import season
import subprocess

class Model:
    @staticmethod
    def _is_warning_stderr(message):
        normalized_message = message.lower()
        warning_tokens = [
            "npm warn",
            "npm notice",
            "- installing packages (npm)",
            "▲ [warning]",
            "node.js version ",
            "odd numbered node.js versions",
            "the 'vendorchunk' option is not used by this builder and will be ignored.",
        ]
        error_tokens = [
            "✘ [error]",
            "fatal error:",
            "application bundle generation failed.",
        ]

        if any(token in normalized_message for token in error_tokens):
            return False

        return any(token in normalized_message for token in warning_tokens)

    @staticmethod
    def execute(cmd, log=True):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()

        if log:
            if out is not None and len(out) > 0:
                out = out.decode('utf-8').strip()
                wiz.logger('build/log')(out)
            if err is not None and len(err) > 0:
                err = err.decode('utf-8').strip()
                if Model._is_warning_stderr(err):
                    wiz.logger('build/log')(err, level=season.LOG_WARNING)
                else:
                    wiz.logger('build/error')(err, level=season.LOG_CRITICAL)

        return p.returncode

    @staticmethod
    def is_working(fs, timestamp):
        try:
            if fs.exists("build/working"):
                timestampLog = int(fs.read("build/working"))
                if timestamp - timestampLog < 5000:
                    fs.write("build/working", str(timestamp))
                    return True
        except:
            return True
        fs.write("build/working", str(timestamp))
        return False

    @staticmethod
    def is_work_finish(fs, timestamp):
        if fs.exists("build/working"):
            timestampLog = int(fs.read("build/working"))
            fs.remove("build/working")
            if timestamp < timestampLog:
                return False
        return True