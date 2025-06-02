from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from datetime import datetime
from app import db
from app.models.task import Task
from app.utils.decorators import auth_required
from app.utils.validators import TaskSchema, TaskUpdateSchema

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
@auth_required
def get_tasks(current_user):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    priority = request.args.get('priority')
    
    query = Task.query.filter_by(user_id=current_user.id)
    
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    
    tasks = query.order_by(Task.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'tasks': [task.to_dict() for task in tasks.items],
        'total': tasks.total,
        'pages': tasks.pages,
        'current_page': page
    }), 200

@tasks_bp.route('/create_task', methods=['POST'])
@auth_required
def create_task(current_user):
    schema = TaskSchema()
    
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status=data.get('status', 'pending'),
        priority=data.get('priority', 'medium'),
        due_date=data.get('due_date'),
        user_id=current_user.id
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({
        'message': 'Task created successfully',
        'task': task.to_dict()
    }), 201

@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@auth_required
def update_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    
    schema = TaskUpdateSchema()
    
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    # Update task fields
    for field in ['title', 'description', 'status', 'priority', 'due_date']:
        if field in data:
            setattr(task, field, data[field])
    
    task.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Task updated successfully',
        'task': task.to_dict()
    }), 200

@tasks_bp.route('/tasks/delete/<int:task_id>', methods=['DELETE'])
@auth_required
def delete_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Task deleted successfully'}), 200