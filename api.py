#Flask est un framework web minimaliste utilisé pour créer des applications web en Python.
#Flask-RESTful est une extension de Flask qui facilite la création d'API RESTful.
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, marshal_with
from flask_mongoengine import MongoEngine

'''
#SQLAlchemy est une bibliothèque Python populaire qui facilite l'interaction avec des bases de données relationnelles. Elle fournit une interface de programmation objet pour travailler avec des bases de données, en utilisant le langage de requête SQL.
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__) #créer une instance de l'application Flask. Le paramètre __name__ est utilisé pour spécifier le nom de l'application.
api = Api(app) # créer une instance de l'API Flask-RESTful en utilisant l'application Flask créée précédemment. L'API est utilisée pour ajouter des ressources et définir les routes de l'API.
'''
#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sqlite.db'
#db = SQLAlchemy(app)
'''
class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    summary = db.Column(db.String(500))
'''
#db.create_all()
'''
'''
#Une ressource représente généralement une entité du monde réel, telle qu'un utilisateur, un produit, un article de blog, etc., qui peut être manipulée à l'aide des opérations CRUD (Create, Read, Update, Delete) via l'API.
#Ce code définit une classe HelloWorld qui hérite de la classe Resource du module Flask-RESTful. La classe Resource fournit une base pour créer des ressources dans une API RESTful.
'''
class HelloWorld(Resource):
    def get(self):
        #Lorsqu'une requête GET est effectuée à cette route, la méthode get est appelée et elle renvoie un dictionnaire JSON contenant la clé "data" avec la valeur "Hello, World!".
        return {'data': 'Hello, World!'}
'''
'''
class HelloName(Resource):
    def get(self, name):
        return {'data': 'Hello, {}'.format(name)}
'''
'''
api.add_resource(HelloWorld,'/helloworld')
api.add_resource(HelloName,'/helloworld/<string:name>')
'''
app = Flask(__name__)
api = Api(app)
app.config['MONGODB_SETTINGS']={
    'db': 'todomodel',
    'host':'localhost',
    'port':27017
}
db = MongoEngine()
db.init_app(app)

class Todomodel(db.Document):
    _id = db.IntField()
    task = db.StringField(required=True)
    summary = db.StringField(required=True)

todos = {
    1: {"task": "Write Hello world program", "summary":"write the code using python."},
    2: {"task": "task 2", "summary":"summary3."},
    3: {"task": "task 3", "summary":"summary3."}
}

task_post_args = reqparse.RequestParser()
task_post_args.add_argument("task", type=str, help="Task is required", required=True)
task_post_args.add_argument("summary", type=str, help="Summary is required", required=True)

task_upgrade_args = reqparse.RequestParser()
task_upgrade_args.add_argument("task", type=str)
task_upgrade_args.add_argument("summary", type=str)

resource_fields = {
    '_id': fields.Integer,
    'task':fields.String,
    'summary':fields.String,
}

class ToDoList(Resource):
    def get(self):
        return todos
    
class ToDo(Resource):
    #so that the response returned will be serializable, in a json format
    @marshal_with(resource_fields)
    def get(self,todo_id):
        #return todos[todo_id]
        task = Todomodel.objects.get(_id=todo_id)
        if not task:
            abort(404,message= "could not find task with that id")
        return task 
    
    @marshal_with(resource_fields)
    def post(self, todo_id):
        args = task_post_args.parse_args()
        '''
        if todo_id in todos:
            abort(409,"Task ID already taken")
        todos[todo_id] = {"task": args["task"],"summary":args["summary"]}
        return todos[todo_id]
        '''
        todo = Todomodel(_id=todo_id, task=args['task'],summary=args['summary']).save()
        return todo, 200
    
    @marshal_with(resource_fields)
    def put(self, todo_id):
        args = task_upgrade_args.parse_args()
        if args['task']:
            Todomodel.objects.get(_id=todo_id).update(task=args['task'])
        if args['summary']:
            Todomodel.objects.get(_id=todo_id).update(task=args['summary'])
        return "{} updated!".format(todo_id), 200

    @marshal_with(resource_fields)
    def delete(self, todo_id):
        #del todos[todo_id]
        Todomodel.objects.get(_id=todo_id).delete()
        return "Task Deleted!", 204

api.add_resource(ToDo,'/todos/<int:todo_id>')
api.add_resource(ToDoList,'/todos')
#Ce code est utilisé pour exécuter l'application Flask lorsque le fichier est exécuté directement (c'est-à-dire pas en tant que module importé).
if __name__ == '__main__':
    app.run(debug=True) #lance le serveur de développement intégré de Flask et écoute les requêtes entrantes. L'argument debug=True active le mode de débogage, ce qui signifie que vous obtiendrez des informations de débogage détaillées en cas d'erreur.

