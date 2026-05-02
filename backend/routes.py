from flask import request, jsonify
from .app import db
from .models import User, Lesson, Progress
from flask import current_app as app

@app.route('/api/lessons', methods=['GET'])
def get_lessons():
    lessons = Lesson.query.all()
    return jsonify([{'id': l.id, 'title': l.title, 'content': l.content, 'level': l.level} for l in lessons])

@app.route('/api/user/progress', methods=['POST'])
def save_progress():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        user = User(username=data['username'])
        db.session.add(user)
        db.session.commit()
    
    progress = Progress(
        user_id=user.id,
        lesson_id=data['lesson_id'],
        wpm=data['wpm'],
        accuracy=data['accuracy']
    )
    db.session.add(progress)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/api/user/progress/<username>', methods=['GET'])
def get_progress(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify([])
    
    progress = Progress.query.filter_by(user_id=user.id).all()
    return jsonify([{
        'lesson_id': p.lesson_id,
        'wpm': p.wpm,
        'accuracy': p.accuracy,
        'completed_at': p.completed_at.isoformat()
    } for p in progress])

@app.route('/api/seed', methods=['POST'])
def seed_data():
    # Clear existing lessons for a fresh seed
    Lesson.query.delete()
    db.session.commit()
    
    lessons = [
        # Level 1: Home Row
        Lesson(title='Home Row - Basic', content='arst neio', level=1),
        Lesson(title='Home Row - Extended', content='arst g m neio', level=1),
        Lesson(title='Home Row - Words', content='star stare rain note nest near sent east', level=1),
        
        # Level 2: Top Row
        Lesson(title='Top Row - Basic', content='qwfpg jluy', level=2),
        Lesson(title='Top Row - Words', content='play plug jump flow glad flip quay wolf', level=2),
        Lesson(title='Home + Top', content='the quick brown fox jumps over the lazy dog', level=2),
        
        # Level 3: Bottom Row
        Lesson(title='Bottom Row - Basic', content='zxc dv kh , . /', level=3),
        Lesson(title='Bottom Row - Words', content='dock back view size zone kind half', level=3),
        
        # Level 4: Full Mastery
        Lesson(title='Common Sentences', content='practice makes perfect for everyone. typing is a useful skill to have in the modern world.', level=4),
        Lesson(title='Code Fragments', content='def hello_world(): print("Hello Colemak!")', level=4),
    ]
    db.session.bulk_save_objects(lessons)
    db.session.commit()
    return jsonify({'status': 'seeded'})

@app.route('/api/custom-lesson', methods=['POST'])
def create_custom_lesson():
    data = request.json
    # We create a temporary lesson for the session
    lesson = Lesson(
        title=data.get('title', 'Custom Practice'),
        content=data.get('content'),
        level=99 # Special level for custom
    )
    # Note: We don't necessarily need to save it to DB if it's just for one session, 
    # but for simplicity in current architecture we can, or just return it.
    # Let's just return a mock object for the frontend to use.
    return jsonify({
        'id': 999,
        'title': lesson.title,
        'content': lesson.content,
        'level': 99
    })
