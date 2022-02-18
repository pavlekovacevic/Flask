from flask import  jsonify, make_response, request
import uuid
from marshmallow.validate import Length,Range
from marshmallow import Schema,fields,ValidationError
from flask import Flask,request
import datetime

app = Flask(__name__)

NOTES = {}

class CreateNoteInputSchema(Schema):
    title = fields.Str(required = True, validate=Length(max = 20))
    note = fields.Str(required = True, validate = Length(max=100))
    user_id = fields.Int(required = True, validate = Range(min=1))
    
noteinputschema = CreateNoteInputSchema()


@app.route('/api/note')
def get_notes():
    return jsonify(NOTES)


@app.route('/api/note', methods=['POST'])
def add_note():
    uid = uuid.uuid4()
    date = datetime.datetime.now()
    req_data = request.json

    try:
        req_data = noteinputschema.load(req_data)
    except ValidationError as err:
        return err.messages, 400
    
    req_data['time_created'] = date
    NOTES[str(uid)] = req_data
    
    return req_data


@app.route('/api/note/<uuid>')
def get_single(uuid):
    if not uuid in NOTES:
        return 'No matching uuid', 404
    
    return jsonify(NOTES[uuid])
    


@app.route('/api/note/<uuid>', methods = ['PATCH'])
def update_note_uuid(uuid):
    req_data = request.json
    if not uuid in NOTES:
        return 'No matching uuid', 404
   
    
    first_dict = NOTES[uuid]
    res = {key: req_data.get(key, first_dict[key]) for key in first_dict}
    
    date = datetime.datetime.now()   
    res['time_updated'] = date
    
    
    return res
        

@app.route('/api/note/<uuid>', methods = ['DELETE'])
def delete_note_uuid(uuid):
    
    if not uuid in NOTES:
        return 'No matching uuid', 404
    delete_note_by_uuid = NOTES[uuid]
    delete_note_by_uuid.clear()
    res = make_response(jsonify({'message':'Note deleted'}), 200)
    
    return res
    
    

app.run()