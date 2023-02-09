const timeout = 2500

async function getData() {
    let url = '/api/get_exam_data'

    return fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then((response) => {
        return response.json()
    }).then((data) => {
        return data
    }).catch((error) => {
        console.log(error)
        return null
    })
}

function updateStudents(data) {
    let studentList = document.getElementById('student-list')

    if (data.students.length) {
        // clear list
        studentList.innerHTML = ''
        data.students.forEach((student) => {
            let studentItem = document.createElement('li')
            studentItem.innerHTML = student
            studentList.appendChild(studentItem)
        })
    } else {
        studentList.innerHTML = 'No students found'
    }
}

async function updateExam() {
    let data = await getData()

    if (data) {
        updateStudents(data)
    }

    setTimeout(updateExam, timeout)
}

window.onload = function () {
    updateExam().then()
}