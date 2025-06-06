function view_questions(questions) {
    for (let i = 0, size = questions.length; i < size; i++) {
        const form = document.getElementById('application_form');
        
        const bold = document.createElement('strong');
        bold.innerHTML = questions[i];
        form.append(bold);

        const textarea = document.createElement('textarea');
        textarea.className = 'form-control';
        textarea.rows = '4';
        textarea.name = `answer_to_question_${i+1}`;
        form.append(textarea);
    }
}

function edit_questions(questions, answers) {
    for (let i = 0, size = questions.length; i < size; i++) {
        const form = document.getElementById('application_form');
        
        const bold = document.createElement('strong');
        bold.innerHTML = questions[i];
        form.append(bold);

        const textarea = document.createElement('textarea');
        textarea.className = 'form-control';
        textarea.rows = '4';
        textarea.name = `answer_to_question_${i+1}`;
        textarea.innerHTML = answers[i];
        form.append(textarea);
    }
}

function update_profile(id) {
    console.log(id);

    const age = document.getElementById(`age`).value;
    const gender = document.getElementById(`gender`).value;
    const ethnicity = document.getElementById(`ethnicity`).value;
    const picture = document.getElementById(`picture`).value;
    const military = document.getElementById(`military`).value;

    fetch(`/edit/${id}`, {
        method: "POST",
        headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
        body: JSON.stringify({
            age: age,
            gender: gender,
            ethnicity: ethnicity,
            military: military,
            picture: picture,
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
}

function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) {
        return parts.pop().split(';').shift();
    }
}