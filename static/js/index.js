function fetchTasks() {
    fetch('/tasks')
        .then(response => response.json())
        .then(tasks => {
            const taskContainer = document.getElementById('task-container');
            taskContainer.innerHTML = '';

            tasks.sort((a, b) => a.id - b.id);

            tasks.forEach(task => {
                const taskElement = document.createElement('li');
                taskElement.innerHTML = `
                    ${task.title} (${task.status})
                    <div class="task-actions">
                        <button class="complete-btn" onclick="updateTask(${task.id})">Completar</button>
                        <button class="delete-btn" onclick="deleteTask(${task.id})">Deletar</button>
                    </div>
                `;
                taskContainer.appendChild(taskElement);
            });
        });
}

function addTask() {
    const title = document.getElementById('task-title').value;

    if (title === '') {
        alert('O título não pode estar vazio');
        return;
    }

    fetch('/task/add', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title: title, status: 'pending' })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        fetchTasks();
    })
    .catch(error => console.error('Erro ao adicionar a tarefa:', error));
}

function updateTask(id) {
    fetch(`/task/update/${id}`, {
        method: 'PUT',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: 'completed' })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        fetchTasks();
    })
    .catch(error => console.error('Erro ao atualizar a tarefa:', error));
}

function deleteTask(id) {
    fetch(`/task/delete/${id}`, {
        method: 'DELETE',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        fetchTasks();
    })
    .catch(error => console.error('Erro ao deletar a tarefa:', error));
}

function deleteAllTasks() {
    if (confirm("Você tem certeza que deseja deletar todas as tarefas?")) {
        fetch('/tasks', {
            method: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            fetchTasks();
        })
        .catch(error => console.error('Erro ao deletar todas as tarefas:', error));
    }
}

document.getElementById('delete-all-tasks-btn').addEventListener('click', deleteAllTasks);
document.getElementById('add-task-btn').addEventListener('click', addTask);
fetchTasks();
