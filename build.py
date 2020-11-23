from cpt.packager import ConanMultiPackager
from cpt_helpers.build_helper import *

if __name__ == "__main__":
    try:
        builder = ConanMultiPackager(out=hidesensitive)
        builder.add_common_builds()
        builder.run()
    except Exception as e:
        hidesensitive(traceback.format_exc())
        hidesensitive(str(e))
        sys.exit(1)
