const timeout = 1000

function getCSRFToken() {
    let cookies = document.cookie.split(';')
    let token = ''

    cookies.forEach((cookie) => {
        if (cookie.includes('csrftoken')) {
            token = cookie.split('=')[1]
        }
    });

    return token
}

function post(url, data) {
    data['csrfmiddlewaretoken'] = getCSRFToken()

    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': data.csrfmiddlewaretoken
        },
        body: JSON.stringify(data)
    }).then((response) => {
        return response.json()
    }).then((data) => {
        return data
    }).catch((error) => {
        console.log(error)
        return null
    })
}

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

function remove_student(studentName) {
    let url = '/api/remove_student'

    let cookies = document.cookie.split(';')
    let csrfToken = ''

    cookies.forEach((cookie) => {
        if (cookie.includes('csrftoken')) {
            csrfToken = cookie.split('=')[1]
        }
    });

    let data = {
        'username': studentName,
        'csrfmiddlewaretoken': csrfToken
    }

    post(url, data).then(() => {
        updateExam().then()
    })
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
            studentItem.id = "student-" + student

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
            removeButtonButton.onclick = function () {
                remove_student(student)
            }

            removeButtonButton.appendChild(removeButtonText)

            removeButton.appendChild(removeButtonButton)

            studentItem.appendChild(removeButton)

            studentList.appendChild(studentItem)
        })
    }
}

function toggleResource(resourceName, isAllowed) {
    post('/api/toggle_resource', {
        'resource': resourceName,
        'isEnable': !isAllowed
    }).then(() => {
        updateExam().then()
    })
}

function deleteResource(resourceName) {
    if (!confirm('Are you sure you want to delete the resource?')) {
        return
    }

    post('/api/delete_resource', {
        'resource': resourceName
    }).then(() => {
        updateExam().then()
    })
}

function updateResources(data) {
    let resourcesList = document.getElementById('resources-list')

    resourcesList.innerHTML = ''

    for (let key in data.resources) {
        let resource = data.resources[key]


        let resourceItem = document.createElement('tr')
        resourceItem.id = "resource-" + key


        let resourceName = document.createElement('td')
        resourceName.scope = 'row'
        resourceName.innerText = resource.name
        resourceName.className = 'text-align-center'

        resourceItem.appendChild(resourceName)

        let resourceButton = document.createElement('td')
        resourceButton.className = 'text-align-center'

        let resourceButtonButton = document.createElement('button')

        // set the onclick function
        resourceButtonButton.onclick = function () {
            toggleResource(resource.name, resource.isAllowed)
        }

        if (resource.isAllowed) {
            resourceButtonButton.className = 'btn btn-outline-danger btn-sm'
            resourceButtonButton.innerText = 'Disable'
        } else {
            resourceButtonButton.className = 'btn btn-outline-success btn-sm'
            resourceButtonButton.innerText = 'Enable'
        }

        resourceButton.appendChild(resourceButtonButton)

        resourceItem.appendChild(resourceButton)

        let resourceURL = document.createElement('td')
        resourceURL.className = 'text-align-center'

        let resourceURLLink = document.createElement('a')
        resourceURLLink.href = resource.url
        resourceURLLink.innerText = resource.url

        resourceURL.appendChild(resourceURLLink)

        resourceItem.appendChild(resourceURL)

        // edit resource
        let resourceEdit = document.createElement('td')
        resourceEdit.className = 'text-align-center'

        let resourceEditButton = document.createElement('a')
        resourceEditButton.className = 'btn btn-outline-primary btn-sm'

        let resourceEditText = document.createElement('i')
        resourceEditText.className = 'bi bi-pencil-square'

        resourceEditButton.href = '/add_resource' + '?resource=' + resource.name

        resourceEditButton.appendChild(resourceEditText)

        resourceEdit.appendChild(resourceEditButton)

        resourceItem.appendChild(resourceEdit)

        let resourceDelete = document.createElement('td')
        resourceDelete.className = 'text-align-center'

        let resourceDeleteButton = document.createElement('button')
        resourceDeleteButton.className = 'btn btn-outline-danger btn-sm'

        let resourceDeleteText = document.createElement('i')
        resourceDeleteText.className = 'bi bi-trash'
        resourceDeleteButton.onclick = function () {
            deleteResource(resource.name)
        }

        resourceDeleteButton.appendChild(resourceDeleteText)

        resourceDelete.appendChild(resourceDeleteButton)

        resourceItem.appendChild(resourceDelete)


        resourcesList.appendChild(resourceItem)
    }
}

async function updateExam() {
    let data = await getData()

    if (data) {
        updateStudents(data)
        updateResources(data)
    }

    setTimeout(updateExam, timeout)
}

window.onload = function () {
    updateExam().then()
}
