import pandas as pd
import json

from flask import jsonify
from flask import current_app as app, request

from app.models.guest_models import GuestList
from app.api import blueprint


@blueprint.route('/backend/message-generator/template/<surname>', methods=['GET'])
def message_generator(surname):

    template_message = "Halo tes {}".format(surname)

    return template_message


@blueprint.route('/backend/guest-list/_upload', methods=['POST'])
def upload_csv():
    file = request.files['file']
    app.logger.info("file: {}".format(file))
    df = pd.read_csv(file, sep=';')
    app.logger.info("data: {}".format(df))

    data_json = json.loads(df.to_json(orient='records'))

    for data in data_json:
        guest = GuestList(invitation_code=str(data['invitation_code']),
                          name=data['name'],
                          group=data['group'],
                          phone=str(data['phone']))
        guest.save()

    return jsonify({"status": 200, "message": "success"})


@blueprint.route('/backend/guest-list/_delete', methods=['DELETE'])
def delete_guest_list():
    guest = GuestList.objects
    guest.delete()

    return jsonify({"status": 200, "message": "success"})
