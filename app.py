from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Main homepage

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        subjects = []
        subject_count = 0
        
        # Extract subjects and their difficulties
        while True:
            subject_name = request.form.get(f'subject-{subject_count+1}')
            subject_difficulty = request.form.get(f'difficulty-{subject_count+1}')
            
            if not subject_name:  # Break if there are no more subjects
                break

            subjects.append((subject_name, subject_difficulty))
            subject_count += 1

        # Extract other data
        total_hours = int(request.form.get('total_hours'))
        learning_style = request.form.get('learning_style')
        study_time = request.form.get('study_time')
        break_interval = int(request.form.get('break_interval'))

        # Generate study schedule
        schedule = {}
        difficulty_weights = {'easy': 1, 'medium': 2, 'hard': 3}
        total_weight = sum(difficulty_weights[subj[1]] for subj in subjects)

        for subject, level in subjects:
            weight = difficulty_weights[level]
            allocated_hours = round((weight / total_weight) * total_hours, 1)  # Round to nearest tenth
            schedule[subject] = {
                'hours': allocated_hours,
                'learning_style': learning_style,
                'study_time': study_time,
                'break_interval': break_interval
            }

            # Generate study methods based on learning style
            study_methods = {
                'Visual': "Use diagrams, charts, and videos to enhance understanding.",
                'Auditory': "Listen to podcasts, recorded lectures, or discuss with others.",
                'Kinesthetic': "Use hands-on learning, such as practicing problems or building models."
            }

            # Adjust schedule for breaks and preferred study time
            subject_schedule = schedule[subject]
            subject_schedule['study_method'] = study_methods[learning_style]
            subject_schedule['time_of_day'] = f"Study in the {study_time}"
            subject_schedule['breaks'] = f"Take a {break_interval}-minute break every {break_interval} minutes of study."

        # Print to debug
        print(schedule)

        # Render the schedule page with generated data
        return render_template('schedule.html', schedule=schedule)

    return render_template('form.html')


@app.route('/schedule', methods=['GET'])
def schedule():
    # You could pull the study plan from a session or database if you wanted persistence
    return render_template('schedule.html', study_plan=None)  # Just in case if it's directly visited

if __name__ == '__main__':
    app.run(debug=True)
