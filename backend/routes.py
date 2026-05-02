from flask import request, jsonify
from .app import db
from .models import User, Lesson, Progress
from flask import current_app as app

import os
import signal
import psutil
from flask import request, jsonify

@app.route('/api/system/stop', methods=['POST'])
def stop_app():
    # Write a trigger file for the batch script to exit
    with open('stop.trigger', 'w') as f:
        f.write('stop')
    
    # Kill frontend (node/vite)
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == 5175: # Frontend port
                    proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
            
    # Kill self (backend)
    os.kill(os.getpid(), signal.SIGTERM)
    return jsonify({'status': 'stopping'})

@app.route('/api/system/restart', methods=['POST'])
def restart_app():
    # Write a trigger file for the batch script to restart
    with open('restart.trigger', 'w') as f:
        f.write('restart')
        
    # Kill frontend
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == 5175:
                    proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Kill self
    os.kill(os.getpid(), signal.SIGTERM)
    return jsonify({'status': 'restarting'})

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
        # Level 1: Home Row Mastery
        Lesson(title='Home Row - Basic', content='arst neio', level=1),
        Lesson(title='Home Row - DH Focus', content='astg neio m', level=1),
        Lesson(title='Home Row - Common Bigrams', content='th he an in er re on at en nd st es', level=1),
        Lesson(title='Home Row - Short Words', content='star rain note nest near sent east area sane', level=1),
        Lesson(title='Home Row - Fluency', content='the rain in spain stays mainly in the plain', level=1),

        # Level 2: Top Row Integration
        Lesson(title='Top Row - Left Hand', content='qwfpg arst', level=2),
        Lesson(title='Top Row - Right Hand', content='jluy; neio', level=2),
        Lesson(title='Top Row - Mixed', content='quick flow glad play jump wolf quay', level=2),
        Lesson(title='Top Row - DH Precision', content='page find peak grow just long your year', level=2),
        Lesson(title='Top Row - Sentences', content='the quick brown fox jumps over the lazy dog', level=2),

        # Level 3: Bottom Row & Punctuation
        Lesson(title='Bottom Row - Basic', content='zxc dv kh , . /', level=3),
        Lesson(title='Bottom Row - Words', content='dock back view size zone kind half calm', level=3),
        Lesson(title='Bottom Row - Integration', content='every day is a new chance to learn and grow', level=3),
        Lesson(title='Punctuation - Basic', content='hello, world! how are you today? (fine.)', level=3),
        Lesson(title='Punctuation - Advanced', content='it\'s "great" to see you; let\'s start!', level=3),

        # Level 4: High Frequency & Speed
        Lesson(title='Top 100 Words - Part 1', content='the be of and a to in of it for not on with he as you do', level=4),
        Lesson(title='Top 100 Words - Part 2', content='at this but his by from they we say her she or an will my', level=4),
        Lesson(title='Trigram Mastery', content='the and ing her hat his tha ere for ent ion ter was', level=4),
        Lesson(title='Double Letters', content='tell well keep book look feel seen soon moon summer', level=4),

        # Level 5: Prose & Real World
        Lesson(title='Prose - Philosophy', content='to be or not to be, that is the question of the soul.', level=5),
        Lesson(title='Prose - Technology', content='artificial intelligence is the future of human computer interaction.', level=5),
        Lesson(title='Prose - Nature', content='the mountains are calling and i must go to the peak.', level=5),

        # Level 6: Coding & Numbers
        Lesson(title='Numbers - Row 1', content='12345 67890 54321 09876', level=6),
        Lesson(title='Coding - Python', content='import os, sys; print("path:", os.getcwd())', level=6),
        Lesson(title='Coding - CSS', content='body { margin: 0; padding: 20px; display: flex; }', level=6),
        Lesson(title='Coding - HTML', content='<div class="main"><h1>Hello World</h1></div>', level=6),

        # Level 7: Master Challenges
        Lesson(title='Mastery - Long Text', content='four score and seven years ago our fathers brought forth on this continent a new nation conceived in liberty and dedicated to the proposition that all men are created equal.', level=7),
        Lesson(title='Mastery - Colemak DH Stress', content='bright green plants grow high above the dark deep valley below.', level=7),
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
