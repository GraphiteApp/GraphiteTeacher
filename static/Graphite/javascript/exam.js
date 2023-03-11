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

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
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

    updateExam().then()
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
    // TODO: implement
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


        let resourceStatus = document.createElement('td')

        if (resource.isAllowed) {
            resourceStatus.innerText = 'Enabled'
            resourceStatus.style.color = 'green'
        } else {
            resourceStatus.innerText = 'Disabled'
            resourceStatus.style.color = 'red'
        }

        resourceStatus.className = 'text-align-center'

        resourceItem.appendChild(resourceStatus)


        let resourceURL = document.createElement('td')
        resourceURL.className = 'text-align-center'

        let resourceURLLink = document.createElement('a')
        resourceURLLink.href = resource.url
        resourceURLLink.innerText = resource.url

        resourceURL.appendChild(resourceURLLink)

        resourceItem.appendChild(resourceURL)


        let resourceButton = document.createElement('td')
        resourceButton.className = 'text-align-center'

        let resourceButtonButton = document.createElement('button')

        if (resource.isAllowed) {
            resourceButtonButton.className = 'btn btn-outline-danger btn-sm'
            resourceButtonButton.innerText = 'Disable'
        } else {
            resourceButtonButton.className = 'btn btn-outline-success btn-sm'
            resourceButtonButton.innerText = 'Enable'
        }

        resourceButtonButton.onclick = toggleResource(resource.name, resource.isAllowed)

        resourceButton.appendChild(resourceButtonButton)

        resourceItem.appendChild(resourceButton)

        // filler for the add resource button
        let addResourceFiller = document.createElement('td')
        addResourceFiller.className = 'text-align-center'

        resourceItem.appendChild(addResourceFiller)

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
