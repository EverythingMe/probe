from json import JSONEncoder
import json
import datetime
import os

from probe import config
from ..helpers.logger import logger

__author__ = 'rotem'


class JSONBasicEncoder(JSONEncoder):
        def default(self, obj):
            return obj.__dict__

#obj must include 'app_version' in its dictionary
def gen_json(objname, test_name, package_name, obj):
    json_string = json.dumps(obj, separators=(',', ':'), ensure_ascii=False, cls=JSONBasicEncoder)
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    json_output_dir = config.JSON_OUTPUT_DIR
    if not os.path.exists(json_output_dir):
        os.makedirs(json_output_dir)

    file_path = os.path.join(json_output_dir, '%s_%s_%s_%s_%s.%s' % (objname, package_name, obj.build_number, test_name, timestamp, 'json'))

    text_file = open(file_path, 'w')
    text_file.write(json_string)
    logger.debug('%s output json file created in %s' % (objname, file_path))
    text_file.close()

    return json_string