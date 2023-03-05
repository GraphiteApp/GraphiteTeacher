const timeout = 1000

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

function sortNames(a, b) {
    if (a.toLowerCase() < b.toLowerCase()) {
        return 0
    }

    return 1
}

function updateStudents(data) {
    let studentList = document.getElementById('student-list')

    studentList.innerHTML = ''

    if (data.students.length + data.left_students.length) {
        // clear list
        data.students = data.students.concat(data.left_students)
        data.students = data.students.sort(sortNames)

        data.students.forEach((student) => {
            let studentItem = document.createElement('tr')

            let studentName = document.createElement('td')
            studentName.scope = 'row'
            studentName.innerText = student
            studentName.className = 'text-align-center'

            studentItem.appendChild(studentName)

            let studentStatus = document.createElement('td')

            if (data.left_students.includes(student)) {
                studentStatus.innerText = 'Left'
                studentStatus.style.color = 'red'
            } else {
                studentStatus.innerText = 'Present'
                studentStatus.style.color = 'green'
            }

            studentStatus.className = 'text-align-center'

            studentItem.appendChild(studentStatus)

            let removeButton = document.createElement('td')
            removeButton.className = 'text-align-center'

            let removeButtonButton = document.createElement('button')
            removeButtonButton.className = 'btn btn-outline-danger btn-sm'

            let removeButtonText = document.createElement('i')
            removeButtonText.className = 'bi bi-x'

            removeButtonButton.appendChild(removeButtonText)

            removeButton.appendChild(removeButtonButton)

            studentItem.appendChild(removeButton)

            studentList.appendChild(studentItem)
        })
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