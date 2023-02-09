function updateStudents() {
    let url = '/api/get_exam_data'

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',

        }
    }).then((response) => {
        console.log(response.json())
        return response.json()
    })
}

window.onload = function () {
    updateStudents();
}