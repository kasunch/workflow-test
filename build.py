from cpt.packager import ConanMultiPackager
from cpt.ci_manager import CIManager
from cpt.printer import Printer
import os, sys, re, traceback, configparser

def hidesensitive(output):
    output_str = str(output)
    output_str = re.sub(r'(CONAN_LOGIN_USERNAME[_\w+]*)=\"(\w+)\"', r'\1="xxxxxxxx"', output_str)
    output_str = re.sub(r'(CONAN_PASSWORD[_\w+]*)=\"(\w+)\"', r'\1="xxxxxxxx"', output_str)
    sys.stdout.write(output_str)

def get_name_and_version():
    parser = configparser.ConfigParser()
    parser.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "project.conf"))
    name = parser["conanfile"]["name"]

    printer = Printer(hidesensitive)
    ci_man = CIManager(printer)
    version = re.sub(".*/", "", ci_man.get_branch())

    return name, version

if __name__ == "__main__":
    try:
        builder = ConanMultiPackager(reference="%s/%s" % get_name_and_version(), out=hidesensitive)
        builder.add_common_builds(pure_c=False)
        builder.run()
    except Exception as e:
        hidesensitive(traceback.format_exc())
        hidesensitive(str(e))
        sys.exit(1)
